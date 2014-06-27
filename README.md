# Rock [![Build Status](https://api.travis-ci.org/rockstack/rock.png?branch=master)](http://travis-ci.org/rockstack/rock)

This is a command line tool that simplifies creating, building, testing, and
running applications.

## Test

``` console
$ virtualenv venv
$ . venv/bin/activate
$ pip install .
$ pip install coverage pep8 nose
$ nosetests && pep8 rock --show-source --show-pep8
```

## License

This work is licensed under the MIT License (see the LICENSE file).

## Icon

The [icon][icon] was created by [Anuar Zhumaev][icon-author] ([CC BY 3.0][icon-license]).

[icon]: http://thenounproject.com/term/rock/5846/
[icon-author]: http://thenounproject.com/yxorama/
[icon-license]: https://creativecommons.org/licenses/by/3.0/us/
