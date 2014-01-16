from __future__ import unicode_literals

import argparse
import locale
import os
import sys
from rock import __version__
from rock.exceptions import Error
from rock.project import Project
from rock.runtime import list as runtime_list
from rock.text import *


def argument_parser(*args, **kwargs):
    format_usage = kwargs.pop('format_usage', None)
    format_help = kwargs.pop('format_help', None)

    class ArgumentParser(argparse.ArgumentParser):

        def format_usage(self):
            return '%s\n' % format_usage

        def format_help(self):
            return '%s\n%s\n' % (self.format_usage(), format_help)

    kwargs['add_help'] = False

    p = ArgumentParser(*args, **kwargs)
    p.add_argument('--help', action='help')

    return p


def project(args):
    """
    Create and return project instance using cli arguments.
    """
    config = {'path': args.path}
    if args.verbose:
        config['verbose'] = True
    if args.dry_run:
        config['dry_run'] = True
        config['verbose'] = True
    if args.runtime:
        config['runtime'] = args.runtime
    return Project(config, env=args.env)


def config(args, argv):
    """
    Output project configuration (json, yaml).
    """
    parser = argument_parser(prog='rock config', format_usage=CONFIG_USAGE,
                             format_help=CONFIG_HELP)
    parser.add_argument('--format', choices=['json', 'yaml'], default='yaml')

    sub_args = parser.parse_args(argv)

    config = project(args).config
    config.setup()

    if sub_args.format == 'json':
        import json
        sys.stdout.write(u'' + json.dumps(config.data, indent=2))
    else:
        import yaml
        yaml.safe_dump(config.data, stream=sys.stdout, encoding=None)


def env(args, argv):
    """
    Output project environment.
    """
    parser = argument_parser(prog='rock env', format_usage=ENV_USAGE,
                             format_help=ENV_HELP)

    sub_args = parser.parse_args(argv)

    for name, value in project(args).config['env'].items():
        sys.stdout.write('export %s="%s"\n' % (name, value))


def runtime(args, argv):
    """
    List runtimes install on system.
    """
    parser = argument_parser(prog='rock runtime', format_usage=RUNTIME_USAGE,
                             format_help=RUNTIME_HELP)

    sub_args = parser.parse_args(argv)

    for r in runtime_list():
        sys.stdout.write('%s\n' % r.name)


def main(argv=None):
    """
    Handle command line arguments.
    """

    if argv is None:
        argv = sys.argv[1:]
        encoding = locale.getdefaultlocale()[1]
        if encoding:
            argv = [a.decode(encoding) for a in sys.argv[1:]]

    # find command position
    pos, skip_next = 0, False
    for i, arg in enumerate(argv):
        if skip_next:
            skip_next = False
            continue
        elif arg.startswith('--'):
            if arg[2:] in ('env', 'path', 'runtime'):
                skip_next = True
        else:
            pos = i
            break

    parser = argument_parser(prog='rock', format_usage=USAGE, format_help=HELP)
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--env', default=os.environ.get('ROCK_ENV', 'local'))
    parser.add_argument('--path', default=os.environ.get('ROCK_PATH', ''))
    parser.add_argument('--runtime', default=os.environ.get('ROCK_RUNTIME'))
    parser.add_argument('command')

    try:
        # only parse up until command
        args = parser.parse_args(argv[:pos + 1])
        if args.command in ('config', 'env', 'runtime'):
            globals()[args.command](args, argv[pos + 1:])
        else:
            project(args).run(args.command, argv[pos + 1:])
    except Error as error:
        message = '%s' % error
        if not message.endswith('\n'):
            message += '\n'
        parser.exit(1, message)
