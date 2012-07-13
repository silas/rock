import argparse
import os
import sys
from rock.exceptions import Error
from rock.project import Project

def project(args):
    return Project(args.path, config={
        'verbose': args.verbose,
    })


def build(args, extra):
    project(args).build()


def run(args, extra):
    project(args).run(' '.join(extra))


def test(args, extra):
    project(args).test()


def main():
    parser = argparse.ArgumentParser(prog='rock',
        description='Rock better runtimes')

    # top-level options
    parser.add_argument('--path', help='project path', default=os.getcwd())
    parser.add_argument('-v', '--verbose', action='store_true', help='show all output')

    # subcommands
    subparsers = parser.add_subparsers(title='subcommands')

    # subcommand: build
    parser_build = subparsers.add_parser('build', help='build project')
    parser_build.set_defaults(func=build)

    # subcommand: run
    parser_run = subparsers.add_parser('run',
        help='run command', add_help=False)
    parser_run.set_defaults(func=run)

    # subcommand: test
    parser_test = subparsers.add_parser('test', help='test project')
    parser_test.set_defaults(func=test)

    try:
        args, extra = parser.parse_known_args()
        args.func(args, extra)
    except Error, error:
        message = '%s' % error
        if not message.endswith('\n'):
            message += '\n'
        parser.exit(1, message)
