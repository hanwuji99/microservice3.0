from .import Mongua
import json
# import redis
import time
class Cache(object):
    def get(self, key):
        pass

    def set(self, key, value):
        pass

# class RedisCache(Cache):
#     redis_db = redis.StrictRedis(host='redisservice', port=6379, db=0)
#
#     def set(self, key, value):
#         return self.redis_db.set(key, value)
#
#     def get(self, key):
#         return self.redis_db.get(key)

class Collections(Mongua):

    __fields__ = Mongua.__fields__ + [
        ('username', str, ''),
        ('date', str, ''),
        ('movieid', str, ''),
    ]

    def to_json(self):
        d = dict()
        for k in self.__fields__:
            key = k[0]
            if not key.startswith('_'):
                d[key] = getattr(self, key)
        return json.dumps(d)

    @classmethod
    def from_json(cls, j):
        d = json.loads(j)
        instance = cls()
        for k, v in d.items():
            setattr(instance, k, v)
        return instance

    @classmethod
    def all_delay(cls):
        time.sleep(3)
        return cls.all()

    should_update_all = True
    # redis_cache = RedisCache()

    # @classmethod
    # def cache_all(cls):
    #     #  redis cache
    #     if cls.should_update_all:
    #         cls.redis_cache.set('Collections_all', json.dumps([i.to_json() for i in cls.all_delay()]))
    #         cls.should_update_all = False
    #     try:
    #         j = json.loads(cls.redis_cache.get('Collections_all'))
    #         j = [cls.from_json(i) for i in j]
    #         return j
    #     except Exception as e:
    #         print e



