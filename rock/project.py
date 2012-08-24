import os
import pipes
import string
import sys
import yaml
from rock.config import Config
from rock.exceptions import ConfigError
from rock.process import ProcessManager
from rock.utils import Shell


class Project(object):

    def __init__(self, config):
        self.config = Config(config)

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
            s.write('set -o errexit')
            # switch to project directory
            s.write('cd ' + pipes.quote(self.config['path']))
            # setup environment variables
            if self.config.get('env'):
                # blank line before exports
                s.write('')
                for name, value in self.config['env'].items():
                    s.write('export %s="%s"' % (name, value))
            # blank line before command
            s.write('')
            # run command and wait for results
            if isinstance(command, (list, tuple)):
                s.write(' '.join(command))
            else:
                s.write(command)

    def execute_type(self, name, *args):
        section = '%s_%s' % (name, args[0]) if len(args) > 0 else name
        if section not in self.config:
            raise ConfigError('section not found: %s' % section)
        self.execute(self.config[section])

    def execute_section(self, name):
        section = self.config.get(name)

        if isinstance(section, dict):
            pm = ProcessManager()
            for name, value in section.items():
                pm.add_process(name, '%s run %s' %
                               (sys.argv[0], pipes.quote(value)))
            pm.loop()
        else:
            self.execute(section)

    def build(self, *args):
        self.execute_type('build', *args)

    def clean(self, *args):
        self.execute_type('clean', *args)

    def run(self, args):
        if len(args) == 0 and 'run' in self.config:
            self.execute_section('run')
        elif len(args) == 1 and 'run_%s' % args[0] in self.config:
            self.execute_section('run_%s' % args[0])
        else:
            self.execute(args)

    def test(self, *args):
        self.execute_type('test', *args)
