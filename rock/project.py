import os
import yaml
import ops
from rock import exceptions
from rock import runtime


class Project(object):

    def __init__(self, path, parse=True):
        self.path = path
        self.runtime = None
        if parse:
            self.parse()

    def parse(self):
        config = {}
        config_file = os.path.join(self.path, 'rock.yml')

        try:
            with open(config_file) as f:
                config = yaml.load(f)
        except Exception, error:
            raise exceptions.ConfigError('Failed to read configuration file: '
                + config_file)

        if not isinstance(config, dict):
            raise exceptions.ConfigError('Invalid project configuration')

        if self.runtime is None:
            runtime_name = config.get('runtime')

            if not isinstance(runtime_name, basestring):
                raise ConfigError('Invalid runtime: %s' % runtime_name)

            self.runtime = runtime.Runtime(runtime_name)

    def build(self):
        self.runtime.env(setup=True)

        build = ops.run('rock-build-${type} ${path}',
            type=self.runtime.type, path=self.path)

        if not build:
            raise exceptions.Error(build.error)
