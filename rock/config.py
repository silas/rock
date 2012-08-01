import copy
import os
import string
import yaml
from rock.exceptions import ConfigError


class Config(object):

    MOUNT = '/'
    DATA = os.path.join(os.path.dirname(__file__), 'data')

    def __init__(self, project=None):
        self._project = project if project else {}
        self._full = None

    def parse(self, path, require_exists=True, require_parses=True):
        if not os.path.isfile(path):
            if require_exists:
                raise ConfigError('not found: ' + path)
            else:
                return None
        try:
            with open(path) as f:
                return yaml.load(f)
        except Exception, error:
            if require_parses:
                raise ConfigError('parse error: ' + path)

    def merge(self, src, dst):
        if src is None:
            return dst
        if 'env' in src:
            # ensure env is a dict of strings
            if not (isinstance(src['env'], dict) or
                    all(map(lambda v: isinstance(v, basestring),
                    src['env'].values()))):
                raise ConfigError('env must be an associative array of ' +
                    'strings')
            if 'env' not in dst:
                dst['env'] = {}
            # evaluate env variables
            for name, value in src['env'].items():
                dst['env'][name] = string.Template(
                    src['env'][name]).safe_substitute(**dst['env'])
            del src['env']
        dst.update(src)

    def project(self):
        if not hasattr(self, '_project_merge'):
            if 'path' in self._project:
                data = self.parse(os.path.join(self._project['path'],
                    '.rock.yml'))
                data.update(self._project)
                self._project = data
            if 'runtime' in self._project:
                if 'runtime_type' not in self._project:
                    self._project['runtime_type'] = self._project['runtime']. \
                        rstrip('0123456789')
            self._project_merge = True
        return copy.deepcopy(self._project)

    def full(self):
        if self._full is None:
            project = self.project()
            # full requirements
            for name in ('path', 'runtime', 'runtime_type'):
                if name not in project:
                    raise ConfigError('%s is required' % name)
            # helper
            runtime_path = os.path.join(self.MOUNT, 'opt', 'rock', 'runtime',
                project['runtime'])
            etc_path = os.path.join(self.MOUNT, 'etc', 'rock', 'runtime')
            runtime_type_yml = project['runtime_type'] + '.yml'
            runtime_yml = project['runtime'] + '.yml'
            # configs
            platform_config = self.parse(os.path.join(runtime_path,
                'rock.yml'), require_exists=False)
            rock_type_config = self.parse(os.path.join(self.DATA, 'runtime',
                runtime_type_yml), require_exists=False)
            rock_config = self.parse(os.path.join(self.DATA, 'runtime',
                runtime_yml), require_exists=False)
            etc_type_config = self.parse(os.path.join(etc_path,
                runtime_type_yml), require_exists=False)
            etc_config = self.parse(os.path.join(etc_path, runtime_yml),
                require_exists=False)
            # merge
            self._full = {
                'env': {
                    'PROJECT_PATH': project['path'],
                },
            }
            # merge configs into full
            self.merge(platform_config, self._full)
            if rock_config or etc_config:
                self.merge(rock_config, self._full)
                self.merge(etc_config, self._full)
            else:
                self.merge(rock_type_config, self._full)
                self.merge(etc_type_config, self._full)
            # merge project
            self.merge(project, self._full)
        return copy.deepcopy(self._full)
