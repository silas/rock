import argparse
import os
import sys
import ops

class Error(Exception): pass

def command_setup(args):
    if args.runtime is None:
        raise Error('Runtime not found')

def command_build(args):
    ops.env('PATH', '%s/bin' % ops.env('ROCK_PATH', default='/opts/rock'), prepend=True)
    ops.env('PATH', '/opt/rock/runtime/%s/usr/bin' % args.runtime, prepend=True)
    build = ops.run("build-node . deps", cwd=os.getcwd())
    if not build:
        print build.stderr,

def command_env(args):
    print 'export PATH="/opt/rock/runtime/%s/usr/bin:$PATH"' % args.runtime

def main():
    parser = argparse.ArgumentParser(prog='rock', description='Rock better runtimes')

    # top-level options
    parser.add_argument('--runtime', help='manual set runtime')

    # subcommands
    subparsers = parser.add_subparsers(help='subcommands', description='valid subcommands')

    # subcommand: build
    parser_env = subparsers.add_parser('build', help='build project')
    parser_env.set_defaults(func=command_build)

    # subcommand: env
    parser_env = subparsers.add_parser('env', help='output runtime environment variables')
    parser_env.set_defaults(func=command_env)

    try:
        args = parser.parse_args()
        command_setup(args)
        args.func(args)
    except Error, error:
        sys.stderr.write('%s\n' % error)

if __name__ == '__main__':
    main()
