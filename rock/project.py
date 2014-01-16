from __future__ import unicode_literals

import os
import pipes
import re
from rock.config import Config
from rock.exceptions import ConfigError
from rock.utils import Shell, isstr

NAME_RE = re.compile('^[a-zA-Z0-9_]+$')


class Project(object):

    def __init__(self, *args, **kwargs):
        self.config = Config(*args, **kwargs)

    def run(self, section, argv=None):
        argv, args, opts, opts_list = argv or [], [], {}, []
        script = self.config.get(section, '')

        # ensure section exists
        def check():
            if section not in self.config:
                raise ConfigError('section not found: %s' % section)
            if not isstr(self.config[section]):
                raise ConfigError('section must be a string: %s' % section)

        # handle run special case
        if section == 'run':
            if not argv:
                check()
            else:
                script = ' '.join(map(pipes.quote, argv))
        else:
            check()
        # build bash script
        with Shell() as shell:
            # print commands as they're run
            if self.config.get('verbose'):
                shell.write('set -o verbose')
            # declare builtin functions
            shell.write('warn() { echo "$@" >&2; }')
            shell.write('die() { warn "$@"; exit 1; }')
            # don't execute commands, just print them
            if self.config.get('dry_run'):
                shell.write('set -o noexec')
            # exit with error if any one command fails
            shell.write('set -o errexit')
            # switch to project directory
            if section != 'run' or len(argv) == 0:
                shell.write('cd ' + pipes.quote(self.config['path']))
            # setup environment variables
            if self.config.get('env'):
                # blank line before exports
                for name, value in self.config['env'].items():
                    shell.write('export %s="%s"' % (name, value))
            # handle arguments
            if section != 'run':
                # raw arguments
                shell.write('export ROCK_ARGV=%s' %
                            pipes.quote(' '.join(argv)))
                for i, arg in enumerate(argv, 1):
                    shell.write('ARGV[%s]=%s' % (i, pipes.quote(arg)))
                # parse arguments
                for arg in argv:
                    if arg.startswith('--'):
                        name, value = arg[2:], 'true'
                        if '=' in name:
                            name, value = name.split('=', 1)
                        name = name.upper().replace('-', '_')
                        if NAME_RE.match(name):
                            opts[name] = value
                            if name in opts_list:
                                opts_list.remove(name)
                            opts_list.append(name)
                    else:
                        args.append(arg)
                # parsed arguments
                shell.write('export ROCK_ARGS=%s' %
                            pipes.quote(' '.join(args)))
                for i, arg in enumerate(args, 1):
                    shell.write('ARGS[%s]=%s' % (i, pipes.quote(arg)))
                # set zero argument to command
                args.insert(0, section)
                # positional arguments
                for i, arg in enumerate(args):
                    shell.write('export ROCK_ARG%s=%s' % (i, pipes.quote(arg)))
                # parsed argument options
                for name, value in opts.items():
                    shell.write('export ROCK_ARGS_%s=%s' %
                                (name, pipes.quote(value)))
                # parsed options
                shell.write('export ROCK_OPTS=%s' %
                            pipes.quote(' '.join(opts_list)))
                shell.write('export ROCK_CWD=%s' % pipes.quote(os.getcwd()))
            # execute script
            shell.write('# script')
            shell.write(script)
