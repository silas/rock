from __future__ import unicode_literals

import os
try:
    from io import StringIO
except ImportError:  # pragma: no cover
    from StringIO import StringIO
from rock import constants
from rock.exceptions import ConfigError


def isexecutable(path):
    return os.path.isfile(path) and os.access(path, os.X_OK)


try:
    basestring

    def isstr(s):
        return isinstance(s, basestring)
except NameError:  # pragma: no cover
    def isstr(s):
        return isinstance(s, str)


def raw(text):
    return text.replace('\\', '\\\\')


class Shell(object):

    def __init__(self):
        self.stdin = StringIO()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.run()

    def run(self):
        if not isexecutable(constants.SHELL[0]):
            raise ConfigError('invalid ROCK_SHELL: %s' % constants.SHELL)
        os.execl(*(constants.SHELL + [self.stdin.getvalue()]))

    def write(self, text):
        self.stdin.write(text + '\n')
