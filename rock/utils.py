import StringIO
import os
from rock.exceptions import ConfigError


ROCK_SHELL = os.environ.get('ROCK_SHELL', '/bin/bash -l -c').split()


class Shell(object):

    def __init__(self):
        self.stdin = StringIO.StringIO()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.run()

    def run(self):
        if not os.path.isfile(ROCK_SHELL[0]) or not os.access(ROCK_SHELL[0], os.X_OK):
            raise ConfigError('invalid ROCK_SHELL: %s' % ROCK_SHELL)
        os.execl(*(ROCK_SHELL + [self.stdin.getvalue()]))

    def write(self, text):
        self.stdin.write(text + '\n')
