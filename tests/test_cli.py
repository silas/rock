import helper
from StringIO import StringIO
from rock import cli, utils
from rock.project import Project


class Args(object):

    def __init__(self):
        self.path = '/tmp/rock123'
        self.verbose = True
        self.dry_run = True
        self.runtime = 'test123'
        self.name = ''


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
        cli.build(Args(), [])
        self.assertTrue('\n\nbuild\n\n' in self.args[4])

    def test_clean(self):
        cli.clean(Args(), [])
        self.assertTrue('\n\nclean\n\n' in self.args[4])

    def test_create(self):
        args = Args()
        args.name = 'test-something'
        cli.create(args, [])
        self.assertTrue('/test-something' in self.args[4])

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

    def test_test(self):
        cli.test(Args(), [])
        self.assertTrue('\n\ntest\n\n' in self.args[4])

    def test_main(self):
        cli.main(args=['runtime'])
        self.assertRaises(SystemExit, cli.main, ['--path=%s/not-found' % helper.TESTS_PATH, 'run', 'ok'])
