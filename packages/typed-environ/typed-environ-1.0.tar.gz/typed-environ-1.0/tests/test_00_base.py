import pytest

from typed_environ import environ


def test_getitem(tmpenv):
    with tmpenv(X='Y'):
        x = environ['X']
        assert isinstance(x, str)
        assert x == 'Y'


def test_keyerror():
    with pytest.raises(KeyError):
        x = environ['X']


def test_str(tmpenv):
    with tmpenv(X='Y'):
        x = environ['X']
        assert isinstance(x, str)
        assert type(x) != str
        assert type(str(x)) == str  # should be str if explicitly cast
