from locust import runners, events
from json import loads
from math import ceil, floor
from time import sleep
import numpy as np
import pandas as pd
import gevent
import requests

from .tools import WARN, DEBUG, SCALER



def kill_locusts(self, kill_count):
    """
    Kill a kill_count of weighted locusts from the Group() object in self.locusts
    """
    bucket = self.weight_locusts(kill_count)
    kill_count = len(bucket)
    self.num_clients -= kill_count
    dying = []
    for g in self.locusts:
        for l in bucket:
            if l == g.args[0]:
                dying.append(g)
                bucket.remove(l)
                break
    for g in dying:
        if g.name != 'Greenlet-0':
            self.locusts.killone(g)
    events.hatch_complete.fire(user_count=self.num_clients)



class AutoScaler(object):
    def __init__(self, target_rps, volatility_threshold=0.1, max_ccu=100, epsilon=1, cycle_step=5):

        runners.locust_runner.kill_locusts = kill_locusts
        
        self.current_locusts    = lambda: runners.locust_runner.user_count - 1
        self.current_rps        = lambda: loads(requests.get("http://localhost:8089/stats/requests").content)['total_rps']
        self.state              = lambda: runners.locust_runner.state
        self.percentile         = lambda: runners.locust_runner.stats.total.get_current_response_time_percentile(0.95)
        self.epsilon            = epsilon
        self.cycle_step         = cycle_step
        self.target_rps         = target_rps
        self.volatility         = volatility_threshold
        self.stop               = False
        self.scalings_performed = 0

        self.last_outcomes      = list()
        self.alerts             = 0
        
        self.max_ccu            = max_ccu


        SCALER("AUTOSCALING STARTED FOR A TARGET OF {} RPS".format(self.target_rps))
        self.start_scaling_cycle()
    
    def start_scaling_cycle(self):
        while not self.stop:
            users   = self.current_locusts()
            total   = self.current_rps()
            single  = total / users if users >= 1 else 0
            target  = self.target_rps


            if self.state() == 'running' and self.is_stable():
                if total < target + self.epsilon and single > 0:
                    to_spawn    = int(ceil(target / single)) - users
                    if to_spawn + users > self.max_ccu:
                        to_spawn = int(floor(self.max_ccu - total - 1))
                        SCALER("Scaling UP with {} more users".format(to_spawn))
                        self.spawn(to_spawn)
                        self.max_ccu_reached()
                        break
                    SCALER("Scaling UP with {} more users".format(to_spawn))
                    self.spawn(to_spawn)
                    self.upscale_efficiency()
                elif total > target - self.epsilon:
                    to_kill     = (int(ceil((total - target) / single))) - 1
                    SCALER("Scaling DOWN with {} less users".format(to_kill))
                    self.kill(to_kill)

            sleep(self.cycle_step)
        SCALER("AUTOSCALING STOPPED")


    def kill(self, count):
        runners.locust_runner.kill_locusts(runners.locust_runner, kill_count=count)

    def spawn(self, count):
        runners.locust_runner.spawn_locusts(spawn_count=count)

    
    def is_stable(self):
        vals = list()
        for _ in range(3):
            current_rps = self.current_rps()
            vals.append(round(current_rps, 2))
            sleep(1.5)

        arr = np.array(vals)
        discrete = np.diff(arr)

        stability = list()
        for num in abs(discrete):
            if num <= self.volatility: stability.append(True)
            else: stability.append(False)
        
        if all(stability):
            return True
        return False


    def upscale_efficiency(self):
        if len(self.last_outcomes) != 3:
            if len(self.last_outcomes) == 4:
                self.last_outcomes.pop(0)
                self.last_outcomes.append(self.current_rps())
                return
            else: 
                self.last_outcomes.append(self.current_rps())
                return
        elif len(self.last_outcomes) == 3:
            x1, x2, x3 = self.last_outcomes
            print(x1, x2, x3)

            A_diff = x1 - x2
            B_diff = x2 - x3

            if (A_diff > 0) and (B_diff > 0):
                WARN("Test is failing !")
                self.alerts += 1
            elif (A_diff > 0) or (B_diff > 0):
                WARN("Test might be failing !")
            else:
                SCALER("Test is stable")
                self.alerts -= 1 if self.alerts > 0 else 0

            self.stop = True if self.alerts >= 3 else False


    def max_ccu_reached(self):
        SCALER("The imposed limit of {} CCU will be reached !".format(self.max_ccu))
        self.stop = True

    
    def __new__(cls, *args, **kwargs):
        if gevent.getcurrent().name == 'Greenlet-0':
            return object.__new__(cls, *args, **kwargs)
        else: return


class HatchingSeason(object):
    def __init__(self, batches=5, interval=10):
        """This feature enables Locust to create new connections every set interval
            This CANNOT currently run along the AutoScaler
            WARNING! This feature locks Greenlet-0 into a special task"""

        runners.locust_runner.kill_locusts = kill_locusts

        self.batch      = batches
        self.interval   = interval

        self.stop = False

        self.kill   = AutoScaler.__dict__['kill']
        self.spawn  = AutoScaler.__dict__['spawn']

        self.hatchery()

    def hatchery(self):
        while not self.stop:
            if runners.locust_runner.state == 'running':
                self.kill(self, self.batch + 1)
                sleep(2)
                self.spawn(self, self.batch)
                sleep(self.interval)
            else: sleep(self.interval)


    def __new__(cls, *args, **kwargs):
        if gevent.getcurrent().name == 'Greenlet-0':
            return object.__new__(cls, *args, **kwargs)
        else: return


class Chain:
    def __init__(self, endpoints, independent=False, wait=0):
        self.chain = endpoints
        self.wait = wait
        self.dependent() if independent == False else self.independent()


    def dependent(self):
        start = self.chain[0]
        end   = self.chain[-1]

        previous = 0
        for x in self.chain:
            endpoint = x[0]
            method = x[1]
            if endpoint == start[0]:
                endpoint.Request(method)
                sleep(self.wait)
                if not endpoint.Result.success: break
                else: previous += 1
            elif endpoint == end[0]:
                if self.chain[previous-1][0].Result.success:
                    endpoint.Request(method)
                else: break
            else:
                if self.chain[previous-1][0].Result.success:
                    endpoint.Request(method)
                    sleep(self.wait)

    def independent(self): # TODO
        pass