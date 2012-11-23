import logging
import ops
import os

root_path = os.path.dirname(os.path.dirname(__file__))

logging.getLogger('ops').addHandler(logging.NullHandler())

def node_hook(self, w):
    self.assertRun('rock run npm shrinkwrap', cwd=w.path)

class RuntimeTests(object):

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
            result = self.assertRun('rock run sample test', cwd=w.path)
            self.assertEquals(result.stdout.rstrip(), '<p>test</p>')
            self.assertRun('rock test', cwd=w.path)
            if hooks.get('post_test'):
                hooks['post_test'](self, w=w)
            self.assertRun('rock clean', cwd=w.path)
            self.assertNotRun('rock test', cwd=w.path)
            self.assertRun('rock build deployment', cwd=w.path)
            self.assertRun('rock test', cwd=w.path)
