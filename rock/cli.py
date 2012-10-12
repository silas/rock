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


def build(args, extra):
    project(args).build(*extra)


def clean(args, extra):
    project(args).clean(*extra)


def create(args, extra):
    names = project(args).create(args.name, *extra)
    if names:
        stdout.write('%s\n' % '\n'.join(names))


def env(args, extra):
    for name, value in project(args).config['env'].items():
        stdout.write('export %s="%s"\n' % (name, value))


def runtime(args, extra):
    for r in runtime_list():
        stdout.write('%s\n' % r.name)


def platform(args, extra):
    p = project(args)

    if not args.platform:
        if not isinstance(p.config.get('platform'), dict):
            raise ConfigError('platform type required')
        if 'type' not in p.config['platform']:
            raise ConfigError('platform.type required')
        args.platform = p.config['platform']['type']

    try:
        module = importlib.import_module(args.platform)
    except ImportError:
        raise ConfigError('platform not installed: %s' % args.platform)

    if not hasattr(module, 'hook'):
        raise ConfigError("platform module doesn't have a hook function")

    return module.hook('cli', project=project, args=extra)


def run(args, extra):
    project(args).run(extra)


def test(args, extra):
    project(args).test(*extra)


def main(args=None):
    description = """
    rock helps you build, test and run your app in the Rock Platform.
    """

    parser = argparse.ArgumentParser(prog='rock', description=description)

    # general options
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='show run commands')
    parser.add_argument('--dry-run', action='store_true',
                        help="show commands, but don't run")
    parser.add_argument('--version', action='version', version=__version__)

    # options
    project_options = parser.add_argument_group('project')
    project_options.add_argument('--path', help='set path',
                                 default=os.getcwd())
    project_options.add_argument('--env', help='set env',
                                 default=os.environ.get('ROCK_ENV', 'local'))
    project_options.add_argument('--platform', help='set platform',
                                 default=os.environ.get('ROCK_PLATFORM', ''))
    project_options.add_argument('--runtime', help='set runtime')

    # project commands
    sub = parser.add_subparsers(title='commands')

    # build
    parser_build = sub.add_parser('build', help='build project',
                                  add_help=False)
    parser_build.set_defaults(func=build)

    # clean
    parser_clean = sub.add_parser('clean', help='clean project',
                                  add_help=False)
    parser_clean.set_defaults(func=clean)

    # create
    parser_create = sub.add_parser('create', help='create new project')
    parser_create.set_defaults(func=create)
    parser_create.add_argument('name', nargs="?", help='template name')

    # env
    # TODO: remove
    parser_env = sub.add_parser('env', help='show environment variables')
    parser_env.set_defaults(func=env)

    # runtime
    parser_runtime = sub.add_parser('runtime', help='list runtimes',
                                    add_help=False)
    parser_runtime.set_defaults(func=runtime)

    # platform
    parser_platform = sub.add_parser('platform', help='platform commands',
                                     add_help=False)
    parser_platform.set_defaults(func=platform)

    # run
    parser_run = sub.add_parser('run', help='run section or command in ' +
                                'project environment', add_help=False)
    parser_run.set_defaults(func=run)

    # test
    parser_test = sub.add_parser('test', help='test project', add_help=False)
    parser_test.set_defaults(func=test)

    try:
        args, extra = parser.parse_known_args(args)
        args.func(args, extra)
    except Error, error:
        message = '%s' % error
        if not message.endswith('\n'):
            message += '\n'
        parser.exit(1, message)
