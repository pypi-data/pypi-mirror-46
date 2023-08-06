Podiant features
================

![Build](https://git.steadman.io/podiant/features/badges/master/build.svg)
![Coverage](https://git.steadman.io/podiant/features/badges/master/coverage.svg)

A very simple feature flipper

## Quickstart

Install features:

```sh
pip install podiant-features
```

Add it to your `INSTALLED_APPS`:
```python
INSTALLED_APPS = (
    ...
    'features',
    ...
)
```

## Running tests

Does the code actually work?

```
coverage run --source features runtests.py
```

## Credits

Tools used in rendering this package:

- [Cookiecutter](https://github.com/audreyr/cookiecutter)
- [`cookiecutter-djangopackage`](https://github.com/pydanny/cookiecutter-djangopackage)
