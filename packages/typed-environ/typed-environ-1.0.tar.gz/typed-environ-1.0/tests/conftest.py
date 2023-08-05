from os import environ

import pytest


class TmpEnv(object):
    def __init__(self, name, val):
        self.name = name
        self.val = val
        self.orig = None

    def __enter__(self):
        self.orig = environ.get(self.name)
        environ[self.name] = self.val

    def __exit__(self, *args, **kwargs):
        if self.orig is None:
            del environ[self.name]
        else:
            environ[self.name] = self.orig


class TmpEnvList(object):
    def __init__(self, **kwargs):
        self.list = [
            TmpEnv(k, v)
            for k, v in kwargs.items()
        ]

    def __enter__(self):
        for item in self.list:
            item.__enter__()

    def __exit__(self, *args, **kwargs):
        for item in self.list:
            item.__exit__(*args, **kwargs)


@pytest.fixture
def tmpenv():
    return TmpEnvList
