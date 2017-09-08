from .import Mongua

class Users(Mongua):

    __fields__ = Mongua.__fields__ + [
        ('username', str, ''),
        ('name', str, ''),
        ('last_active',str, '')
    ]

    # def to_json(self):
    #     d = dict()
    #     for k in self.__fields__:
    #         key = k[0]
    #         if not key.startswith('_'):
    #             d[key] = getattr(self, key)
    #     return json.dumps(d)
    #
    # @classmethod
    # def from_json(cls, j):
    #     d = json.loads(j)
    #     instance = cls()
    #     for k, v in d.items():
    #         setattr(instance, k, v)
    #     return instance







