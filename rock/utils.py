from __future__ import unicode_literals

import os
try:
    from io import StringIO
except ImportError:  # pragma: no cover
    from StringIO import StringIO
from rock.exceptions import ConfigError

ROCK_SHELL = (os.environ.get('ROCK_SHELL') or '/bin/bash -c').split()
ROCK_SHELL.insert(1, os.path.basename(ROCK_SHELL[0]))


def isexecutable(path):
    return os.path.isfile(path) and os.access(path, os.X_OK)


try:
    basestring

    def isstr(s):
        return isinstance(s, basestring)
except NameError:  # pragma: no cover
    def isstr(s):
        return isinstance(s, str)


class Shell(object):

    def __init__(self):
        self.stdin = StringIO()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.run()

    def run(self):
        if not isexecutable(ROCK_SHELL[0]):
            raise ConfigError('invalid ROCK_SHELL: %s' % ROCK_SHELL)
        os.execl(*(ROCK_SHELL + [self.stdin.getvalue()]))

    def write(self, text):
        self.stdin.write(text + '\n')
