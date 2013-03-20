import argparse
import os
import sys
from rock import __version__
from rock.exceptions import Error
from rock.project import Project
from rock.runtime import list as runtime_list

stdout = sys.stdout


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
    parser = argparse.ArgumentParser(prog='rock config')
    parser.add_argument('--format', help='set output format',
                        choices=['json', 'yaml'], default='yaml')

    sub_args = parser.parse_args(argv)

    config = project(args).config
    config.setup()

    if sub_args.format == 'json':
        import json
        stdout.write(json.dumps(config.data, indent=2))
    else:
        import yaml
        stdout.write(yaml.dump(config.data))


def env(args, argv):
    """
    Output project environment.
    """
    for name, value in project(args).config['env'].items():
        stdout.write('export %s="%s"\n' % (name, value))


def runtime(args, argv):
    """
    List runtimes install on system.
    """
    for r in runtime_list():
        stdout.write('%s\n' % r.name)


def main(argv=None):
    """
    Handle command line arguments.
    """
    description = """
    rock better runtimes.
    """

    if argv is None:
        argv = sys.argv[1:]

    # find command position
    pos, skip_next = 0, False
    for i, arg in enumerate(argv):
        if skip_next:
            skip_next = False
            continue
        elif arg.startswith('--'):
            if arg[2:] in ('env', 'path', 'runtime'):
                skip_next = True
        elif arg.startswith('-'):
            continue
        else:
            pos = i
            break

    parser = argparse.ArgumentParser(prog='rock', description=description)

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

    parser.add_argument('command', help='action to take')

    try:
        # only parse up until command
        args = parser.parse_args(argv[:pos + 1])
        if args.command in ('config', 'env', 'runtime'):
            globals()[args.command](args, argv[pos + 1:])
        else:
            project(args).run(args.command, argv[pos + 1:])
    except Error, error:
        message = '%s' % error
        if not message.endswith('\n'):
            message += '\n'
        parser.exit(1, message)
