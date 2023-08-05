from os import environ as _environ

from . import _val


class Environment(object):
    def __getitem__(self, name):
        val = _environ[name]
        return _val.Value(val)

    def get(self, name, default=None, type=None):
        try:
            val = self[name]
            if type is not None:
                val = type(val)
            return val
        except KeyError:
            return default
