from time import time, sleep
from random import randint
from datetime import datetime
from json import loads
import weakref
import pandas as pd

from .display import DEBUG, WARN, SCALER
from .exceptions import *





class LocustEndpoint:

    instances   = list()
    previous    = None

    def __init__(self, endpoint, methods, name=None, headers=None, body=None):
        """Core backpack class representing endpoints and their data"""

        self.__class__.instances.append(weakref.proxy(self))
        self.__nonzero__ = self.__bool__    # For Python 2 compatibility

        self.endpoint   = endpoint
        self.name       = name if name is not None else endpoint
        self.original   = self.name
        self.methods    = methods
        self.headers    = headers if headers is not None else {}
        self.body       = body if body is not None else {}
        self.instance   = None
        self.Result     = None

        self.columns    = ['response_time', 'status']
        self.statistics = pd.DataFrame(columns=self.columns)

        self.current_pivot = False
        self.sealed = False
        self.debug = False

        self.transit = lambda x: None
        self.dependencies = list()


    def __add__(self, member):
        """LocustEndpoint addition support for chaining dependant requests"""

        if not self.current_pivot:
            self.Request()
            self.current_pivot = True
        if self.Result.success: 
            member.Request()
            member.current_pivot = True
        self.current_pivot   = False
        return member

    def __rshift__(self, member):
        """LocustEndpoint dependency building support using right shift operator"""

        member.transit(self)
        return member
    


    def __bool__(self):
        """Bool implementation for easier result checking
            Example: if <LocustEndpoint>: 
                returns True if <LocustEndpoint>.Result.success is True"""

        try:
            if self.Result.success: return True
            else: return False
        except: return False


    @property
    def seal(self):
        """Blocks this LocustEndpoint from doing requests until unsealed"""
        self.sealed = True
        self.Result = self.RequestResult(False, 'null', self.endpoint)
        WARN("{} SEALED".format(self.endpoint))

    @property
    def unseal(self):
        """Unseals the sealed LocustEndpoint to re-enable requests"""
        self.sealed = False
        WARN("{} UNSEALED".format(self.endpoint))


    def attach(self, caller): self.instance = caller

    @property
    def DEBUG_MODE_ON(self):
        self.debug = True
        DEBUG("DEBUG MODE ACTIVATED FOR {}".format(self.endpoint))

    @property
    def DEBUG_MODE_OFF(self):
        self.debug = False
        DEBUG("DEBUG MODE DEACTIVATED FOR {}".format(self.endpoint))

    def bank_statistics(self, response_time, status):
        prev = self.previous.endpoint if self.previous is not None else 'First'
        data = {
            'response_time' : response_time,
            'status'        : status,
            'previous_req'  : prev,
            'stamp'         : datetime.now().strftime('%H:%M:%S')
        }
        self.statistics = self.statistics.append(data, ignore_index=True)


    def set_dependency_rule(self, asker, *dependency):
        if len(dependency) == 1:
            self.dependencies.append((asker, dependency[0]))
        # TODO - Complete this for deep dependency


    def Enhance(self, enhancing_func):
        self.Request = enhancing_func(self.Request)

    def Request(self, method=None):
        if self.sealed: return

        if self.instance == None: raise NoAttachmentException("LoustEndpoint not attached to Locust TaskSet object")
        elif method == None and type(self.methods) == str: method = self.methods


        if type(method) == list and method.lower() in self.methods or type(method) == str and (method.lower() == self.methods or method.lower() in self.methods):
            if   method == 'get'     :  self.get()           
            elif method == 'post'    :  self.post()
            elif method == 'patch'   :  self.patch()
            elif method == 'delete'  :  self.delete()
            self.__class__.previous = self

        if len(self.methods) > 1 and method == None and type(self.methods) == list:
            err = "This endpoint supports more than one method which requires specifying it when calling the request function"
            raise MissingMethodException(err)
        elif type(self.methods) == str and self.methods != method.lower() and method is not None:
            err = "Request was called with {} but only supports {}".format(method.upper(), self.methods.upper())
            raise MissingMethodException(err)


    def get(self):
        t0 = time()
        req = self.instance.client.get(self.endpoint,
                            name            = self.name,
                            headers         = self.headers,
                            params          = self.body,
                            catch_response  = True
                            )
        self.status_check(req, time() - t0)


    def post(self):
        t0 = time()
        req = self.instance.client.post(self.endpoint,
                            name            = self.name,
                            headers         = self.headers,
                            json            = self.body,
                            # data            = self.body,
                            # params          = self.body,
                            catch_response  = True
                            )
        self.status_check(req, time() - t0)


    def patch(self):
        t0 = time()
        req = self.instance.client.patch(self.endpoint,
                            name            = self.name,
                            headers         = self.headers,
                            json            = self.body,
                            catch_response  = True
                            )
        self.status_check(req, time() - t0)


    def delete(self):
        t0 = time()
        req = self.instance.client.delete(self.endpoint,
                            name            = self.name,
                            headers         = self.headers,
                            catch_response  = True
                            )
        self.status_check(req, time() - t0)



    def status_check(self, request_object, t):
        timeout = "Empty response, possible timeout"
        if request_object.status_code >= 200 and request_object.status_code < 400:
            self.Result = self.RequestResult(True, request_object, self.endpoint)
            self.resolve_dependencies()
            request_object.success()
            self.bank_statistics(t, self.Result.success)
        elif request_object.status_code == 0:
            self.Result = self.RequestResult(False, request_object, self.endpoint)
            request_object.failure(
                "{} - {}".format(request_object.content, timeout))
        else:
            self.Result = self.RequestResult(False, request_object, self.endpoint)
            request_object.failure("{}".format(request_object.content))



    def resolve_dependencies(self):
        if len(self.dependencies) >= 1:             # Check if there are any deps first
            for dependency in self.dependencies:
                if len(dependency[1]) == 1:         # Only top level key needed
                    dep = dependency[1][0]          # Get the dep from the 1-elem tuple
                    try:
                        dependency[0].body[dep] = self.Result.json()[dep]   # Pass it
                    except Exception as e:
                        WARN("Unable to resolve '{}' dependency for {}: {}".format(
                            dependency[1], dependency[0], str(e)
                        ))
                else:                               # Deeper key needed
                    depth = 0
                    resp = self.Result.json()       # Initial response
                    for _ in range(len(dependency[1])):
                        resp = resp[dependency[1][depth]]   # Go deeper in the response
                        depth += 1
                    try:
                        dependency[0].body[dep] = self.Result.json()[resp] # TODO Dynamic depth assignation
                    except Exception as e:
                        WARN("Unable to resolve '{}' dependency for {}: {}".format(
                            dependency[1], dependency[0], str(e)
                        ))



    class RequestResult:
        def __init__(self, status, request_object, endpoint):
            """The result subclass of each request made by a LocustEndpoint"""

            self.success = status
            self.failure = not status
            self.endpoint = endpoint
            self.json    = lambda: self.content_as_json()
            
            try: self.status_code = request_object.status_code
            except: self.status_code = 0
            try: self.response = request_object.content
            except: self.response = {}

        
        def content_as_json(self):
            if self.response == {}: return {}
            try: js = loads(self.response)
            except:
                js = {}
                WARN("CANNOT CONVERT RESPONSE OF {} TO JSON".format(self.endpoint))
            finally: return js


class LocustEndpointCollection(object):
    created = 0
    def __init__(self):
        self.instances = LocustEndpoint.instances
        self.unique = self.separate_uniques()

        self.endpoint_statistics = self.frame_welder()

        
    def separate_uniques(self):
        uniques = dict()
        for instance in self.instances:
            if instance.endpoint in uniques.keys():
                uniques[instance.endpoint].append(instance)
            else:
                uniques[instance.endpoint] = [instance]
        return uniques

    def frame_welder(self):
        frame_collection = dict()

        for endp in self.unique:
            new_frame = pd.concat([x.statistics for x in self.unique[endp]], ignore_index=True)
            new_frame.sort_values(by=['stamp'], inplace=True, ascending=True)
            frame_collection[endp] = new_frame
        
        return frame_collection


    def __new__(cls, *args, **kwargs):
        if LocustEndpointCollection.created < 1:
            LocustEndpointCollection.created += 1
            return object.__new__(cls, *args, **kwargs)
        else: return