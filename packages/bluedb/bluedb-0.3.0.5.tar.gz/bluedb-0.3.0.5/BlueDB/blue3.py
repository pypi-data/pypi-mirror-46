import sys
from collections import MutableMapping, MutableSequence
try:
    import ujson as json
except:
    try:
        import rapidjson as json
    except:
        import json

def _check_file(name):
    try:
        with open(name, 'r') as fp:
            return True
    except:
        return False

def _load_type(key, value, previous):
    if type(value) == type(dict()):
        return _BlueDict(key, value, previous)
    elif type(value) == type(list()):
        return _BlueList(key, value, previous)
    else:
        return value

def _check_size(item):
    return sys.getsizeof(item)

MAX_SIZE = 1e5

class BlueDatabase(MutableMapping):

    def __init__(self, name, has_copy = False):
        self.has_copy = has_copy
        self.name = name
        self.filename = self.name+'.blu3'
        self.cache = {}

        if _check_file(self.filename) is False:
            with open(self.filename, 'w') as fp:
                json.dump({}, fp)

    def _get_all(self):
        with open(self.filename, 'r') as fp:
            data = json.load(fp)
            data.update(self.cache)
        return data

    def _delitem__(self, key):
        try:
            del self.cache[key]
        except:
            with open(self.filename, 'r') as fp:
                data = json.load(fp)
            del data[key]
            with open(self.filename, 'w') as fp:
                json.dump(data, fp)

    def __getitem__(self, key):
        try:
            return self.cache[key]
        except:
            with open(self.filename, 'r') as fp:
                data = json.load(fp)
            return _load_type(key, data[key], self)

    def _setitem__(self, key, value):
        if _check_size(self.cache) >= MAX_SIZE:
            with open(self.filename, 'r') as fp:
                data = json.load(fp)
            while _check_size(self.cache) > MAX_SIZE:
                item = self.cache.popitem()
                data[item[0]] = item[1]
            with open(self.filename, 'w') as fp:
                json.dump(data, fp)
        else:
            self.cache[key] = _load_type(key, value, self)

    def _push(self):
        with open(self.filename, 'r') as fp:
            data = dict(json.load(fp))
        for k, v in self.cache.items():
            try:
                data[k] = dict(v.get_all())
            except:
                data[k] = v
        with open(self.filename, 'w') as fp:
            json.dump(data, fp)

    def __repr__(self):
        return str(self._get_all())

    def __len__(self):
        return len(self._get_all())

    def __iter__(self):
        return iter(self._get_all())

PENDING = []
RUNNING = []

class Blue(BlueDatabase):

    def __init__(self, name):
        """
        BlueDB
        THIS IS NOT THE BASE CLASS
        THIS IS A SUBCLASS RUNNING OFF THE PARENT OF `BlueDatabase`
        for i in Blue.PENDING:
            if i.name == name:
                i._push()
                i.has_copy = True
                Blue.PENDING.remove(i)
                Blue.RUNNING.append(i)
                super().__init__(name, has_copy = True)
            else:
                super().__init__(name, has_copy = False)
        Blue.RUNNING.append(self)
        """
        dbs = [i.name for i in PENDING]
        if name in dbs:
            totals = []
            for db in PENDING:
                if db.name == name:
                    totals.append(db)
            for db in totals:
                db._push()
                db.has_copy = True
                PENDING.remove(db)
            super().__init__(name, has_copy = True)
        else:
            dbs = [i.name for i in RUNNING]
            if name in dbs:
                super().__init__(name, has_copy = True)
            else:
                super().__init__(name, has_copy = False)
        RUNNING.append(self)

    def __setitem__(self, key, value):
        if self not in PENDING:
            PENDING.append(self)
        self._setitem__(key, value)
        if self.has_copy:
            self.push()

    def __delitem__(self, key):
        if self not in PENDING:
            PENDING.append(self)
        self._delitem__(key)
        if self.has_copy:
            self.push()

    def __del__(self):
        self.push()

    def push(self):
        PENDING.remove(self)
        self._push()

class _BlueDict(MutableMapping):

    def __init__(self, key, value, previous):
        self.name = key
        self.previous = previous
        self.body = {}

        for key in value.keys():
            self.body[key] = _load_type(key, value[key], self)

    def __delitem__(self, key):
        del self.body[key]
        self.previous.__setitem__(self.name, self.name)

    def __getitem__(self, key):
        return self.previous.__getitem__(self.name)[key]

    def __setitem__(self, key, value):
        self.body[key] = _load_type(key, value, self)
        self.previous.__setitem__(self.name, self)

    def get_all(self):
        new = {}
        for key in self.body.keys():
            try:
                new[key] = self.body[key].get_all()
            except:
                new[key] = self.body[key]
        return new

    def __str__(self):
        return str(self.body)

    def __repr__(self):
        return str(self.body)

    def __len__(self):
        return len(self.body)

    def __iter__(self):
        return iter(self.body)

class _BlueList(MutableSequence):

    def __init__(self, key, value, previous):
        super().__init__()
        self.name = key
        self.body = []
        self.previous = previous
        for i in range(len(value)):
            self.body.append(_load_type(i, value[i], self))

    def __delitem__(self, index):
        del self.body[index]
        self.previous.__setitem__(self.name, self)

    def __getitem__(self, index):
        return self.previous.__getitem__(self.name)[index]

    def __setitem__(self, index, value):
        self.body[index] = _load_type(index, value, previous)
        self.previous.__setitem__(self.name, self)

    def get_all():
        new = []
        for i in self.body:
            try:
                new.append(i.get_all())
            except:
                new.append(i)
        return new

    def __len__(self):
        return len(self.body)

    def __repr__(self):
        return str(self.body)

    def insert(self, index, value):
        self.body[index] = _load_type(index, value, previous)
        self.previous.__setitem__(self.name, self)
