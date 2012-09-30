import argparse
import os
import sys
from rock import __version__
from rock.exceptions import Error
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
    parser.add_argument('--dry-run', action='store_true',
                        help="show commands, but don't run")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='show run commands')
    parser.add_argument('--version', action='version', version=__version__)

    # project options
    project_options = parser.add_argument_group('project options')
    project_options.add_argument('--path', help='set path',
                                 default=os.getcwd())
    project_options.add_argument('--env', help='set env',
                                 default=os.environ.get('ROCK_ENV', 'local'))
    project_options.add_argument('--runtime', help='set runtime')

    # project commands
    project = parser.add_subparsers(title='project')

    # project: build
    parser_build = project.add_parser('build', help='build project')
    parser_build.set_defaults(func=build)

    # project: clean
    parser_clean = project.add_parser('clean', help='clean project')
    parser_clean.set_defaults(func=clean)

    # project: create
    parser_create = project.add_parser('create', help='create project')
    parser_create.set_defaults(func=create)
    parser_create.add_argument('name', nargs="?", help='template name')

    # project: env
    parser_env = project.add_parser('env', help='show environment variables')
    parser_env.set_defaults(func=env)

    # runtime
    parser_runtime = project.add_parser('runtime', help='list runtimes',
                                        add_help=False)
    parser_runtime.set_defaults(func=runtime)

    # project: run
    parser_run = project.add_parser('run', help='run project file',
                                    add_help=False)
    parser_run.set_defaults(func=run)

    # project: test
    parser_test = project.add_parser('test', help='test project')
    parser_test.set_defaults(func=test)

    try:
        args, extra = parser.parse_known_args(args)
        args.func(args, extra)
    except Error, error:
        message = '%s' % error
        if not message.endswith('\n'):
            message += '\n'
        parser.exit(1, message)
