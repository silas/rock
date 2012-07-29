import StringIO
import os


class Shell(object):

    def __enter__(self):
        self.stdin = StringIO.StringIO()
        return self

    def __exit__(self, type, value, traceback):
        os.execl('/usr/bin/env', 'bash', 'bash', '-c', self.stdin.getvalue())

    def write(self, text):
        self.stdin.write(text + '\n')
