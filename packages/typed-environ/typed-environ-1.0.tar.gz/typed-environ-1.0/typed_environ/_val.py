import json as _json
from distutils.util import strtobool as _strtobool


class Value(str):
    def __bool__(self):
        return bool(_strtobool(self))

    def __nonzero__(self):  # pragma: no cover
        # Python 2
        return self.__bool__()

    def __json(self):
        val = _json.loads(self)
        if isinstance(val, dict):
            return val.items()
        else:
            return val

    def __list(self):
        if len(self) == 0:
            return []
        return self.split(',')

    def __iter__(self):
        try:
            val = self.__json()
        except _json.JSONDecodeError:
            val = self.__list()
        return iter(val)
