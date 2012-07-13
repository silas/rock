import os
import sys
import yaml
from rock import utils
from rock.exceptions import ConfigError, RunError


class Project(object):

    def __init__(self, path, config=None):
        self.path = path
        self.config = config or {}
        self.setup()

    def setup(self):
        config = {}

        path = os.path.join(self.path, '.rock.yml')

        try:
            with open(path) as f:
                config = yaml.load(f)
        except Exception, error:
            raise ConfigError('Failed to read configuration file: '
                + path)

        runtime = config.get('runtime')

        if not isinstance(runtime, basestring):
            raise ConfigError('Invalid runtime: %s' % runtime)

        config['type'] = config['runtime'].rstrip('0123456789')
        config['runtime_root'] = os.path.join('/opt', 'rock', 'runtime', config['runtime'])
        config['runtime_env'] = os.path.join(config['runtime_root'], 'env')

        path = os.path.dirname(__file__)
        path = os.path.join(path, 'runtime', '%s.yml' % config['type'])

        if os.path.exists(path):
            try:
                with open(path) as f:
                    tmp_config = yaml.load(f)
                    tmp_config.update(config)
                    config = tmp_config
            except Exception, error:
                print 'Failed to parse: %s' % path

        for name in ('build', 'test'):
            value = config.get(name)

            if not isinstance(name, basestring):
                raise ConfigError('Invalid %s: %s' % (name, value))

        config['verbose'] = any([
            self.config.get('verbose'),
            config.get('verbose'),
        ])

        self.config = config

    def execute(self, command):
        with utils.Shell(stdout=sys.stdout, stderr=sys.stderr) as s:
            s.run('source ' + self.config['runtime_env'])
            s.run('set -e')
            if self.config['verbose']:
                s.run('set -v')
            s.run(command)
            s.wait()
            if s.code > 0:
                raise RunError()

    def build(self):
        self.execute(self.config['build'])

    def run(self, command):
        if 'run' in self.config:
            command = str.format(self.config['run'], command=command)
        self.execute(command)

    def test(self):
        self.execute(self.config['test'])
