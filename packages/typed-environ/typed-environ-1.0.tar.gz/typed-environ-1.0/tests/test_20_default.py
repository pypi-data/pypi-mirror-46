from typed_environ import environ


def test_get(tmpenv):
    with tmpenv(X='Y'):
        x = environ.get('X')
        assert x == 'Y'

    x = environ.get('X')
    assert x is None


def test_none(tmpenv):
    with tmpenv(X='Y'):
        x = environ.get('X', type=str)
        assert x == 'Y'

    x = environ.get('X', type=str)
    assert x is None


def test_default(tmpenv):
    with tmpenv(PORT='8001'):
        port = environ.get('PORT', default=8000)
        assert int(port) == 8001

    port = environ.get('PORT', default=8000)
    assert int(port) == 8000


def test_default_int(tmpenv):
    with tmpenv(PORT='8001'):
        port = environ.get('PORT', type=int, default=8000)
        assert port == 8001

    port = environ.get('PORT', type=int, default=8000)
    assert port == 8000


def test_default_list(tmpenv):
    with tmpenv(ALLOWED_HOSTS='localhost,127.0.0.1'):
        allowed_hosts = environ.get('ALLOWED_HOSTS', type=list, default=None)
        assert allowed_hosts == [
            'localhost',
            '127.0.0.1',
        ]

    with tmpenv(ALLOWED_HOSTS=''):
        allowed_hosts = environ.get('ALLOWED_HOSTS', type=list, default=None)
        assert allowed_hosts == []

    allowed_hosts = environ.get('ALLOWED_HOSTS', type=list, default=None)
    assert allowed_hosts is None
