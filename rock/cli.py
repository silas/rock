import argparse
import os
import sys
import ops
from rock.exceptions import Error
from rock.project import Project


def build(args):
    Project(args.path).build()


def env(args):
    print Project(args.path).runtime.env(render='bash')


def test(args):
    Project(args.path).test()


def run():
    parser = argparse.ArgumentParser(prog='rock',
                                     description='Rock better runtimes')

    # top-level options
    parser.add_argument('--path', help='set project path', default=os.getcwd())

    # subcommands
    subparsers = parser.add_subparsers(help='subcommands',
                                       description='valid subcommands')

    # subcommand: build
    parser_env = subparsers.add_parser('build', help='build project')
    parser_env.set_defaults(func=build)

    # subcommand: env
    parser_env = subparsers.add_parser('env',
        help='output runtime environment variables')
    parser_env.set_defaults(func=env)

    # subcommand: test
    parser_env = subparsers.add_parser('test', help='test project')
    parser_env.set_defaults(func=test)

    try:
        args = parser.parse_args()
        args.func(args)
    except Error, error:
        message = '%s' % error
        if message.endswith('\n'):
            message = message[:-1]
        ops.exit(1, message)
