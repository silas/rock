import logging
import os
from unittest import *

import ops
from nose.tools import nottest
try:
    from unittest2 import *
except:
    pass

root_path = os.path.dirname(os.path.dirname(__file__))

try:
    logging.getLogger('ops').addHandler(logging.NullHandler())
except:
    pass

class RuntimeTests(TestCase):

    create_lock = None

    def assertRun(self, *args, **kwargs):
        kwargs['combine'] = True
        r = ops.run(*args, **kwargs)
        self.assertTrue(r, '\n\n' + r.stdout + '\n\n' + r.stderr)
        return r

    def assertNotRun(self, *args, **kwargs):
        kwargs['combine'] = True
        r = ops.run(*args, **kwargs)
        self.assertFalse(r, '\n\n' + r.stdout + '\n\n' + r.stderr)
        return r

    def workspace(self):
        ns = 'rock.test.runtime.{name}-'.format(name=self.name)
        return ops.workspace(prefix=ns)

    def project_path(self):
        root = self.name.rstrip('0123456789')
        return os.path.join(root_path, 'assets', root)

    def test_full(self):
        root = self.name.rstrip('0123456789')

        with self.workspace() as w:
            self.assertRun('rock --runtime=%s init' % self.name, cwd=w.path)
            with open(w.join('.rock.yml')) as f:
                self.assertEqual(f.read(), 'runtime: %s\n' % self.name)
            for name in self.init_files:
                self.assertTrue(os.path.isfile(w.join(name)), 'found file %s' % name)
            for name in self.init_directories:
                p = w.join(name)
                self.assertTrue(os.path.isdir(p), 'found directory %s' % name)
                ops.run('rmdir ${path}', path=p)
            ops.run('cp -r ${src_path}/* ${dst_path}',
                src_path=self.project_path(), dst_path=w.path)
            for command in ('build', 'test', 'clean'):
                r = self.assertRun('rock %s --help' % command, cwd=w.path)
                match = 'Usage: rock %s' % command
                self.assertEqual(r.stdout.split('\n')[0].strip()[0:len(match)], match)
            self.assertRun('rock build', cwd=w.path)
            result = self.assertRun('rock run sample test', cwd=w.path)
            self.assertEquals(result.stdout.rstrip(), '<p>test</p>')
            self.assertRun('rock test', cwd=w.path)
            if self.create_lock:
                self.assertRun(self.create_lock, cwd=w.path)
            self.assertRun('rock clean', cwd=w.path)
            self.assertNotRun('rock test', cwd=w.path)
            self.assertRun('rock build --deployment', cwd=w.path)
            self.assertRun('rock test', cwd=w.path)
