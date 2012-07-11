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
        config_file = os.path.join(self.path, '.rock.yml')

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

    def run(self, command, **kwargs):
        run_kwargs = {
            'cwd': self.path,
            'stdout': True,
            'stderr': True,
        }
        run_kwargs.update(kwargs)
        return ops.run(command, **run_kwargs)

    def build(self):
        build = self.run(self.config['build'])

        if not build:
            raise BuildError()

    def test(self):
        test = self.run(self.config['test'])

        if not test:
            raise TestError()
