from time import time, sleep
from random import randint



class Scenario(object):
    # instances = list()
    def __init__(self, endpoints, wait=1, pause=0, runtime=None, independent_requests=False):
        """
        The endpoints parameter is a list that accepts tuples containing:
            (<LocustEndpoint object>, <request method>)
        """

        # self.__class__.instances.append(weakref.proxy(self))

        self.runtime = runtime
        self.wait = wait
        self.pause = pause
        self.endpoints = endpoints
        self.independent_requests = independent_requests
        self.scenario_complete = False
        self.stop = False

        self.run_once = lambda: self.run(once=True)


    def run(self, once=False):
        started = time()
        self.scenario_complete = False

        def run_independent():
            if self.runtime != None:
                while time() - started < self.runtime:
                    for endpoint, method in self.endpoints:
                        endpoint.Request(method)
                        sleep(self.wait)
                    sleep(self.pause)
                    if once: break
                self.scenario_complete = True
            else:
                while not self.stop:
                    for endpoint, method in self.endpoints:
                        endpoint.Request(method)
                        sleep(self.wait)
                    sleep(self.pause)
                    if once: break
                self.scenario_complete = True

        def run_dependent():
            if self.runtime != None:
                while time() - started < self.runtime:
                    for endpoint, method in self.endpoints:
                        endpoint.Request(method)
                        if not endpoint.Result.success: continue
                        sleep(self.wait)
                    sleep(self.pause)
                    if once: break
                self.scenario_complete = True
            else:
                while not self.stop:
                    for endpoint, method in self.endpoints:
                        endpoint.Request(method)
                        if not endpoint.Result.success: continue
                        sleep(self.wait)
                    sleep(self.pause)
                    if once: break
                self.scenario_complete = True

        def run_weighted():
            if self.runtime != None:
                while time() - started < self.runtime:
                    for endpoint, method, chance in self.endpoints:
                        if chance <= randint(1, 100):
                            endpoint.Request(method)
                            sleep(self.wait)
                    sleep(self.pause)
                    if once: break
                self.scenario_complete = True
            else:
                while not self.stop:
                    for endpoint, method, chance in self.endpoints:
                        if chance <= randint(1, 100):
                            endpoint.Request(method)
                            sleep(self.wait)
                    sleep(self.pause)
                    if once: break
                self.scenario_complete = True


        if isinstance(self, WeightedScenario): run_weighted()
        elif not self.independent_requests: run_dependent()
        else: run_independent()



    # DUNDERS
    def __len__(self):
        return len(self.endpoints)

    def __getitem__(self, index):
        return self.endpoints[index]

    # def __del__(self): pass



class WeightedScenario(Scenario):
    def __init__(self, endpoints, wait=1, runtime=None):
        """
        The endpoints parameter is a list that accepts tuples containing:
            (<LocustEndpoint object>, <request method>, <weight>)
        """

        independent_requests = True
        try:
            super().__init__(self, endpoints, wait, runtime, independent_requests)
        except TypeError:
            super(WeightedScenario, self).__init__(endpoints, wait, runtime, independent_requests)


class SequenceScenario(Scenario):
    def __init__(self, endpoints, wait=1, runtime=None):
        """
        The endpoints parameter is a list of lists of tuples containing:
            (<LocustEndpoint object>, <request method>, <weight> (optional))
        """

        independent_requests = True
        try:
            super().__init__(self, endpoints, wait, runtime, independent_requests)
        except TypeError:
            super(SequenceScenario, self).__init__(endpoints, wait, runtime, independent_requests)   
        

    # TODO - Create a sequence-like task flow // Currently broken and tracebacky
    def run(self):
        print(type(self.endpoints[0]))
        def run_weighted():
            pass
        def run_normal():       # TODO - Add per-sequence runtime support
            for _set in self.endpoints:
                if len(_set) == 2:      # Unweighted endpoints
                    for endpoint, method in _set:
                        endpoint.Request(method)
                        sleep(self.wait)
                elif len(_set) == 3:    # Weighted endpoints
                    for endpoint, method, chance in _set:
                        if chance <= randint(1, 100):
                            endpoint.Request(method)
                            sleep(self.wait)

        
        if isinstance(self.endpoints[0], tuple): run_weighted()
        elif isinstance(self.endpoints[0], list): run_normal()