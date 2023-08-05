# typed-environ

[![Build Status](https://travis-ci.com/MichaelKim0407/typed-environ.svg?branch=master)](https://travis-ci.com/MichaelKim0407/typed-environ)
[![Coverage Status](https://coveralls.io/repos/github/MichaelKim0407/typed-environ/badge.svg?branch=master)](https://coveralls.io/github/MichaelKim0407/typed-environ?branch=master)

Environment variables with type support.

## Usage

```python
from typed_environ import environ
```

* `int` value without default

    ```python
    port = int(environ['PORT'])
    ```

* `int` value with default

    ```python
    port = environ.get('PORT', type=int, default=8000)
    ```

* `bool` value without default

    ```python
    debug = bool(environ['DEBUG'])
    ```

    [Accepted values](https://docs.python.org/3/distutils/apiref.html#distutils.util.strtobool).

    **Note**:
    The return value of `environ['DEBUG']` is not simply a `str`,
    since `bool` cast for a `str` only checks if the string is empty.
    Similarly, casting the result into `list` or `dict` (see below) works
    differently from casting on a string.
    The return value can still be used as a string normally
    (excluding `bool` and `iter` calls).
    To avoid complications on `str` values,
    explicitly call `str(environ['xxx'])`,
    or use `os.environ` instead.

* `bool` value with default

    ```python
    debug = environ.get('DEBUG', type=bool, default=False)
    ```

* `list`

    ```python
    allowed_hosts = environ.get('ALLOWED_HOSTS', type=list)
    ```

    Split the string by `','`.

    **Note 1**:
    If the value is an empty string, returns `[]` instead of `['']`.

    **Note 2**:
    `default` here is `None`. It does not have to be a value of `type`.

* json

    ```python
    data_list = list(environ['DATA_LIST'])
    data = dict(environ['DATA'])
    ```

    Load the environment variable from a json-formatted string,
    which can be a `list` or a `dict`.

    **Note**:
    When calling `iter`
    (and `list`, `dict`, `tuple`, `set`, etc. by extension),
    json-decoding will be attempted first,
    and then comma-splitting as specified above.

## Installation

```bash
pip install typed-environ
```
