import os
import string
import yaml
from rock import utils
from rock.exceptions import ConfigError, RunError


class Project(object):

    def __init__(self, path, config=None):
        self.path = path
        self.config = config or {}
        self.parse()

    def merge_config(self, src, dst):
        if 'env' in src:
            # ensure env is a dict of strings
            if not (isinstance(src['env'], dict) or
                    all(map(lambda v: isinstance(v, basestring), src['env'].values()))):
                raise ConfigError('env must be an associative array of strings')
            if 'env' not in dst:
                dst['env'] = {}
            # evaluate env variables
            for name, value in src['env'].items():
                dst['env'][name] = string.Template(src['env'][name]).safe_substitute(**dst['env'])
            del src['env']
        dst.update(src)

    def parse(self):
        project_config = {}

        # parse project

        path = os.path.join(self.path, '.rock.yml')

        try:
            with open(path) as f:
                project_config = yaml.load(f)
                project_config.update(self.config)
        except Exception, error:
            raise ConfigError('Failed to read configuration file: '
                + path)

        runtime = project_config.get('runtime')

        if not isinstance(runtime, basestring):
            raise ConfigError('Invalid runtime: %s' % runtime)

        # parse global config

        mount = '/'

        project_config['type'] = project_config['runtime'].rstrip('0123456789')
        project_config['runtime_root'] = os.path.join(mount, 'opt', 'rock', 'runtime',
            project_config['runtime'])

        runtime_path = ['runtime', '%s.yml' % project_config['type']]

        # list of possible configuration files
        data_path = []
        data_path.append(os.path.join(project_config['runtime_root'], 'rock.yml'))
        data_path.append(os.path.join(os.path.dirname(__file__), 'data',
            *runtime_path))
        data_path.append(os.path.join(mount, 'etc', 'rock', *runtime_path))

        config = {'env': {'PROJECT_PATH': self.path}}

        # read non-project configuration files
        for path in data_path:
            if os.path.exists(path):
                try:
                    with open(path) as f:
                        self.merge_config(yaml.load(f), config)
                except Exception, error:
                    raise ConfigError('Failed to parse "%s": %s' % (path, error))

        # merge non-project configuration into project configuration
        self.merge_config(project_config, config)

        # validate
        for name in ('build', 'setup', 'test'):
            value = config.get(name)

            if not isinstance(name, basestring):
                raise ConfigError('Invalid %s: %s' % (name, value))

        # finish
        self.config = config

    def execute(self, command, **kwargs):
        with utils.Shell(**kwargs) as s:
            # exit with error if any one command fails
            s.run('set -o errexit')
            # print commands as they're run
            s.run('set -o verbose')
            # don't execute commands, just print them
            if self.config['dry_run']:
                s.run('set -o noexec')
            # setup environment variables
            for name, value in self.config['env'].items():
                s.run('export %s="%s"' % (name, value))
            # run command and wait for results
            s.run(command)
            s.wait()
            if s.code > 0:
                raise RunError()

    def build(self):
        self.execute(self.config['build'])

    def clean(self):
        self.execute(self.config['clean'])

    def run(self, command):
        self.execute(command, stdin=True)

    def setup(self):
        self.execute(self.config['setup'])

    def test(self):
        self.execute(self.config['test'])
