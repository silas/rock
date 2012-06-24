import os
from rock import exceptions

class Runtime(object):

    def __init__(self, name):
        self.name = name

    @property
    def path(self):
        return '/opt/rock/runtime/%s' % self.name

    @property
    def exists(self):
        if not hasattr(self, '_exists'):
            self._exists = os.path.exists(self.path)
        return self._exists

    def env(self, render=None):
        data = {
            'PATH': ( os.path.join(self.path, 'usr', 'bin'), { 'prepend': True } )
        }
        if render is None:
            return data
        elif render == 'bash':
            text = ''
            for name, value in data.items():
                if value[1].get('prepend'):
                    text += 'export %s="%s:$%s;"\n' % (name, value[0], name)
                elif value[1].get('append'):
                    text += 'export %s="$%s:%s;"\n' % (name, name, value[0])
                else:
                    text += 'export %s="%s";\n' % (name, value[0])
            return text
        else:
            raise Error('Unknown render format')

    def env_setup(self):
        for name, value in self.env():
            ops.env(name, value[0], **value[1])
