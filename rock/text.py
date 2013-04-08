from __future__ import unicode_literals


def _(text):
    return text.strip('\n')

USAGE = _("""
Usage: rock [--help] [--env=ENV] [--path=PATH] [--runtime=RUNTIME] command
""")

HELP = _("""
  --help             show help message
  --verbose          show script while running
  --dry-run          show script without running
  --version          show version

project:
  --env=ENV          set env
  --path=PATH        set path
  --runtime=RUNTIME  set runtime

commands:
  build              run build
  test               run tests
  run                run in environment
  clean              clean project files

other commands:
  config             show project configuration
  env                show evaluable environment variables
  init               generates project skeleton
  runtime            show installed runtimes
""")

CONFIG_USAGE = _("""
Usage: rock config [--format=FORMAT]
""")

CONFIG_HELP = _("""
  --help             show help message
  --format           set output format (json, yaml)
""")

ENV_USAGE = _("""
Usage: rock env
""")

ENV_HELP = _("""
  --help             show help message
""")

RUNTIME_USAGE = _("""
Usage: rock runtime
""")

RUNTIME_HELP = _("""
  --help             show help message
""")
