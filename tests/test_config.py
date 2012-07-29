import os
import unittest
from rock.config import Config

tests_path = os.path.join(os.path.dirname(__file__))

env_path = os.path.join(tests_path, 'assets', 'env')
project_path = os.path.join(tests_path, 'assets', 'project')
data_path = os.path.join(tests_path, 'assets', 'data')


class ConfigTestCase(unittest.TestCase):

    def setup_test(self):
        Config.MOUNT = os.path.join(env_path, 'test')
        Config.DATA = os.path.join(data_path, 'test')
        self.path = os.path.join(project_path, 'simple')
        return Config({'path': self.path})

    def test_project(self):
        c = self.setup_test().project()
        self.assertEqual(c['path'], self.path)
        self.assertEqual(c['runtime'], 'test123')
        self.assertEqual(c['runtime_type'], 'test')

    def test_full(self):
        c = self.setup_test().full()
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
        # tasks
        self.assertEqual(c['build'].strip(), 'build')
        self.assertEqual(c['build_deployment'].strip(), 'build deployment')
        self.assertEqual(c['clean'].strip(), 'clean')
        self.assertEqual(c['test'].strip(), 'test')
