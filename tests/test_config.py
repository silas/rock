import helper
import os
from rock.config import Config
from rock.exceptions import ConfigError


class ConfigTestCase(helper.unittest.TestCase):

    def setup(self, name='simple', data='test', config=None, env='local'):
        helper.setenv(data=data)
        self.path = os.path.join(helper.PROJECT_PATH, name)
        self.env = env
        if config is None:
            config = {'path': self.path}
        return Config(config, env=env)

    def full(self, c):
        self.assertEqual(c['path'], self.path)
        self.assertEqual(c['runtime'], 'test123')
        self.assertEqual(c['runtime_type'], 'test')
        # env
        env = c['env']
        self.assertEqual(env['PATH'],
            '%s/bindir:/opt/rock/runtime/test123/usr/bin:${PATH}' %
            self.path)
        self.assertEqual(env['BUILD_PATH'], 'build_path')
        self.assertEqual(env['TEST_PATH'], 'test_path')
        self.assertEqual(env['PROJECT_PATH'], self.path)
        # build with parent
        build = [b for b in c['build'].split('\n') if b]
        self.assertEqual(len(build), 3)
        self.assertEqual(build[0], 'pre')
        self.assertEqual(build[1], 'build')
        self.assertEqual(build[2], 'post')
        # other tasks
        self.assertEqual(c['build_deployment'].strip(), 'build deployment')
        self.assertEqual(c['clean'].strip(), 'clean')
        self.assertEqual(c['test'].strip(), 'test')
        # misc
        self.assertTrue('build' in c)
        self.assertTrue('build' in iter(c))

    def test_paths(self):
        paths = Config.paths('ok')
        self.assertEqual(len(paths), 3)
        self.assertTrue(paths[0].endswith('/user/test/ok'))
        self.assertTrue(paths[1].endswith('/test/etc/rock/ok'))
        self.assertTrue(paths[2].endswith('/data/test/ok'))

    def test_parent(self):
        c = self.setup('parent')
        self.assertEqual(c['test_parent1'], '1')
        self.assertEqual(c['test_parent2'], '2')
        # str to dict
        self.assertEqual(c['test_str_to_str'], 'pre-simple1-post')
        self.assertEqual(c['test_str_to_dict']['one'], 'pre1-simple2-post1')
        self.assertEqual(c['test_str_to_dict']['two'], 'pre2-simple2-post2')
        # dict to dict
        self.assertEqual(c['test_dict_to_dict']['one'], 'pre1-simple1-post1')
        self.assertEqual(c['test_dict_to_dict']['two'], 'pre2--post2')
        self.assertEqual(c['test_dict_to_dict']['three'], 'simple3')
        self.assertEqual(c['test_dict_to_dict']['four'], 'pre4-simple4-post4')

    def test_parent2(self):
        c = self.setup('parent2')
        with self.assertRaisesRegexp(ConfigError, r'^unable to merge') as a:
            c['test_dict_to_dict']

    def test_simple1(self):
        c = self.setup()
        self.full(c)
        self.assertEqual(c['env']['HELLO'], 'world')
        # misc other
        self.assertEqual(len(c), 11)

    def test_simple2(self):
        c = self.setup(data='test123', env='prod')
        self.full(c)
        self.assertEqual(c['env']['HELLO'], 'better world')

    def test_runtime_notfound(self):
        c = self.setup('runtime_notfound')
        with self.assertRaisesRegexp(ConfigError, r"runtime path doesn't exist") as a:
            c['path']

    def test_runtime_config_notfound(self):
        c = self.setup('runtime_config_notfound')
        with self.assertRaisesRegexp(ConfigError, r'not found: .*') as a:
            c['path']

    def test_project_parse(self):
        c = self.setup('project_parse')
        with self.assertRaisesRegexp(ConfigError, r'.rock.yml syntax error') as a:
            c['path']

    def test_parse(self):
        c = self.setup('parse')
        with self.assertRaisesRegexp(ConfigError, r'parse error: .*') as a:
            c['path']

    def test_badenv1(self):
        c = self.setup('badenv1')
        with self.assertRaisesRegexp(ConfigError, r'env must be an associative array') as a:
            c['path']

    def test_badenv2(self):
        c = self.setup('badenv2')
        with self.assertRaisesRegexp(ConfigError, r'env.one must be a string') as a:
            c['path']

    def test_nopath(self):
        c = self.setup('simple', config={})
        with self.assertRaisesRegexp(ConfigError, r'path is required') as a:
            c['path']
