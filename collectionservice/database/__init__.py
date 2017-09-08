import time
import copy
import json
from pymongo import MongoClient

mongua = MongoClient(host="mongodbservice",port=27017,connect=False)


def next_id(name):
    query = {
        'name': name,
    }
    update = {
        '$inc': {
            'seq': 1
        }
    }
    kwargs = {
        'query': query,
        'update': update,
        'upsert': True,
        'new': True,
    }
    doc = mongua.db['data_id']
    new_id = doc.find_and_modify(**kwargs).get('seq')
    return new_id


class Mongua(object):
    __fields__ = [
        '_id',
        ('id', int, -1),
        ('type', str, ''),
        ('deleted', bool, False),
        ('created_time', int, 0),
        ('updated_time', int, 0),
    ]

    def blacklist(self):
        b = [
            '_id',
        ]
        return b

    def json(self):
        _dict = self.__dict__
        d = {k: v for k, v in _dict.items() if k not in self.blacklist()}
        return d

    @classmethod
    def new(cls, form=None, **kwargs):
        name = cls.__name__
        m = cls()
        fields = copy.deepcopy(cls.__fields__)
        fields.remove('_id')
        if form is None:
            form = {}
        for f in fields:
            k, t, v = f
            if k in form:
                setattr(m, k, t(form[k]))
            else:
                setattr(m, k, v)
        for k, v in kwargs.items():
            if hasattr(m, k):
                setattr(m, k, v)
            else:
                raise KeyError
        m.id = next_id(name)
        ts = int(time.time())
        m.created_time = ts
        m.updated_time = ts
        m.type = name.lower()
        m.save()
        return m

    def save(self):
        name = self.__class__.__name__
        mongua.db[name].save(self.__dict__)

    @classmethod
    def delete(cls, id):
        name = cls.__name__
        query = {
            'id': id
        }
        mongua.db[name].remove(query)

    @classmethod
    def all(cls):
        return cls._find()

    @classmethod
    def _find(cls, **kwargs):
        name = cls.__name__
        flag_sort = '__sort'
        sort = kwargs.pop(flag_sort, None)
        ds = mongua.db[name].find(kwargs)
        if sort is not None:
            ds = ds.sort(sort)
        l = [cls._new_with_bson(d) for d in ds]
        return l

    @classmethod
    def _new_with_bson(cls, bson):
        m = cls()
        fields = copy.deepcopy(cls.__fields__)
        fields.remove('_id')
        for f in fields:
            k, t, v = f
            if k in bson:
                setattr(m, k, bson[k])
            else:
                setattr(m, k, v)
        setattr(m, '_id', bson['_id'])
        m.type = cls.__name__.lower()
        return m

    @classmethod
    def find_by(cls, **kwargs):
        return cls.find_one(**kwargs)

    @classmethod
    def find_one(cls, **kwargs):
        l = cls._find(**kwargs)
        if len(l) > 0:
            return l[0]
        else:
            return None

    @classmethod
    def clean(cls):
        name = cls.__name__
        mongua.db[name].remove()

