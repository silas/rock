from __future__ import unicode_literals

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
    def split(self):
        return self.args[3].split('\n# script\n', 1)

    @property
    def script(self):
        return self.split[1].strip()

    def test_arg(self):
        self.p.run('clean', ['--six', '--zero', 'one', '--two=2', 'three', 'four', '--five=five', '--six'])
        data = {}
        for value in self.split[0].split('\n'):
            if not value.startswith('export '):
                continue
            name = value.split(' ', 1)[1]
            if '=' not in name:
                continue
            data[name.split('=', 1)[0]] = value
        self.assertEqual(data.get('ROCK_ENV'), 'export ROCK_ENV="local"')
        self.assertEqual(data.get('ROCK_ARGV'), "export ROCK_ARGV='--six --zero one --two=2 three four --five=five --six'")
        self.assertEqual(data.get('ROCK_ARGS'), "export ROCK_ARGS='one three four'")
        self.assertEqual(data.get('ROCK_ARG0'), "export ROCK_ARG0=clean")
        self.assertEqual(data.get('ROCK_OPTS'), "export ROCK_OPTS='ZERO TWO FIVE SIX'")

    def test_run(self):
        self.p.run('run')
        self.assertEqual(self.script, 'echo zero')

    def test_run_manual(self):
        self.p.run('run', ['echo', 'hello'])
        self.assertEqual(self.script, 'echo hello')

    def test_run_no_section(self):
        self.p = helper.project(helper.Args(name='parent'))
        self.assertRaises(ConfigError, self.p.run, 'run')

    def test_run_section_not_string(self):
        self.p = helper.project(helper.Args(name='parent'))
        self.assertRaises(ConfigError, self.p.run, 'test_str_to_dict')

    def test_build(self):
        self.p.run('build')
        self.assertEqual(self.script, 'pre\n\nbuild\n\npost')

    def test_clean(self):
        self.p.run('clean')
        self.assertEqual(self.script, 'clean')
