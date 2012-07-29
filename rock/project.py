import os
import string
import yaml
from rock.config import Config
from rock.utils import Shell
from rock.exceptions import ConfigError


class Project(object):

    def __init__(self, config):
        self.config = Config(config).full()

    def execute(self, command):
        with Shell() as s:
            # declare builtin functions
            s.write('warn() { echo "$@" >&2; }')
            s.write('die() { warn "$@"; exit 1; }')
            # print commands as they're run
            if self.config.get('verbose'):
                s.write('set -o verbose')
            # don't execute commands, just print them
            if self.config.get('dry_run'):
                s.write('set -o noexec')
            # exit with error if any one command fails
            s.write('set -o errexit\n')
            # setup environment variables
            for name, value in self.config['env'].items():
                s.write('export %s="%s"' % (name, value))
            # run command and wait for results
            s.write(command)

    def execute_type(self, name, *args):
        section = '%s_%s' % (name, args[0]) if len(args) > 0 else name
        if section not in self.config:
            raise ConfigError('section not found: %s' % section)
        self.execute(self.config[section])

    def build(self, *args):
        self.execute_type('build', *args)

    def clean(self, *args):
        self.execute_type('clean', *args)

    def run(self, args):
        if len(args) > 0 and 'run_%s' % args[0] in self.config:
            self.execute_type('run', args[0])
        else:
            self.execute(' '.join(args))

    def test(self, *args):
        self.execute_type('test', *args)
