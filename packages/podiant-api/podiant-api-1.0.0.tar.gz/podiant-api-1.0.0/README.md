Podiant API
===========

![Build](https://git.steadman.io/podiant/api/badges/master/build.svg)
![Coverage](https://git.steadman.io/podiant/api/badges/master/coverage.svg)
![Documentation](https://readthedocs.org/projects/podiant-api/badge/?version=latest)

A JSON-API framework for Django

## Quickstart

Install API:

```sh
pip install podiant-api
```

Add it to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = (
    ...
    'api',
    ...
)
```

## Documentation

Get full documentation at [podiant-api.readthedocs.io](https://podiant-api.readthedocs.io/en/latest/index.html).

## Running tests

Does the code actually work?

```
coverage run --source api runtests.py
```

## Credits

Tools used in rendering this package:

- [Cookiecutter](https://github.com/audreyr/cookiecutter)
- [`cookiecutter-djangopackage`](https://github.com/pydanny/cookiecutter-djangopackage)
