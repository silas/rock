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

    class ArgumentParser(argparse.ArgumentParser):

        def format_usage(self):
            text = 'usage: rock [-v] [--env=ENV] [--path=PATH] ' + \
                   '[--runtime=RUNTIME] command\n'
            return text

        def format_help(self):
            text = self.format_usage()
            text += '\n'
            text += '  -h, --help         show help message\n'
            text += '  -v, --verbose      show script while running\n'
            text += '  --dry-run          show script without running\n'
            text += '  --version          show version\n'
            text += '\n'
            text += 'project:\n'
            text += '  --env=ENV          set env (local)\n'
            text += '  --path=PATH        set path\n'
            text += '  --runtime=RUNTIME  set runtime\n'
            text += '\n'
            text += 'commands:\n'
            text += '  build              run build\n'
            text += '  test               run tests\n'
            text += '  run                run in environment\n'
            text += '  clean              clean project files\n'
            text += '\n'
            text += 'other commands:\n'
            text += '  config             show project configuration\n'
            text += '  env                show evaluable environment ' + \
                    'variables\n'
            text += '  runtime            show installed runtimes\n'
            return text

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

    parser = ArgumentParser(prog='rock')
    parser.add_argument('-v', '--verbose', action='store_true')
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
    except Error, error:
        message = '%s' % error
        if not message.endswith('\n'):
            message += '\n'
        parser.exit(1, message)
