import helper
import os
import subprocess
import sys
import tempfile
from StringIO import StringIO
from rock import cli, utils
from rock.exceptions import ConfigError
from rock.project import Project

PROJECT_PATH = os.path.join(helper.TESTS_PATH, 'assets', 'project')

class Args(object):

    def __init__(self, **kwargs):
        self.path = os.path.join(PROJECT_PATH, 'simple')
        self.verbose = True
        self.dry_run = True
        self.runtime = 'test123'
        self.name = ''
        self.env = 'local'
        for name, value in kwargs.items():
            setattr(self, name, value)


class CliTestCase(helper.unittest.TestCase):

    def setUp(self):
        helper.setenv()
        def execl(*args):
            self.args = args
        utils.os.execl = execl
        self.stdout = cli.stdout = StringIO()

    def test_project(self):
        self.assertTrue(isinstance(cli.project(Args()), Project))

    def test_env(self):
        cli.env(Args(), [])
        self.assertTrue('\nexport TEST_PATH="test_path"\n' in self.stdout.getvalue())

    def test_runtime(self):
        cli.runtime(Args(), [])
        self.assertTrue('\ntest123\n' in self.stdout.getvalue())

    def test_main(self):
        cli.main(args=['runtime'])
        stderr = sys.stderr
        try:
            sys.stderr = StringIO()
            self.assertRaises(SystemExit, cli.main, ['--path=%s/not-found' % helper.TESTS_PATH, 'run', 'ok'])
        finally:
            sys.stderr = stderr
