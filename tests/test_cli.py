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
        self.platform = ''
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

    def test_build(self):
        cli.build(Args(), ['deployment'])
        self.assertTrue('\n\nbuild deployment\n\n' in self.args[3])

    def test_clean(self):
        cli.clean(Args(), [])
        self.assertTrue('\n\nclean\n\n' in self.args[3])

    def test_create(self):
        args = Args()
        args.name = 'test-something'
        path = tempfile.mkdtemp('rock.tests')
        try:
            # ok
            args.path = os.path.join(path, 'one')
            cli.create(args, ['--one', 'one', '--two=two', 'arg'])
            self.assertTrue('/test-something' in self.args[3])
            # bad args
            self.assertRaises(ConfigError, cli.create, args, ['--f:ail=true'])
            # path not empty
            with open(os.path.join(args.path, 'test'), 'w+') as f:
                f.write('test')
            self.assertRaises(ConfigError, cli.create, args, [])
            # path not dir
            args.path = os.path.join(path, 'two')
            with open(args.path, 'w+') as f:
                f.write('test')
            self.assertRaises(ConfigError, cli.create, args, [])
        finally:
            subprocess.check_call(['rm', '-fr', path])

    def test_create_list(self):
        cli.create(Args(), [])
        self.assertEqual(self.stdout.getvalue(), 'test-something\n')

    def test_env(self):
        cli.env(Args(), [])
        self.assertTrue('\nexport TEST_PATH="test_path"\n' in self.stdout.getvalue())

    def test_platform(self):
        self.assertEqual(cli.platform(Args(platform='helper'), []), 'ok')
        # platform not installed
        self.assertRaises(ConfigError, cli.platform, Args(platform='not-exist'), [])
        # platform doesn't have main
        self.assertRaises(ConfigError, cli.platform, Args(platform='empty'), [])
        # no platform
        self.assertRaises(ConfigError, cli.platform, Args(), [])
        # no platform type
        path = os.path.join(PROJECT_PATH, 'platform_type_notfound')
        self.assertRaises(ConfigError, cli.platform, Args(path=path), [])
        # platform from yaml
        path = os.path.join(PROJECT_PATH, 'platform')
        self.assertEqual(cli.platform(Args(path=path), ['1', '2']), '1,2')

    def test_runtime(self):
        cli.runtime(Args(), [])
        self.assertTrue('\ntest123\n' in self.stdout.getvalue())

    def test_run(self):
        cli.run(Args(), ['one', 'two', 'three'])
        self.assertTrue('\none two three\n' in self.args[3])
        # str section
        cli.run(Args(), [])
        self.assertTrue('\necho zero\n' in self.args[3])
        # run section
        cli.run(Args(), ['two'])
        self.assertTrue('\necho two\n' in self.args[3])

    def test_test(self):
        cli.test(Args(), [])
        self.assertTrue('\n\ntest\n\n' in self.args[3])
        # not found
        self.assertRaises(ConfigError, cli.test, Args(), ['not_found'])

    def test_main(self):
        cli.main(args=['runtime'])
        stderr = sys.stderr
        try:
            sys.stderr = StringIO()
            self.assertRaises(SystemExit, cli.main, ['--path=%s/not-found' % helper.TESTS_PATH, 'run', 'ok'])
        finally:
            sys.stderr = stderr
