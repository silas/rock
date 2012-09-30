import os
import pipes
import re
import string
import sys
import yaml
from rock.config import Config
from rock.exceptions import ConfigError
from rock.process import ProcessManager
from rock.utils import Shell

NAME_RE = re.compile('^[a-zA-Z_]+$')


class Project(object):

    def __init__(self, *args, **kwargs):
        self.config = Config(*args, **kwargs)

    def _setup(self, shell):
        # declare builtin functions
        shell.write('warn() { echo "$@" >&2; }')
        shell.write('die() { warn "$@"; exit 1; }')
        # print commands as they're run
        if self.config.get('verbose'):
            shell.write('set -o verbose')
        # don't execute commands, just print them
        if self.config.get('dry_run'):
            shell.write('set -o noexec')
        # exit with error if any one command fails
        shell.write('set -o errexit')
        # switch to project directory
        shell.write('cd ' + pipes.quote(self.config['path']))
        # setup environment variables
        if self.config.get('env'):
            # blank line before exports
            shell.write('')
            for name, value in self.config['env'].items():
                shell.write('export %s="%s"' % (name, value))
        # blank line before command
        shell.write('')

    def execute(self, command):
        with Shell() as shell:
            self._setup(shell)
            # run command and wait for results
            if isinstance(command, (list, tuple)):
                shell.write(' '.join(command))
            else:
                shell.write(command)

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

    def _template(self, path, args):
        with Shell() as shell:
            self._setup(shell)
            # handle options
            length = len(args)
            skip_next = False
            template_args = []
            for i in xrange(length):
                if skip_next:
                    skip_next = False
                    continue
                arg = args[i]
                if arg.startswith('--'):
                    name, value = arg[2:], '1'
                    if '=' in name:
                        name, value = name.split('=', 1)
                    elif (i + 1 < length and not args[i + 1].startswith('--')):
                        value = args[i + 1]
                        skip_next = True
                    name = name.upper().replace('-', '_')
                    if NAME_RE.match(name):
                        # write options to shell
                        shell.write('export ROCK_%s="%s"' %
                                    (name, pipes.quote(value)))
                    else:
                        raise ConfigError('invalid argument: ' + arg)
                else:
                    template_args.append(arg)
            shell.write('. ' + path)

    def create(self, name=None, *args):
        if not self.config._setup:
            self.config._setup = True
        # project path
        path = self.config['path']
        # if name is given try to run it, otherwise list available templates
        if name:
            # create project path if it doesn't exist
            if not os.path.exists(path):
                os.makedirs(path)
            # ensure its a directory
            if not os.path.isdir(path):
                raise ConfigError('path must be a directory')
            # ensure its empty
            if os.listdir(path):
                raise ConfigError('directory is not empty')
            # search for template and run if it exists
            for template_path in self.config.paths('template'):
                template_path = os.path.join(template_path, name)
                if os.path.isfile(template_path):
                    # run template
                    self._template(template_path, args)
        else:
            templates = set()
            # get paths
            for path in self.config.paths('template'):
                if not os.path.isdir(path):
                    continue
                for template in os.listdir(path):
                    if os.path.isfile(os.path.join(path, template)):
                        templates.add(template)
            templates = list(templates)
            templates.sort()
            return templates

    def run(self, args):
        if len(args) == 0 and 'run' in self.config:
            self.execute_section('run')
        elif len(args) == 1 and 'run_%s' % args[0] in self.config:
            self.execute_section('run_%s' % args[0])
        else:
            self.execute(args)

    def test(self, *args):
        self.execute_type('test', *args)
