import argparse
import os
import sys
import ops

def setup(args):
    if args.runtime is None:
        raise Error('Runtime not found')

def build(args):
    ops.env('PATH', '/opt/rock/runtime/%s/usr/bin' % args.runtime, prepend=True)
    build = ops.run('rock-build-node . deps', cwd=os.getcwd())
    if not build:
        print build.stderr,

def env(args):
    print 'export PATH="/opt/rock/runtime/%s/usr/bin:$PATH"' % args.runtime

def main():
    parser = argparse.ArgumentParser(prog='rock', description='Rock better runtimes')

    # top-level options
    parser.add_argument('--path', help='set project path', default=os.getcwd())

    # subcommands
    subparsers = parser.add_subparsers(help='subcommands', description='valid subcommands')

    # subcommand: build
    parser_env = subparsers.add_parser('build', help='build project')
    parser_env.set_defaults(func=build)

    # subcommand: env
    parser_env = subparsers.add_parser('env', help='output runtime environment variables')
    parser_env.set_defaults(func=env)

    try:
        args = parser.parse_args()
        setup(args)
        args.func(args)
    except Error, error:
        sys.stderr.write('%s\n' % error)
