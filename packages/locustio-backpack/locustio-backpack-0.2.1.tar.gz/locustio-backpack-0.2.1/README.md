# Locust Backpack

The **Locust Backpack** is a Locustio load testing framework extension that aims to simplify writing load test scripts while also adding some functionality and awesome quirks.

The main idea behind the module is "Endpoints as objects". 
This means less hardcoding, fewer decision blocks, smaller chances for mistakes and bugs, less stress and more fun.


## Getting Started

Starting to use the **Backpack** is simple. After placing the module in your working directory, import it from the Locust script:
```
import locust_backpack as Backpack
```
At this point, you are a proud user of the Locust Backpack. Time to put it to work.



## Initialization
As mentioned earlier, the **Backpack** ideology is "Endpoints as objects".  Thus, we have to create objects from all the endpoints which will later be used in the load test.

This can be done outside the TaskSet child class, in a different file, or just wherever we prefer.

The master class holding the endpoint data is **LocustEndpoint**. Each individual endpoint has to be initialized with an instance of this class, accepting the following parameters:
```
LocustEndpoint(self, endpoint, methods, name=None, headers=None, body=None)
```

|  Argument      |Description                    |Default|
|----------------|-------------------------------|-----------------------------|
|**endpoint (str)**|`string representing the actual endpoint`|`N/A`|
|**methods (str or list)**|`string or list containing all the methods the endpoint supports`|`N/A`|
|**name (str)** |`string representing a friendly or a debug name for the endpoint. This is the name the endpoint will have on the Locust UI`|`name = endpoint`|
|**headers(dict)**|`the headers this endpoint will use`|`{}`|
|**body(dict)**|`the body this endpoint will use`|`{}`|

>Note: The values passed when initializing a LocustEndpoint are not permanent. These can be modified anytime during the test !

Examples:

**Only the mandatory parameters:**

```
TeamInit = Backpack.LocustEndpoint('/public/team/v1/init', 'post')
```
```
PvP2Init = Backpack.LocustEndpoint('/public/pvp2/v1/init', ['post', 'get'])
```

**Passing a custom name**

```
ResetSession = Backpack.LocustEndpoint('/public/session/v1/cheat/reset','post',
            name="/public/session/v1/cheat/reset::newUser")
```

**Passing a body**

```
SessionStart = Backpack.LocustEndpoint('/public/session/v1/start', 'post',
            name="/public/session/v1/start::newUser", 
            body={"device_type": "test",
                    "device_id": "test", 
                    "version": 320, 
                    "language": "RO", 
                    "gender": 1, 
                    "name": "load_test", 
                    "platform": 1})
```	


Once all our LocustEndpoints are created, we need access to the TaskSet in order to be able to make requests using Locust. This can be achieved in two ways:

Looping through a list of all endpoints and applying their _attach()_ method to the current context:

```
for endp in [TeamInit, ResetSession, SessionStart, PvP2Init, EventInit]:
    endp.attach(self)
```

Calling the Backpack method _Unzip()_ which does the same as above but saves you from providing a list of LocustEndpoints

```
Backpack.Unzip(self)
```



# Making Requests

### Simple Request

Remember  ```self.client.post(...)``` ? Forget about it.

Locust Backpack exposes a much simpler way of making a request and tracking it's result:
```
TeamInit.Request()
``` 
or 
```
TeamInit.Request('post')
```

Calling _Request()_ without a parameter will use the endpoint's passed method when initializing the LocustEndpoint. Specifying a method will use that method from the method pool.

> Note: If **LocustEndpoint** was initialized with a list of methods and _Request()_ is called without arguments, a **MissingMethodException** will be thrown !

But what happens under the hood when we ```LocustEndpoint.Request()``` ?
>* A self.client.method(*args) request is made, following the Locust style and using the default or provided method
>* A status code check is performed, registering the request.success or request.failure for Locust
>* A Result object is created, containing all the request information

---

### Simple-Chaining Dependent Requests

What if we want to connect multiple requests, but we want each subsequent request to be made only if the previous one succeeds? It couldn't be any easier!

```
ResetSession + SessionStart
``` 
_...seriously, that's all..._

The above is translated to:
>* Make a request to **ResetSession**
>* Check the result of **ResetSession**
>* If **ResetSession** is successful, make a request to **SessionStart**

Of course, any number of requests can be chained:
```
TeamInit + ResetSession + SessionStart + EventInit
```
Let's say ```TeamInit``` fails in the above scenario. In such case, no request following it will be performed because the dependency chain has failed from that point.

> Note: Simple-Chaining has no wait time between requests. If successful, each request will be made instantly after the previous one

> Note: Simple-Chaining only support LocustEndpoints that were declared with a single method
---
### Advanced-Chaining Dependent Requests

To address the limitations of Simple-Chaining, Advanced-Chaining was created.
Advanced-Chaining is defined by the backpack class _Chain()_ as such:
```
Chain(self, endpoints, independent=False, wait=0)
```

|  Argument      |Description                    |Default|
|----------------|-------------------------------|-----------------------------|
|**endpoints (list of tuples )**|`list of tuples containing an endpoint and it's method`|`N/A`|
|**independent(bool)**|`wether or not the provided endpoints depend on the success of the previous one`|`False`|
|**wait(int)** |`integer representing how much time to wait between making the provided requests`|`0`|



Example:
```
Backpack.Chain([(PvP2Init, 'get'), (PvP2Init, 'post')], wait=2)
```



# Scenarios

What if there was an easy way to build and run a scenario? Well there isn't one way to do it, but multiple.


### Simple Scenario

The most basic way of building a scenario is the backpack's _Scenario()_ class.

```Scenario(self, endpoints, wait=1, runtime=None, independent_requests=False)```

|  Argument      |Description                    |Default|
|----------------|-------------------------------|-----------------------------|
|**endpoints (list of tuples )**|`list of tuples containing an endpoint and it's method`|`N/A`|
|**wait(int)**|`integer representing how much time to wait(sec) between making the provided requests`|`1`|
|**runtime(int)** |`integer representing the runtime(sec) of the scenario`|`None`|
|**independent_requests(bool)**|`wether or not the provided endpoints depend on the success of the previous one`|`False`|

Example:
```
scenario_endpoints = [(TeamInit, 'post'), (ResetSession, 'post'),
                    (SessionStart, 'post'), (PvP2Init, 'get'),
                    (PvP2Init, 'post'), (EventInit, 'post')]
```

```
SCENARIO = backpack.Scenario(scenario_endpoints, runtime=10, independent_requests=True)
```

But this will not run the  Scenario yet! Two methods are available for running the scenario:

```
SCENARIO.run()
```
Or if you would like to run the scenario only once, regardless of runtime:
```
SCENARIO.run_once()
```

---
### Weighted Scenario
Maybe we want to add a chance for endpoints when running a scenario.
For that purpose, _WeightedScenario()_ comes into play. Subclassing the Simple Scenario, there are only two minor differences between them:

>* WeightedScenario() does not have an independent_requests argument
>* The tuples passed to WeightedScenario() have a 3rd element representing an int between 1-100 which is that chance for that request to be made (100 meaning 100% chance)

Example:
```
scenario_endpoints = [(TeamInit, 'post', 100), (ResetSession, 'post', 20),
                    (SessionStart, 'post', 100), (PvP2Init, 'get', 75), 
                    (PvP2Init, 'post', 15), (EventInit, 'post', 50)]

SCENARIO_2 = Backpack.WeightedScenario(scenario_endpoints, runtime=15)

SCENARIO_2.run()
```
or 
```
SCENARIO.run_once()
```

---
### Sequenced Scenario (WIP)
One other way of building a scenario is using the _Backpack.SequenceScenario()_ feature

What this scenario builder has special is it's ability to receive a list-of-lists-of-tuples or a list-of-tuples-of-lists-of-tuples.

Example:

First, we define some sequences. These are lists of tuples containing the LocustEndpoint, it's method and an **optional** weight/chance

```
sequence_1 = [(TeamInit, 'post', 10), (ResetSession, 'post', 20)]
sequence_2 = [(SessionStart, 'post', 30), (PvP2Init, 'get', 20)]
sequence_3 = [(PvP2Init, 'post', 50), (EventInit, 'post', 80)]
```

Then we build the sequenced scenario by passing the sequences above and an **optional** weight/chance

```
SCENARIO_3 = Backpack.SequenceScenario([sequence_1, sequence_2, sequence_3])
```
OR
```
SCENARIO_3 = Backpack.SequenceScenario([(sequence_1, 40), (sequence_2, 70), (sequence_3, 25)])
```

Then we can finally call the _run()_ method:

```
SCENARIO_3.run()
``` 
or 
```
SCENARIO_3.run_once()
```

# The Result Object
Whenever a LocustEndpoint makes a request, a _Result_ object is created. Every subsequent request to that LocustEndpoint overwrites the previous Result object.

This Result object holds information about the latest request to it's endpoint and has a few useful attributes as well:

```
LocustEndpoint.Result.success       # Equals True if request is successful
LocustEndpoint.Result.failure       # Equals True if request has failed
LocustEndpoint.Result.status_code   # Equals the status code of the request
LocustEndpoint.Result.response      # Contains the bare response of the request
```

```
LocustEndpoint.Result.json()        # Tries to return the json-formatted response  
```


# Dependency building
The Locust Backpack is a deep one, with many pockets. 

Let's assume we have an endpoint that needs an element from the response of another endpoint. Of course, we could parse the response and assign that specific key/element to the other endpoint, but why go through all that trouble every time?

For example, let's say we have an endpoint ```EventInit``` that needs the key ```'player'``` from another endpoint ```SessionStart```

We can permanently declare this dependency anywhere in the Locust script with the following:

```
EventInit >> DEPENDS_ON('player') >> SessionStart
```

Once this is done, every successful request to ```SessionStart``` will assign it's ```player``` key to ```EventInit```'s body, making ```EventInit``` use it in future requests.


# Other features
Don't think that's all. This backpack is prepared for long journeys.

---
## Sealing and Unsealing

Each LocustEndpoint has sealing and unsealing features which can be activated and deactivated with

```
EventInit.seal
```
```
EventInit.unseal
```

Sealing an endpoint means that the endpoint will be unable to make any further requests until being unsealed.

This does not interfere in any way with the script logic, but once a sealed endpoint request is reached, the request part is skipped and that endpoint's latest Result will be set to a silent fail (not registered anywhere)

There is also a way of sealing and unsealing all LocustEndpoints at once:

```
Backpack.SealAll()
```
```
Backpack.UnsealAll()
```

---
## Check a Request's Success

Aside from using the _Result()_ object to access all information regarding the latest request, including the success with ```EventInit.Result.success```, we can use a simpler and quicker way:

More specifically, we can check for the _truthness_ of a LocustEndpoint instance
```
if EventInit: # Your code
```

In other words, the following two methods have the exact same result:
```
if EventInit.Result.success: # Code
```
```
if EventInit: # Code
```

---
## Mass Assignation

As already mentioned, attributes of a LocustEndpoint can be changed anytime. But what if you want to modify or create a variable for all (or more than one) LocustEndpoints?

This is achieved using _Backpack.SetGlobal()_

|  Argument      |Description                    |Default                      |
|----------------|-------------------------------|-----------------------------|
|**variable (str)**|`the variable that will be modified or created`|`N/A`|
|**value (anything)**|`value of variable`|`N/A`|
|**selective (list)** |`integer representing the runtime(sec) of the scenario`|`All LocustEndpoints`|

Example:

**Setting the same header for all LocustEndpoints**
```
Backpack.SetGlobal('headers', auth_header)
```

**Or just for specific LocustEndpoints**
```
Backpack.SetGlobal('headers', auth_header, selective=[EventInit, TeamInit])
```

---
## Zipping (WIP)

Every unzipped backpack should be zipped back. It would be a pitty to lose anything from it.

To that effect, the Backpack function _Zip()_ was created.

Calling ```Backpack.Zip()``` from anywhere within your current test will save all the test data to a folder within your workspace.

Zip() will:
>* Check if the Locust address "http://localhost:8089/" is accessible
>* Download the Locust .csv files
>* Build a clone of the Locust stats page
>* Use seaborn to plot the test details
>* Nicely save everything to a datestamped folder in your current working directory

> Note! Due to the fact that all zipping operations are done on a localhost URL, _Zip()_ should only be called by the Locust Master



## Flow Chart of a LocustEndpoint Request

```mermaid
graph TB

A(LocustEndpoint) -- Request --> B(TaskSet.client.method)
B -- status_check --> C(Request Result)
C -- request.success --> D(LocustEndpoint.Result)
D --> F(Resolve dependencies)
C -- request.failure --> E(LocustEndpoint.Result)