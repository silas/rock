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

    def run(self, name):
        if name not in self.config:
            raise ConfigError('%s not found' % name.capitalize())

        kwargs = {}

        if self.config['verbose']:
            kwargs['stdout'] = sys.stdout
            kwargs['stderr'] = sys.stderr

        with utils.Shell(**kwargs) as s:
            s.run('source ' + self.config['runtime_env'])
            s.run('set -ev')
            s.run(self.config[name])
            s.wait()
            if s.code > 0:
                text = '\nFailed to %s' % name
                if not self.config['verbose'] and s.data[0] is not None:
                    text = '%s\n%s' % (s.data[0].rstrip(), text)
                raise RunError(text)

    def build(self):
        self.run('build')

    def test(self):
        self.run('test')
