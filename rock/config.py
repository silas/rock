from __future__ import unicode_literals

import collections
import copy
import os
import re
import string
import yaml
from rock import constants
from rock.exceptions import ConfigError
from rock.utils import isstr, raw

PARENT_RE = re.compile(r'\{\{\s*parent\s*\}\}', re.MULTILINE)


class Config(collections.Mapping):
    """
    Parse and merge configuration files.
    """

    def __init__(self, data, env=None):
        self.data = data
        self.env = env
        self._setup = False

    @staticmethod
    def paths(*args):
        return (
            Config.user_path(*args),
            Config.etc_path(*args),
            Config.data_path(*args),
        )

    @staticmethod
    def data_path(*args):
        return os.path.join(*(os.path.dirname(os.path.realpath(__file__)),
                            'data') + args)

    @staticmethod
    def etc_path(*args):
        return Config.mount_path(*('etc', 'rock') + args)

    @staticmethod
    def mount_path(*args):
        return os.path.join(*(constants.MOUNT_PATH,) + args)

    @staticmethod
    def user_path(*args):
        return os.path.join(*(os.path.expanduser('~/.rock'),) + args)

    @staticmethod
    def runtime(*args, **kwargs):
        from rock.runtime import Runtime
        return Runtime(*args, **kwargs)

    @staticmethod
    def parse(path, require_exists=True, require_parses=True):
        """
        Parse and return configuration file.
        """
        if not os.path.isfile(path):
            if require_exists:
                raise ConfigError('not found: ' + path)
            return
        try:
            with open(path) as f:
                return yaml.safe_load(f)
        except Exception as error:
            if require_parses:
                raise ConfigError('parse error: ' + path)

    def merge_env(self, src, dst, env=None):
        """
        Merge environment variables.
        """
        env = 'env_%s' % env if env else 'env'
        if env in src:
            if not isinstance(src[env], dict):
                raise ConfigError('%s must be an associative array' % env)
            # evaluate env variables
            for name, value in src[env].items():
                if not isstr(value):
                    if isinstance(value, (int, float)):
                        src[env][name] = str(value)
                    else:
                        raise ConfigError('%s.%s must be a string' %
                                          (env, name))
                dst['env'][name] = string.Template(
                    src[env][name]).safe_substitute(**dst['env']).rstrip('\n')

            del src[env]

    def merge(self, src, dst):
        if src is None:
            return dst
        # merge global environment variables
        self.merge_env(src, dst)
        # merge env-specific environment variables
        self.merge_env(src, dst, self.env)
        # merge sections
        for name in list(src.keys()):
            if name not in dst:
                if isstr(src[name]):
                    src[name] = PARENT_RE.sub('', src[name])
                elif isinstance(src[name], dict):
                    for subname in src[name]:
                        value = src[name][subname]
                        if isstr(value):
                            src[name][subname] = PARENT_RE.sub('', value)
                dst[name] = src[name]
            elif isstr(src[name]):
                if not isstr(dst[name]):
                    raise ConfigError('unable to merge "%s" into "str"' %
                                      type(dst[name]).__name__)
                dst[name] = PARENT_RE.sub(raw(dst[name]), src[name])
            elif isinstance(src[name], dict):
                dst_is_dict = isinstance(dst[name], dict)
                for subname in src[name]:
                    if isstr(dst[name]):
                        src[name][subname] = PARENT_RE.sub(raw(dst[name]),
                                                           src[name][subname])
                    elif dst_is_dict:
                        if subname in dst[name]:
                            src[name][subname] = PARENT_RE.sub(
                                raw(dst[name][subname]),
                                src[name][subname],
                            )
                            del dst[name][subname]
                        else:
                            src[name][subname] = PARENT_RE.sub(
                                '',
                                src[name][subname],
                            )
                if dst_is_dict:
                    src[name].update(dst[name])
                dst[name] = src[name]
            del src[name]
        dst.update(src)

    @staticmethod
    def evaluate(data):
        changed = False
        for _ in range(5):
            changed = False
            for n1, v1 in data.items():
                if not isstr(v1):
                    continue
                n = re.escape(n1)
                r = re.compile(r'\{\{\s*' + n + r'\s*\}\}', re.MULTILINE)
                for n2, v2 in data.items():
                    if not isstr(v2):
                        continue
                    data[n2] = r.sub(raw(data[n1]), data[n2]).rstrip('\n')
                    changed |= v2 != data[n2]
            if not changed:
                break
        if changed:
            raise ConfigError('.rock.yml circular reference')

    def setup_path(self):
        if not self.data.get('path'):
            path = '.'
            while os.path.split(os.path.abspath(path))[1]:
                config_path = os.path.join(path, '.rock.yml')
                if os.path.isfile(config_path):
                    self.data['path'] = os.path.abspath(path)
                    break
                path = os.path.join('..', path)
        if not self.data.get('path'):
            self.data['path'] = os.getcwd()

    def setup(self):
        if self._setup:
            return
        self._setup = True
        # path
        self.setup_path()
        # new configuration
        data = {}
        # runtime
        yml_path = os.path.join(self.data['path'], '.rock.yml')
        if yml_path and os.path.isfile(yml_path):
            data = self.parse(yml_path)
            if not isinstance(data, dict):
                raise ConfigError('.rock.yml syntax error')
            data.update(self.data)
        else:
            data = copy.deepcopy(self.data)
        # runtime
        require_runtime = 'runtime' in data
        if require_runtime:
            require_runtime = data['runtime'] not in constants.RUNTIMES
        else:
            data['runtime'] = '__none__'
        # project
        if not data.get('path'):
            raise ConfigError('path is required')
        if not os.path.isdir(data['path']):
            raise ConfigError('path is not a directory')
        # paths
        runtime = self.runtime(data['runtime'])
        etc_path = self.etc_path('runtime')
        runtime_yml = data['runtime'] + '.yml'
        data_path = self.data_path('runtime', runtime_yml)
        if not os.path.exists(data_path):
            file_name = data['runtime'].rstrip('0123456789') + '.yml'
            data_path = self.data_path('runtime', file_name)
        # ensure runtime exists
        if require_runtime and not os.path.isdir(runtime.path()):
            raise ConfigError(
                "%s runtime path doesn't exist" % data['runtime']
            )
        # parse configs
        runtime_config = self.parse(runtime.path('rock.yml'),
                                    require_exists=require_runtime)
        rock_config = self.parse(data_path, require_exists=False)
        etc_config = self.parse(os.path.join(etc_path, runtime_yml),
                                require_exists=False)
        # merge
        self.data = {
            'env': {
                'ROCK_ENV': self.env,
                'ROCK_PATH': data['path'],
                'ROCK_RUNTIME': data['runtime'],
            },
        }
        # merge runtime
        self.merge(runtime_config, self.data)
        # merge runtime config
        self.merge(rock_config, self.data)
        self.merge(etc_config, self.data)
        # merge project
        self.merge(data, self.data)
        # evaluate
        self.evaluate(self.data)

    def __contains__(self, *args, **kwargs):
        self.setup()
        return self.data.__contains__(*args, **kwargs)

    def __getitem__(self, *args, **kwargs):
        self.setup()
        return self.data.__getitem__(*args, **kwargs)

    def __iter__(self, *args, **kwargs):
        self.setup()
        return self.data.__iter__(*args, **kwargs)

    def __len__(self, *args, **kwargs):
        self.setup()
        return self.data.__len__(*args, **kwargs)
