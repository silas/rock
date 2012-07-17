import os
import subprocess
import sys
from rock.exceptions import RunError

class Shell(object):

    def __init__(self, stdin=None, stdout=None, stderr=None):
        self.process = None
        self.code = -1
        self.stdin = sys.stdin if stdin is True else stdin
        self.stdout = stdout
        self.stderr = stderr
        self.data = (None, None)

    def __enter__(self):
        self.process = subprocess.Popen(
            ['/usr/bin/env', 'bash'],
            stdin=subprocess.PIPE,
            stdout=self.stdout,
            stderr=self.stderr,
            shell=False,
            close_fds=True,
        )
        return self 

    def __exit__(self, type, value, traceback):
        self.wait()

    def run(self, command):
        self.process.stdin.write('%s\n' % command)

    def wait(self):
        if self.code < 0:
            if self.stdin and not os.isatty(0):
                for data in self.stdin:
                    self.process.stdin.write(data)
            self.data = self.process.communicate()
            self.code = self.process.returncode
        return self.code
