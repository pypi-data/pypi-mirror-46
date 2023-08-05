# brain-plasma
Sharing data between callbacks, on Apache Plasma. Built for Dash, useful anywhere. Only supported on Mac/Linux for now.

---

`brain-plasma` is a high-level wrapper for the Apache Plasma PlasmaClient API with an added object naming, reference, and changing system.

### Key Features

1. Create and reference named shared-memory Python objects
2. Change the value of those shared-memory Python objects
3. Thread-safe: it doesn't matter if the processes or threads sharing the `Brain` object share memory or not; the namespace is only stored in Plasma and checked each time any object is referenced.
4. Store large objects, especially Pandas and NumPy objects, in the backend
5. Access those objects very quickly - faster than Parquet. Pulling ~10,000,000 row Pandas object takes about .45 seconds, storing it takes about 1 second. Instantaneous for most objects of reasonable size, including Pandas up to ~200,000 rows.

**Current Drawbacks**

4. (3.) above slows the `Brain` down, minutely...but it makes it safe for programs that don't share memory. This only becomes a problem if there are thousands of variables that need to be parsed each time, but even then it's still a small fraction of a second.
6. Limited to Arrow-serializable objects.

### Basic Usage

Basic idea: the brain has a list of names that it has "learned" that are attached to objects in Plasma. Bracket notation can be used as a shortcut of the `learn` and `recall` methods.

```
$ pip install pyarrow
$ pip install brain-plasma
$ plasma_store -m 50000000 -s /tmp/plasma & disown
```

```
from brain_plasma import Brain
brain = Brain(start_process=True)

this = 'a text object'
that = [1,2,3,4]
those = pd.DataFrame(dict(this=[1,2,3,4],that=[4,5,6,7]))

brain['that'] = that # recommended
brain.learn(this,'this') # underlying API
brain.learn(those,'those')

brain['this'] # recommended
> 'a text object'

brain.recall('that') # underlying API
> [1,2,3,4]

type(brain.recall('those'))
> pandas.core.frame.DataFrame

brain.forget('this')
brain.recall('this')
> # error, that name/object no longer exists

brain.names()
> ['that','those']
```

### API Reference for `brain_plasma.Brain`

**Initialization**

`brain = Brain(path="/tmp/plasma", start_process=False, size=50000000)`

Parameters:

* `path` - which path to use to start and/or connect to the plasma store
* `start_process` - whether or not to start a new process at that path. Kills existing process if it exists.
* `size` - number of bytes that the plasma_store can use

**Attributes**

`Brain.client`

The underlying PlasmaClient instance. Created at instantiation. Requires plasma_store to be running locally.

`Brain.path`

The path to the PlasmaClient connection folder. Default is `/tmp/plasma` but can be changed by using `brain = Brain(path='/my/new/path')`

`Brain.size`

int - number of bytes available in the plasma_store, e.g. `50000000`

`Brain.mb`

str - number of mb available, e.g. `'50 MB'`

NOTE: brain.size and brain.mb ARE NOT ACCURATE if:
a. you have used `brain.start()` without specifying the size. 
b. you specify size in `brain = Brain()` but do not specify `start_process=True`

**Methods**

`Brain.__setitem__` and `Brain.__getitem__` i.e. 'bracket notation' or `brain['name']`

Shortcuts for `Brain.learn` and `Brain.recall`

`Brain.learn(thing, name, description=False)`

Store object `thing` in Plasma, reference later with `name`

`Brain.recall(name)`

Get the value of the object with name `name` from Plasma

`Brain.info(name)`

Get the metadata associated with the object with name `name`

`Brain.forget(name)`

Delete the object in Plasma with name `name` as well as the index object

`Brain.names()`

Get a list of all objects that `Brain` knows the name of (all names in the `Brain` namespace)

`Brain.ids()`

Get a list of all the plasma.ObjectIDs that brain knows the name of

`Brain.knowledge()`

Get a list of all the "brain object" index objects used as a reference: name (variable name), name_id (bytes of the ObjectID for the index object) d(bytes of ObjectID for the value), description (False if not assigned)

`Brain.sleep()`

Disconnect `Brain.client` from Plasma. Must use `Brain.wake_up()` to use the `Brain` again.

`Brain.wake_up()`

Reconnect `Brain.client` to Plasma.

`Brain.start(path=None,size=None)`

Restarts the `plasma_store` process for a dead `Brain`. NOTE: DOES NOT RESTART AN EXISTING PLASMA_STORE AT THAT PATH.

`Brain.dead(i_am_sure=False)`

If i_am_sure==True, disconnect `Brain.client` and kill the `plasma_store` process with `$ pkill plasma_store`

---

### Notes and TODO

Apache PlasmaClient API reference: https://arrow.apache.org/docs/python/generated/pyarrow.plasma.PlasmaClient.html#pyarrow.plasma.PlasmaClient

Apache Plasma docs: https://arrow.apache.org/docs/python/plasma.html#

**TODO**

* multiple assignment
  * this is actually very easy, as the underlying PlasmaClient API already supports this.
* multiple namespaces
  * i.e. `brain` and `brain_` can be in the same shared memory space without sharing a namespace
  * `brain = Brain(namespace='app1')` changes the "names" prefix to some custom thing
- [x] launch the `plasma_store` from a `Brain` instance
  - ~~I built this using `subprocess` but it won't run in the background.~~~ rebuilt using `os.system` and it works fine
* do special things optimizing the PlasmaClient interactions with NumPy and Pandas objects
* change the size of the `plasma_store` but maintain current namespace(s)
* ability to persist items on disk and recall them with the same API
* specify in docs which objects cannot be used due to serialization constraints
* ability to dump all/specific objects and name reference to a standard disk location
  * plus ability to recover these changes later - maybe make it standard behaviour to check the standard location


---

Made with :heart: by Russell Romney in Madison, WI. Thanks for the help from @tcbegley
