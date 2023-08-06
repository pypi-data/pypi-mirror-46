from time import time, sleep, strftime, gmtime
from datetime import datetime
from re import sub
from locust import runners, events
import gevent, requests, os

from .core import LocustEndpoint, LocustEndpointCollection
from .display import DEBUG, WARN, SCALER


def Date(end):
    """
    Returns a strftime formatted date

    Passs "end" as a string. Examples:
        10s, 15s, 5m, 8m, 2h, 3h, 1d, etc.
        s => seconds
        m => minutes
        h => hours
        d => days
    """

    if end.endswith("s"):
        multiplier = 1
    elif end.endswith("m"):
        multiplier = 60
    elif end.endswith("h"):
        multiplier = 3600
    elif end.endswith("d"):
        multiplier = 86400

    now = int(time())
    this_much_time = int(sub(r"\D", "", end))
    secs_to_add = now + this_much_time * multiplier
    result = strftime('%Y-%m-%d %H:%M:%S', gmtime(secs_to_add))

    return result

def Clock(time_string):
    """
    Returns an int representing the given string in seconds

    Passs "end" as a string. Examples:
        10s, 15s, 5m, 8m, 2h, 3h, 1d, etc.
        s => seconds
        m => minutes
        h => hours
        d => days
    """
    if time_string.endswith("s"):
        multiplier = 1
    elif time_string.endswith("m"):
        multiplier = 60
    elif time_string.endswith("h"):
        multiplier = 3600
    elif time_string.endswith("d"):
        multiplier = 86400

    this_much_time = int(sub(r"\D", "", time_string))
    
    return int(this_much_time * multiplier)


def SetGlobal(variable, value, inst):
    """ Set a LocustEndpoint variable for all or selected Endpoints """
    if isinstance(inst, list):
        for instance in inst:
            try: setattr(instance, variable, value)
            except: WARN("Cannot assign {} variable".format(variable))
    else:
        for instance in inst.BackpackPouch:
            try: setattr(instance, variable, value)
            except: WARN("Cannot assign {} variable".format(variable))


def SealAll(inst):
    """ Seal all LocustEndpoint instances making them unable to perform requests"""
    for instance in inst.BackpackPouch:
        instance.seal

def UnsealAll(inst):
    """ Unseal all LocustEndpoint instances making them able to perform requests"""
    for instance in inst.BackpackPouch:
        instance.unseal

def Unzip(inst):
    inst.BackpackPouch = list()
    attributes = inst.__dict__
    for attribute in attributes:
        if isinstance(attributes[attribute], LocustEndpoint):
            inst.BackpackPouch.append(attributes[attribute])
            attributes[attribute].attach(inst)
    

called_once = 0
def Zip():
    """Zip can be called by the Locust Master to save the test details
        Zip should be called when Locust is still active to have access to the Locust UI"""

    global called_once
    if called_once >= 1: return
    called_once +=1

    url = "http://{}:8089/".format(MasterIP())
    output = make_current_test_dir()
    collect = LocustEndpointCollection()

    def check():
        code = requests.get(url).status_code
        if code != 200:
            WARN("Bad status code ({}) from {}".format(code, url))

    def download_csv_files(url):
        import wget, sys

        os.mkdir(output+"/csv")

        csvs = [url + "stats/requests/csv",
                url + "stats/distribution/csv",
                url + "exceptions/csv" ]
                
        sys.stdout.fileno = lambda: 1
        for url in csvs:
            wget.download(url, out=output+"/csv")
    

    def plot_and_save_stats():
        import matplotlib.pyplot as plt

        os.mkdir(output+"/plots/")

        for frame in collect.endpoint_statistics:
            df = collect.endpoint_statistics[frame]
            df.plot(x='stamp', y='response_time', style='-')
            plt.savefig(output+"/plots/" + frame.strip("/"), bbox_inches='tight')

    def build_stats_page():
        pass # ?????


    try: check()
    except: 
        WARN("Cannot contact address {}".format(url))
        return
    
    try: download_csv_files(url)
    except Exception as e: WARN("Failed to download CSV files: {}".format(e))
    try: plot_and_save_stats()
    except Exception as e: WARN("Failed to plot and save statistics: {}".format(e))
    try: build_stats_page()
    except Exception as e: WARN("Failed to build and save stats page: {}".format(e))


def MasterIP():
    import socket
    try:
        master = runners.locust_runner.master_host
    except AttributeError:
        master = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
    return str(master)

def make_current_test_dir():
    this = datetime.now()
    folder_name = "LT_{}_{}_{}_{}_{}".format(this.year, this.month, this.day, this.hour, this.minute)
    dirn = os.path.dirname(os.path.realpath(__file__)) + '/results/' + folder_name
    os.makedirs(dirn)
    return dirn