import helper
import os
import subprocess
import sys
import tempfile
from StringIO import StringIO
from rock import cli, utils
from rock.exceptions import ConfigError
from rock.project import Project
from helper import Args


def config_file(name):
    with open(os.path.join(helper.CONFIG_PATH, name)) as f:
        return f.read().strip()


class CliTestCase(helper.unittest.TestCase):

    def setUp(self):
        helper.setenv()
        def execl(*args):
            self.args = args
        utils.os.execl = execl
        self.stdout = cli.stdout = StringIO()

    def test_project(self):
        self.assertTrue(isinstance(cli.project(Args()), Project))

    def test_config_json(self):
        cli.config(Args(), ['--format=json'])
        self.assertEqual(self.stdout.getvalue().strip(), config_file('data.json'))

    def test_config_yaml(self):
        cli.config(Args(), ['--format=yaml'])
        self.assertEqual(self.stdout.getvalue().strip(), config_file('data.yaml'))

    def test_env(self):
        cli.env(Args(), [])
        self.assertTrue('\nexport TEST_PATH="test_path"\n' in self.stdout.getvalue())

    def test_runtime(self):
        cli.runtime(Args(), [])
        self.assertTrue('\ntest123\n' in self.stdout.getvalue())

    def test_main_empty(self):
        stderr = sys.stderr
        try:
            sys.stderr = StringIO()
            self.assertRaises(SystemExit, cli.main, [])
            self.assertTrue('rock better runtimes.' in sys.stderr.getvalue())
        finally:
            sys.stderr = stderr

    def test_main_valid(self):
        cli.main(args=['runtime'])

    def test_main_invalid(self):
        stderr = sys.stderr
        try:
            sys.stderr = StringIO()
            self.assertRaises(SystemExit, cli.main, ['--path=%s/not-found' % helper.TESTS_PATH, 'run', 'ok'])
        finally:
            sys.stderr = stderr
