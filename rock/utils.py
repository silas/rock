import subprocess
from rock.exceptions import RunError

class Shell(object):

    def __init__(self, shell='/usr/bin/bash', stdout=None, stderr=None):
        self.process = None
        self.shell = shell
        self.code = -1
        self.stdout = subprocess.PIPE if stdout is None else stdout
        self.stderr = subprocess.STDOUT if stderr is None else stderr
        self.data = (None, None)

    def __enter__(self):
        self.process = subprocess.Popen(
            self.shell,
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
            self.process.stdin.flush()
            self.data = self.process.communicate()
            self.code = self.process.returncode
        return self.code
