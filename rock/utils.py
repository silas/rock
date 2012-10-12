import StringIO
import os


class Shell(object):

    def __init__(self):
        self.stdin = StringIO.StringIO()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.run()

    def run(self):
        os.execl('/bin/bash', '-l', '-c', self.stdin.getvalue())

    def write(self, text):
        self.stdin.write(text + '\n')
