from collections import abc
from keyword import iskeyword


class FrozenJson:
    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if iskeyword(key):
                key += "_"
            elif str(key).isnumeric():
                key = "_" + key
            self.__data[key] = value

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return FrozenJson.build(self.__data[name])

    def __repr__(self):
        return "FrozenJson(%r)" % (self.__data)

    @classmethod
    def build(cls, obj):

        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj
