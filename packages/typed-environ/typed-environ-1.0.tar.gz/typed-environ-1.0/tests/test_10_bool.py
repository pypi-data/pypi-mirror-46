from typed_environ import environ


def test_bool(tmpenv):
    with tmpenv(DEBUG='True', HTTPS='0'):
        assert bool(environ['DEBUG']) is True
        assert bool(environ['HTTPS']) is False
