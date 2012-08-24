# Copyright (c) 2012 Nick Stenning, http://whiteink.com/
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Author: Nick Stenning
# Site: https://github.com/nickstenning/honcho
#
# Modifications by Silas Sewell

from __future__ import print_function

import signal
import subprocess
import sys
from Queue import Queue, Empty
from threading import Thread


class Printer(object):
    def __init__(self, output=sys.stdout, name='unknown', width=0):
        self.output = output
        self.name = name
        self.width = width

        self._write_prefix = True

    def write(self, *args, **kwargs):
        new_args = []

        for arg in args:
            lines = arg.split('\n')
            lines = [self._prefix() + l if l else l for l in lines]
            new_args.append('\n'.join(lines))

        self.output.write(*new_args, **kwargs)

    def _prefix(self):
        return '{name} | '.format(name=self.name.ljust(self.width))


class Process(subprocess.Popen):
    """

    A simple utility wrapper around subprocess.Popen that stores
    a number of attributes needed by Honcho.

    """
    def __init__(self, cmd, name=None, *args, **kwargs):
        self.name = name
        self.reader = None
        self.printer = None

        defaults = {
            'stdout': subprocess.PIPE,
            'stderr': subprocess.STDOUT,
            'shell': True,
            'bufsize': 1,
            'close_fds': True
        }
        defaults.update(kwargs)

        super(Process, self).__init__(cmd, *args, **defaults)


class ProcessManager(object):
    """

    Here's where the business happens. The ProcessManager multiplexes and
    pretty-prints the output from a number of Process objects, typically added
    using the add_process() method.

    Example:

        pm = ProcessManager()
        pm.add_process('name', 'ruby server.rb')
        pm.add_process('name', 'python worker.py')

        pm.loop()

    """
    def __init__(self):
        self.processes = []
        self.queue = Queue()
        self.system_printer = Printer(sys.stdout, name='system')

        self._terminating = False

    def add_process(self, name, cmd):
        """

        Add a process to this manager instance:

        Arguments:

        name        - a human-readable identifier for the process
                      (e.g. 'worker'/'server')
        cmd         - the command-line used to run the process
                      (e.g. 'python run.py')

        """
        self.processes.append(Process(cmd, name))

    def loop(self):
        """

        Enter the main loop of the program. This will print the multiplexed
        output of all the processes in this ProcessManager to sys.stdout, and
        will block until all the processes have completed.

        If one process terminates, all the others will be terminated by
        Honcho, and loop() will return.

        """

        self._init_readers()
        self._init_printers()

        for proc in self.processes:
            print("started with pid {0:d}".format(proc.pid), file=proc.printer)

        while self._process_count() > 0:
            try:
                proc, line = self.queue.get(timeout=0.1)
            except Empty:
                pass
            except KeyboardInterrupt:
                print("SIGINT received", file=sys.stderr)
                self.terminate()
            else:
                print(line, end='', file=proc.printer)

                if proc.poll() is not None:
                    print('process terminated', file=proc.printer)
                    self.terminate()

    def terminate(self):
        """

        Terminate all the child processes of this ProcessManager, bringing the
        loop() to an end.

        """
        if self._terminating:
            return False

        self._terminating = True

        print("sending SIGTERM to all processes", file=self.system_printer)
        for proc in self.processes:
            if proc.poll() is None:
                print("sending SIGTERM to pid {0:d}".format(proc.pid),
                      file=self.system_printer)
                proc.terminate()

        def kill(signum, frame):
            # If anything is still alive, SIGKILL it
            for proc in self.processes:
                if proc.poll() is None:
                    print("sending SIGKILL to pid {0:d}".format(proc.pid),
                          file=self.system_printer)
                    proc.kill()

        signal.signal(signal.SIGALRM, kill)
        signal.alarm(5)

    def _process_count(self):
        return [p.poll() for p in self.processes].count(None)

    def _init_readers(self):
        for proc in self.processes:
            t = Thread(target=_enqueue_output, args=(proc, self.queue))
            t.daemon = True  # thread dies with the program
            t.start()

    def _init_printers(self):
        width = max(len(p.name) for p in self.processes)
        width = max(width, len(self.system_printer.name))

        self.system_printer.width = width

        for proc in self.processes:
            proc.printer = Printer(sys.stdout,
                                   name=proc.name,
                                   width=width)


def _enqueue_output(proc, queue):
    for line in iter(proc.stdout.readline, b''):
        if not line.endswith('\n'):
            line += '\n'
        queue.put((proc, line))
    proc.stdout.close()
