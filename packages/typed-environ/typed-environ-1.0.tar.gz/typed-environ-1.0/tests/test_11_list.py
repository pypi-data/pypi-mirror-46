from typed_environ import environ


def test_list(tmpenv):
    with tmpenv(ALLOWED_HOSTS='localhost,127.0.0.1'):
        allowed_hosts = list(environ['ALLOWED_HOSTS'])
        assert allowed_hosts == [
            'localhost',
            '127.0.0.1',
        ]


def test_empty_list(tmpenv):
    with tmpenv(ALLOWED_HOSTS=''):
        allowed_hosts = list(environ['ALLOWED_HOSTS'])
        assert allowed_hosts == []
