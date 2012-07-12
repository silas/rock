import argparse
import os
import sys
import ops
from rock.exceptions import Error
from rock.project import Project


def build(args, extra):
    Project(args.path).build()


def run(args, extra):
    Project(args.path).run(' '.join(extra))


def test(args, extra):
    Project(args.path).test()


def main():
    parser = argparse.ArgumentParser(prog='rock',
        description='Rock better runtimes')

    # top-level options
    parser.add_argument('--path', help='project path', default=os.getcwd())

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
        if message.endswith('\n'):
            message = message[:-1]
        ops.exit(1, message)
