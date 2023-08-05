import json

from typed_environ import environ


def test_json_list(tmpenv):
    with tmpenv(DATA_LIST='[1, "x"]'):
        data = list(environ['DATA_LIST'])
        assert data == [
            1,
            'x',
        ]


def test_json(tmpenv):
    data0 = {
        'DEBUG': True,
        'ALLOWED_HOSTS': [
            '127.0.0.1',
            'localhost',
        ],
    }
    with tmpenv(DATA=json.dumps(data0)):
        data = dict(environ['DATA'])
        assert data == data0
