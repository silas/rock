import collections
import copy
import os
import string
import yaml
from rock.exceptions import ConfigError


class Config(collections.Mapping):

    MOUNT = '/'
    DATA = os.path.join(os.path.dirname(__file__), 'data')

    def __init__(self, data):
        self._data = data
        self._setup = False

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

    def setup(self):
        if self._setup: return
        self._setup = True
        # setup configuration
        data = {}
        # runtime
        yml_path = ('path' in self._data and
            os.path.join(self._data['path'], '.rock.yml'))
        if yml_path and os.path.isfile(yml_path):
            data = self.parse(yml_path)
            data.update(self._data)
        else:
            data = copy.deepcopy(self._data)
        if 'runtime' in data and 'runtime_type' not in data:
            data['runtime_type'] = data['runtime'].rstrip('0123456789')
        # project
        for name in ('path', 'runtime', 'runtime_type'):
            if name not in data:
                raise ConfigError('%s is required' % name)
        # paths
        runtime_path = os.path.join(self.MOUNT, 'opt', 'rock', 'runtime',
            data['runtime'])
        etc_path = os.path.join(self.MOUNT, 'etc', 'rock', 'runtime')
        runtime_type_yml = data['runtime_type'] + '.yml'
        runtime_yml = data['runtime'] + '.yml'
        # ensure runtime exists
        if not os.path.isdir(runtime_path):
            raise ConfigError("runtime path doesn't exist")
        # configs
        runtime_config = self.parse(os.path.join(runtime_path,
            'rock.yml'))
        rock_type_config = self.parse(os.path.join(self.DATA, 'runtime',
            runtime_type_yml), require_exists=False)
        rock_config = self.parse(os.path.join(self.DATA, 'runtime',
            runtime_yml), require_exists=False)
        etc_type_config = self.parse(os.path.join(etc_path,
            runtime_type_yml), require_exists=False)
        etc_config = self.parse(os.path.join(etc_path, runtime_yml),
            require_exists=False)
        # merge
        self._data = {
            'env': {
                'PROJECT_PATH': data['path'],
            },
        }
        # merge runtime
        self.merge(runtime_config, self._data)
        # merge runtime config
        if rock_config or etc_config:
            self.merge(rock_config, self._data)
            self.merge(etc_config, self._data)
        else:
            self.merge(rock_type_config, self._data)
            self.merge(etc_type_config, self._data)
        # merge project
        self.merge(data, self._data)

    def __contains__(self, *args, **kwargs):
        self.setup()
        return self._data.__contains__(*args, **kwargs)

    def __getitem__(self, *args, **kwargs):
        self.setup()
        return self._data.__getitem__(*args, **kwargs)

    def __iter__(self, *args, **kwargs):
        self.setup()
        return self._data.__getitem__(*args, **kwargs)

    def __len__(self, *args, **kwargs):
        self.setup()
        return self._data.__len__(*args, **kwargs)
