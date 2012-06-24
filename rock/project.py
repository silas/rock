import yaml
from rock import exceptions
from rock import runtime

class Project(object):

    def __init__(self, path, runtime=None):
        self.path = path
        self.runtime = runtime
        self.parse()

    def parse(self):
        config = {}

        try:
            with open(self.path) as f:
                config = yaml.load(f)
        except Exception, error:
            raise exceptions.ConfigError('Failed to read configuration file: %s' % self.path)

        if not isinstance(config, dict):
            raise exceptions.ConfigError('Invalid project configuration')

        if self.runtime is None:
            runtime_type = config.get('runtime')

            if not isinstance(runtime_type, basestring):
                raise ConfigError('Invalid runtime: %s' % runtime_type)

            self.runtime = runtime.Runtime(runtime_type)

    def build(self):
        self.runtime.env_seutp()
        build = ops.run('rock-build-node ${path} deps', path=self.path, cwd=self.path)
        if not build:
            raise exceptions.Error(build.error.rstrip)
