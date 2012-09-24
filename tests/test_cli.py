import helper
import os
import subprocess
import tempfile
from StringIO import StringIO
from rock import cli, utils
from rock.exceptions import ConfigError
from rock.project import Project


class Args(object):

    def __init__(self):
        self.path = os.path.join(helper.TESTS_PATH, 'assets', 'project', 'simple')
        self.verbose = True
        self.dry_run = True
        self.runtime = 'test123'
        self.name = ''
        self.env = 'local'


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
        self.assertTrue('\n\nbuild deployment\n\n' in self.args[4])

    def test_clean(self):
        cli.clean(Args(), [])
        self.assertTrue('\n\nclean\n\n' in self.args[4])

    def test_create(self):
        args = Args()
        args.name = 'test-something'
        path = tempfile.mkdtemp('rock.tests')
        try:
            # ok
            args.path = os.path.join(path, 'one')
            cli.create(args, ['--one', 'one', '--two=two', 'arg'])
            self.assertTrue('/test-something' in self.args[4])
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

    def test_runtime(self):
        cli.runtime(Args(), [])
        self.assertTrue('\ntest123\n' in self.stdout.getvalue())

    def test_run(self):
        cli.run(Args(), ['one', 'two', 'three'])
        self.assertTrue('\none two three\n' in self.args[4])
        # str section
        cli.run(Args(), [])
        self.assertTrue('\necho zero\n' in self.args[4])
        # dict section
        cli.run(Args(), ['full'])

    def test_test(self):
        cli.test(Args(), [])
        self.assertTrue('\n\ntest\n\n' in self.args[4])
        # not found
        self.assertRaises(ConfigError, cli.test, Args(), ['not_found'])

    def test_main(self):
        cli.main(args=['runtime'])
        self.assertRaises(SystemExit, cli.main, ['--path=%s/not-found' % helper.TESTS_PATH, 'run', 'ok'])
