import argparse
import os
import sys
import ops
from rock.exceptions import Error
from rock.project import Project


def build(args):
    Project(args.path).build()


def run(args):
    Project(args.path).run()


def test(args):
    Project(args.path).test()


def main():
    parser = argparse.ArgumentParser(prog='rock',
        description='Rock better runtimes')

    # top-level options
    parser.add_argument('--path', help='set project path', default=os.getcwd())

    # subcommands
    subparsers = parser.add_subparsers(help='subcommands',
        description='valid subcommands')

    # subcommand: build
    parser_build = subparsers.add_parser('build', help='build project')
    parser_build.set_defaults(func=build)

    # subcommand: run
    parser_run = subparsers.add_parser('run',
        help='run command in environment')
    parser_run.set_defaults(func=run)

    # subcommand: test
    parser_test = subparsers.add_parser('test', help='test project')
    parser_test.set_defaults(func=test)

    try:
        args = parser.parse_args()
        args.func(args)
    except Error, error:
        message = '%s' % error
        if message.endswith('\n'):
            message = message[:-1]
        ops.exit(1, message)
