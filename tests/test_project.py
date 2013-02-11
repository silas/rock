import helper
from rock import utils
from rock.exceptions import ConfigError


class ProjectTestCase(helper.unittest.TestCase):

    def setUp(self):
        helper.setenv()
        def execl(*args):
            self.args = args
        utils.os.execl = execl
        self.p = helper.project()

    @property
    def script(self):
        return self.args[3].split('\n# script\n', 1)[1].strip()

    def test_run(self):
        self.p.run('run')
        self.assertEqual(self.script, 'echo zero')

    def test_run_manual(self):
        self.p.run('run', ['echo', 'hello'])
        self.assertEqual(self.script, 'echo hello')

    def test_run_no_section(self):
        self.p = helper.project(helper.Args(name='parent'))
        self.assertRaises(ConfigError, self.p.run, 'run')

    def test_build(self):
        self.p.run('build')
        self.assertEqual(self.script, 'pre\n\nbuild\n\npost')

    def test_clean(self):
        self.p.run('clean')
        self.assertEqual(self.script, 'clean')
