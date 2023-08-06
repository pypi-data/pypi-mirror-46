# ci

[![PyPI Version](https://img.shields.io/pypi/v/ci.svg?style=flat-square&colorB=4c1)][pypi]
[![Build Status](https://img.shields.io/travis/rossmacarthur/python-ci/master.svg?style=flat-square)][travis]
[![Code Coverage](https://img.shields.io/codecov/c/github/rossmacarthur/python-ci.svg?style=flat-square)][codecov]

Easily run common CI tasks for Python builds.

## Getting started

Install this package with

```bash
pip install ci
```

## Example usage

Here are some examples of how you would use the `ci` tool.

Run `flake8` on Python 2.7 only
```
ci --skip 2.7 flake8
```

Run `pip install codecov` on Python 3.x.x only
```
ci --only 3 pip install codecov
```

Run `codecov` on Python 3.7.2 only
```
ci --only 3.7.2 codecov
```

If for some reason you are running a command that takes the same options as this
tool then you can use two dashes `--` to specify that this tool should no longer
match options:
```
ci --only 3 -- git --version
```

## License

This project is licensed under the MIT License. See the [LICENSE] file.

[LICENSE]: LICENSE
[pypi]: https://pypi.org/project/ci/
[travis]: https://travis-ci.org/rossmacarthur/python-ci
[codecov]: https://codecov.io/gh/rossmacarthur/python-ci
