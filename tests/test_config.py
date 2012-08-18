import os
import unittest
from rock.config import Config
from rock.exceptions import ConfigError

tests_path = os.path.join(os.path.dirname(__file__))

env_path = os.path.join(tests_path, 'assets', 'env')
project_path = os.path.join(tests_path, 'assets', 'project')
data_path = os.path.join(tests_path, 'assets', 'data')


class ConfigTestCase(unittest.TestCase):

    def setup_test(self, name='simple', mount='test', data='test', config=None):
        Config.MOUNT = os.path.join(env_path, mount)
        Config.DATA = os.path.join(data_path, data)
        self.path = os.path.join(project_path, name)
        if config is None:
            config = {'path': self.path}
        return Config(config)

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
        self.assertEqual(len(c), 8)
        self.assertTrue('build' in c)
        self.assertTrue('build' in iter(c))

    def test_parent(self):
        c = self.setup_test('parent')
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
        c = self.setup_test('parent2')
        with self.assertRaisesRegexp(ConfigError, r'^unable to merge') as a:
            c['test_dict_to_dict']

    def test_simple1(self):
        self.full(self.setup_test())

    def test_simple2(self):
        self.full(self.setup_test(data='test123'))

    def test_runtime_notfound(self):
        c = self.setup_test('runtime_notfound')
        with self.assertRaisesRegexp(ConfigError, r"runtime path doesn't exist") as a:
            c['path']

    def test_runtime_config_notfound(self):
        c = self.setup_test('runtime_config_notfound')
        with self.assertRaisesRegexp(ConfigError, r'not found: .*') as a:
            c['path']

    def test_project_parse(self):
        c = self.setup_test('project_parse')
        with self.assertRaisesRegexp(ConfigError, r'.rock.yml syntax error') as a:
            c['path']

    def test_parse(self):
        c = self.setup_test('parse')
        with self.assertRaisesRegexp(ConfigError, r'parse error: .*') as a:
            c['path']

    def test_badenv1(self):
        c = self.setup_test('badenv1')
        with self.assertRaisesRegexp(ConfigError, r'env must be an associative array of strings') as a:
            c['path']

    def test_badenv2(self):
        c = self.setup_test('badenv2')
        with self.assertRaisesRegexp(ConfigError, r'env must be an associative array of strings') as a:
            c['path']

    def test_nopath(self):
        c = self.setup_test('simple', config={})
        with self.assertRaisesRegexp(ConfigError, r'path is required') as a:
            c['path']
