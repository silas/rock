import os
import yaml
import ops
from rock.exceptions import *


class Project(object):

    def __init__(self, path, setup=True):
        self.path = path
        self.config = {}
        if setup:
            self.setup()

    def setup(self):
        config_file = os.path.join(self.path, 'rock.yml')

        try:
            with open(config_file) as f:
                config = yaml.load(f)
        except Exception, error:
            raise ConfigError('Failed to read configuration file: '
                + config_file)

        if not isinstance(config, dict):
            raise ConfigError('Invalid project configuration')

        runtime = config.get('runtime')

        if not isinstance(runtime, basestring):
            raise ConfigError('Invalid runtime: %s' % runtime)

        config['runtime_path'] = '/opt/rock/runtime/%s' % runtime

        config['type'] = runtime.rstrip('0123456789')

        build = config.get('build')

        if build is None:
            config['build'] = 'rock-build-%s' % config['type']
        elif not isinstance(build, basestring):
            raise ConfigError('Invalid build command: %s' % build)

        test = config.get('test')

        if test is None:
            config['test'] = 'rock-test-%s' % config['type']
        elif not isinstance(test, basestring):
            raise ConfigError('Invalid test command: %s' % test)

        self.config = config

    def env(self, render=None, setup=False):
        data = {
            'PATH': (os.path.join(self.config['runtime_path'], 'usr', 'bin'),
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
            raise EnvError('Unknown render format')

    def build(self):
        self.env(setup=True)

        build = ops.run(self.config['build'], cwd=self.path, stdout=True,
             stderr=True)

        if not build:
            raise BuildError(build.stderr.strip())

        return build.stdout.strip()

    def test(self):
        self.env(setup=True)

        test = ops.run(self.config['test'], cwd=self.path, stdout=True,
            stderr=True)

        if not test:
            raise TestError(test.stdout)
