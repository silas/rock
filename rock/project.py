import os
import yaml
import ops
from rock.exceptions import ConfigError
from rock.build import Build
from rock.runtime import Runtime
from rock.test import Test


class Project(object):

    def __init__(self, path, parse=True):
        self.path = path
        self.config = {}
        if parse:
            self.parse()

    def parse(self):
        config_file = os.path.join(self.path, 'rock.yml')

        try:
            with open(config_file) as f:
                config = yaml.load(f)
        except Exception, error:
            raise ConfigError('Failed to read configuration file: '
                + config_file)

        if not isinstance(config, dict):
            raise ConfigError('Invalid project configuration')

        runtime_name = config.get('runtime')

        if not isinstance(runtime_name, basestring):
            raise ConfigError('Invalid runtime: %s' % runtime_name)

        build = config.get('build')

        if build is not None and not isinstance(build, basestring):
            raise ConfigError('Invalid build command: %s' % build)

        test = config.get('test')

        if test is not None and not isinstance(test, basestring):
            raise ConfigError('Invalid test command: %s' % test)

        self.config = config

    @property
    def runtime(self):
        if not hasattr(self, '_runtime'):
            self._runtime = Runtime(self.config['runtime'])
        return self._runtime

    @property
    def build(self):
        return Build(self)

    @property
    def test(self):
        return Test(self)
