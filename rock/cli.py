import argparse
import importlib
import os
import sys
from rock import __version__
from rock.exceptions import ConfigError, Error
from rock.project import Project
from rock.runtime import list as runtime_list

stdout = sys.stdout


def project(args):
    config = {'path': args.path}
    if args.verbose:
        config['verbose'] = True
    if args.dry_run:
        config['dry_run'] = True
        config['verbose'] = True
    if args.runtime:
        config['runtime'] = args.runtime
    return Project(config, env=args.env)


def config(args, extra):
    parser = argparse.ArgumentParser(prog='rock config')
    parser.add_argument('--format', help='set output format',
                        choices=['json', 'yaml'], default='yaml')

    sub_args = parser.parse_args(extra)

    config = project(args).config
    config.setup()

    if sub_args.format == 'json':
        import json
        stdout.write(json.dumps(config.data, indent=2))
    else:
        import yaml
        stdout.write(yaml.dump(config.data))


def env(args, extra):
    for name, value in project(args).config['env'].items():
        stdout.write('export %s="%s"\n' % (name, value))


def runtime(args, extra):
    for r in runtime_list():
        stdout.write('%s\n' % r.name)


def main(args=None):
    description = """
    rock better runtimes.
    """

    add_help = True

    for arg in sys.argv[1:]:
        if not arg.startswith('-'):
            add_help = False
            break

    parser = argparse.ArgumentParser(prog='rock', description=description,
                                     add_help=add_help)

    # general options
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='show run commands')
    parser.add_argument('--dry-run', action='store_true',
                        help="show commands, but don't run")
    parser.add_argument('--version', action='version', version=__version__)

    # options
    options = parser.add_argument_group('project')
    options.add_argument('--path', help='set path',
                         default=os.environ.get('ROCK_PATH', ''))
    options.add_argument('--env', help='set env',
                         default=os.environ.get('ROCK_ENV', 'local'))
    options.add_argument('--runtime', help='set runtime')

    parser.add_argument('command', nargs='?', help='action to take')

    try:
        args, extra = parser.parse_known_args(args)
        if args.command in ('config', 'env', 'runtime'):
            globals()[args.command](args, extra)
        elif args.command:
            project(args).run(args.command, extra)
        else:
            parser.print_usage(file=sys.stderr)
            parser.exit(1)
    except Error, error:
        message = '%s' % error
        if not message.endswith('\n'):
            message += '\n'
        parser.exit(1, message)
