import os
import unittest
import ops

root_path = os.path.dirname(os.path.dirname(__file__))

def node_hook(self, w):
    self.assertRun('rock run npm shrinkwrap', cwd=w.path)

class RuntimeTestCase(unittest.TestCase):

    def assertRun(self, *args, **kwargs):
        kwargs['combine'] = True
        r = ops.run(*args, **kwargs)
        self.assertTrue(r, '\n\n' + r.stdout)

    def assertNotRun(self, *args, **kwargs):
        kwargs['combine'] = True
        r = ops.run(*args, **kwargs)
        self.assertFalse(r, '\n\n' + r.stdout)

    def runtime(self, name, **hooks):
        root = name.rstrip('0123456789')
        ns = 'rock.test.runtime.{name}-'.format(name=name)

        project_path = os.path.join(root_path, 'assets', root)

        with ops.workspace(prefix=ns) as w:
            ops.run('cp -r ${src_path}/* ${dst_path}', src_path=project_path,
                dst_path=w.path)
            with open(w.join('.rock.yml'), 'w+') as f:
                f.write('runtime: {name}'.format(name=name))
            self.assertRun('rock build', cwd=w.path)
            self.assertRun('rock test', cwd=w.path)
            if hooks.get('post_test'):
                hooks['post_test'](self, w=w)
            self.assertRun('rock clean', cwd=w.path)
            self.assertNotRun('rock test', cwd=w.path)
            self.assertRun('rock build deployment', cwd=w.path)
            self.assertRun('rock test', cwd=w.path)

    def test_node04(self):
        self.runtime('node04')

    def test_node06(self):
        self.runtime('node06', post_test=node_hook)

    def test_node08(self):
        self.runtime('node08', post_test=node_hook)

    def test_perl516(self):
        self.runtime('perl516')

    def test_php54(self):
        self.runtime('php54')

    def test_python27(self):
        self.runtime('python27')

    def test_ruby18(self):
        self.runtime('ruby18')

    def test_ruby19(self):
        self.runtime('ruby19')
