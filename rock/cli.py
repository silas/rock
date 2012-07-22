import argparse
import os
import sys
from rock.exceptions import Error
from rock.project import Project


def project(args):
    config = {'path': args.path}
    if args.verbose:
        config['verbose'] = True
    if args.dry_run:
        config['dry_run'] = True
        config['verbose'] = True
    if args.runtime:
        config['runtime'] = args.runtime
    return Project(config)


def build(args, extra):
    project(args).build(*extra)


def clean(args, extra):
    project(args).clean(*extra)


def env(args, extra):
    for name, value in project(args).config['env'].items():
        print 'export %s="%s"' % (name, value)


def run(args, extra):
    project(args).run(extra)


def test(args, extra):
    project(args).test(*extra)


def main():
    description = """
    rock helps you build, test and run your app in the Rock Platform.
    """

    parser = argparse.ArgumentParser(prog='rock', description=description)

    # general options
    parser.add_argument('--dry-run', action='store_true',
        help="show commands, but don't run")
    parser.add_argument('--verbose', action='store_true',
        help='show run commands')

    # project options
    project_options = parser.add_argument_group('project options')
    project_options.add_argument('--path', help='set path',
        default=os.getcwd())
    project_options.add_argument('--runtime', help='set runtime')

    # project commands
    project = parser.add_subparsers(title='project')

    # project: build
    parser_build = project.add_parser('build', help='build project')
    parser_build.set_defaults(func=build)

    # project: clean
    parser_clean = project.add_parser('clean', help='clean project')
    parser_clean.set_defaults(func=clean)

    # project: env
    parser_env = project.add_parser('env', help='show environment variables')
    parser_env.set_defaults(func=env)

    # project: run
    parser_run = project.add_parser('run',
        help='run project file', add_help=False)
    parser_run.set_defaults(func=run)

    # project: test
    parser_test = project.add_parser('test', help='test project')
    parser_test.set_defaults(func=test)

    try:
        args, extra = parser.parse_known_args()
        args.func(args, extra)
    except Error, error:
        message = '%s' % error
        if not message.endswith('\n'):
            message += '\n'
        parser.exit(1, message)
