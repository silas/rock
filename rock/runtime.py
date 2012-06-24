import os
import ops
from rock import exceptions


class Runtime(object):

    def __init__(self, name):
        self.name = name
        self.type = name.rstrip('0123456789')

    @property
    def path(self):
        return '/opt/rock/runtime/%s' % self.name

    @property
    def exists(self):
        return os.path.exists(self.path)

    def env(self, render=None, setup=False):
        data = {
            'PATH': (os.path.join(self.path, 'usr', 'bin'),
                {'prepend': True})
        }
        if setup:
            for name, value in data.items():
                ops.env(name, value[0], **value[1])
        if render is None:
            return data
        elif render in ['bash', 'sh']:
            text = []
            for name, value in data.items():
                if value[1].get('prepend'):
                    text.append('export %s="%s:$%s";' % (name, value[0], name))
                elif value[1].get('append'):
                    text.append('export %s="$%s:%s";' % (name, name, value[0]))
                else:
                    text.append('export %s="%s";' % (name, value[0]))
            return '\n'.join(text)
        else:
            raise Error('Unknown render format')
