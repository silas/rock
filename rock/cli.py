import argparse
import os
import sys
from rock.exceptions import Error
from rock.project import Project

def project(args):
    return Project(args.path, config={ 'dry_run': args.dry_run })


def build(args, extra):
    project(args).build()


def clean(args, extra):
    project(args).clean()


def env(args, extra):
    for name, value in project(args).config['env'].items():
        print 'export %s="%s"' % (name, value)


def run(args, extra):
    project(args).run(' '.join(extra))


def setup(args, extra):
    project(args).setup()


def test(args, extra):
    project(args).test()


def tool(args, extra):
    project(args).tool(' '.join(extra))


def main():
    parser = argparse.ArgumentParser(prog='rock',
        description='Rock better runtimes')

    # top-level options
    parser.add_argument('--path', help='project path', default=os.getcwd())
    parser.add_argument('--dry-run', action='store_true', help="display but don't run commands")

    # project commands
    project = parser.add_subparsers(title='project')

    # project: build
    parser_build = project.add_parser('build', help='build project')
    parser_build.set_defaults(func=build)

    # project: clean
    parser_clean = project.add_parser('clean', help='clean project')
    parser_clean.set_defaults(func=clean)

    # project: env
    parser_env = project.add_parser('env', help='display environment variables')
    parser_env.set_defaults(func=env)

    # project: run
    parser_run = project.add_parser('run',
        help='run project file', add_help=False)
    parser_run.set_defaults(func=run)

    # project: setup
    parser_setup = project.add_parser('setup', help='setup project')
    parser_setup.set_defaults(func=setup)

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
