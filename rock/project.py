import os
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

        # parse project

        path = os.path.join(self.path, '.rock.yml')

        try:
            with open(path) as f:
                config = yaml.load(f)
                config.update(self.config)
        except Exception, error:
            raise ConfigError('Failed to read configuration file: '
                + path)

        runtime = config.get('runtime')

        if not isinstance(runtime, basestring):
            raise ConfigError('Invalid runtime: %s' % runtime)

        # parse global config

        mount = '/'

        config['type'] = config['runtime'].rstrip('0123456789')
        config['runtime_root'] = os.path.join(mount, 'opt', 'rock', 'runtime',
            config['runtime'])
        config['runtime_env'] = os.path.join(config['runtime_root'], 'env')

        runtime_path = ['runtime', '%s.yml' % config['type']]

        data_path = []
        data_path.append(os.path.join(os.path.dirname(__file__), 'data',
            *runtime_path))
        data_path.append(os.path.join(mount, 'etc', 'rock', *runtime_path))

        for path in data_path:
            if os.path.exists(path):
                try:
                    with open(path) as f:
                        tmp_config = yaml.load(f)
                        tmp_config.update(config)
                        config = tmp_config
                except Exception, error:
                    raise ConfigError('Failed to parse "%s": %s' % (path, error))

        # validate

        for name in ('build', 'test'):
            value = config.get(name)

            if not isinstance(name, basestring):
                raise ConfigError('Invalid %s: %s' % (name, value))

        # finish

        self.config = config

    def execute(self, command, **kwargs):
        with utils.Shell(**kwargs) as s:
            # import runtime environment
            s.run("source '%s'" % self.config['runtime_env'])
            # exit with error if any one command fails
            s.run('set -o errexit')
            # print commands as they're run
            s.run('set -o verbose')
            # don't execute commands, just print them
            if self.config['dry_run']:
                s.run('set -o noexec')
            # run command and wait for results
            s.run(command)
            s.wait()
            if s.code > 0:
                raise RunError()

    def build(self):
        self.execute(self.config['build'])

    def run(self, command):
        if 'run' in self.config:
            command = str.format(self.config['run'], command=command)
        self.execute(command, stdin=True)

    def test(self):
        self.execute(self.config['test'])
