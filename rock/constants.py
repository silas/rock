from __future__ import unicode_literals

import os

MOUNT_PATH = os.environ.get('ROCK_MOUNT_PATH', '/')

RUNTIMES = ['node', 'perl', 'php', 'python', 'ruby']

SHELL = (os.environ.get('ROCK_SHELL') or '/bin/bash -c').split()
SHELL.insert(1, os.path.basename(SHELL[0]))
