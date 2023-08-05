[![PyPI version](https://badge.fury.io/py/BlueDB.svg)](https://badge.fury.io/py/BlueDB)
[![GitHub version](https://badge.fury.io/gh/Enderdas%2FBluedb.svg)](https://badge.fury.io/gh/Enderdas%2FBluedb)
# BlueDB
*use my database, is good!*

```python
>>> from BlueDB import Blue
>>> database = Blue('database')
>>> database['key'] = {'nested key': 'nested value'}
>>> print(database['key']['nested key'])
nested value

>>> database['key']['nested key'] = 'new value'
>>> print(database)
{'key': {'nested key': 'new value'}}

```

`py -m pip install BlueDB` to install it then import `Blue` class and you're good to go!


### Blue2

> [Blue2](BlueDB/blue2.py) ~ A BlueDB subset

Blue2 uses JSON to make it faster and more human readable. Blue2 also sticks with the same framework and design as the original BlueDB.
```python
>>> from BlueDB.blue2 import Blue
>>> database = Blue('database')
>>> database['key'] = {'nested key': 'nested value'}
#same functions and features as BlueDB...but more JSON!!!
>>> print(database['key']['nested key'])
nested value
#WOW very JSON!!!
>>> database['key']['nested key'] = 'new value'
>>> print(database)
{'key': {'nested key': 'new value'}}

```

*Blue2 can use Builtin JSON, UltraJSON or RapidJSON*

### Blue3

> [Blue3](BlueDB/blue3.py) ~ A BlueDB superset

```python
>>> from BlueDB.blue3 import Blue
>>> database = Blue('database')
>>> database['key'] = {'nested key': 'nested value'}
>>> database2 = Blue('database')
>>> print(database); print(database2)
{'key': {'nested key': 'nested value'}} #database
{'key': {'nested key': 'nested value'}} #database2

>>> database['key']['nested key'] = 'new value'
>>> print(database); print(database2)
{'key': {'nested key': 'new value'}} #database
{'key': {'nested key': 'new value'}} #database2

```

*Blue3 can also use Builtin JSON, UltraJSON or RapidJSON*

##### How is it different?

What makes Blue3 different from both the original BlueDB and Blue2 is Blue3 has a special feature which lets you open and run multiple versions of the same database and have fluent consistent data flow across all of them. Meaning when you edit data in one version of the database it will automatically update that information into every other version.

##### How is it faster?

Blue3 uses JSON, in-memory caches and memory monitoring to incrementally dump data from in-memory to disk, making key setting and getting faster and more efficient. The same principal is used in the library [Chest](ttps://github.com/mrocklin/chest) from which I got the idea to spill to disk.

##### Is this the best version of BlueDB?

Currently yes. Will it be the best overall? no, BlueDB will have better and faster versions in the future. All of my any or up and coming work can be seen in [Indev](BlueDB/indev)
