import collections
import copy
import os
import re
import string
import yaml
from rock.exceptions import ConfigError


PARENT_RE = re.compile(r'\{\{\s*parent\s*\}\}', re.MULTILINE)
TEMPLATE_RE = re.compile(r'^(?:build|clean|run|test)(?:_.+)?$')


class Config(collections.Mapping):

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
        return os.path.join(*(os.path.dirname(__file__), 'data') + args)

    @staticmethod
    def etc_path(*args):
        return Config.mount_path(*('etc', 'rock') + args)

    @staticmethod
    def mount_path(*args):
        return os.path.join(*('/',) + args)

    @staticmethod
    def user_path(*args):
        return os.path.join(*(os.path.expanduser('~/.rock'),) + args)

    @staticmethod
    def runtime(*args, **kwargs):
        from rock.runtime import Runtime
        return Runtime(*args, **kwargs)

    @staticmethod
    def parse(path, require_exists=True, require_parses=True):
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

    def merge_env(self, src, dst, env=None):
        env = 'env_%s' % env if env else 'env'
        if env in src:
            if not isinstance(src[env], dict):
                raise ConfigError('%s must be an associative array' % env)
            # evaluate env variables
            for name, value in src[env].items():
                if not isinstance(value, basestring):
                    if isinstance(value, (int, float)):
                        src[env][name] = str(value)
                    else:
                        raise ConfigError('%s.%s must be a string' %
                                          (env, name))
                dst['env'][name] = string.Template(
                    src[env][name]).safe_substitute(**dst['env'])
            del src[env]

    def merge(self, src, dst):
        if src is None:
            return dst
        self.merge_env(src, dst)
        self.merge_env(src, dst, self.env)
        # parent section to build, clean, run and test
        for name in src.keys():
            if not TEMPLATE_RE.match(name):
                continue
            if name not in dst:
                if isinstance(src[name], basestring):
                    src[name] = PARENT_RE.sub('', src[name])
                elif isinstance(src[name], dict):
                    for subname in src[name]:
                        value = src[name][subname]
                        if isinstance(value, basestring):
                            src[name][subname] = PARENT_RE.sub('', value)
                dst[name] = src[name]
            elif isinstance(src[name], basestring):
                if not isinstance(dst[name], basestring):
                    raise ConfigError('unable to merge "%s" into "str"' %
                                      type(dst[name]).__name__)
                dst[name] = PARENT_RE.sub(dst[name], src[name])
            elif isinstance(src[name], dict):
                dst_is_dict = isinstance(dst[name], dict)
                for subname in src[name]:
                    if isinstance(dst[name], basestring):
                        src[name][subname] = PARENT_RE.sub(dst[name],
                                                           src[name][subname])
                    elif dst_is_dict:
                        if subname in dst[name]:
                            src[name][subname] = PARENT_RE.sub(
                                dst[name][subname],
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

    def setup(self):
        if self._setup:
            return
        self._setup = True
        # setup configuration
        data = {}
        # runtime
        yml_path = ('path' in self.data and
                    os.path.join(self.data['path'], '.rock.yml'))
        if yml_path and os.path.isfile(yml_path):
            data = self.parse(yml_path)
            if not isinstance(data, dict):
                raise ConfigError('.rock.yml syntax error')
            data.update(self.data)
        else:
            data = copy.deepcopy(self.data)
        if 'runtime' in data and 'runtime_type' not in data:
            data['runtime_type'] = data['runtime'].rstrip('0123456789')
        # project
        for name in ('path', 'runtime', 'runtime_type'):
            if name not in data:
                raise ConfigError('%s is required' % name)
        # runtime
        runtime = self.runtime(data['runtime'])
        # paths
        etc_path = self.etc_path('runtime')
        runtime_type_yml = data['runtime_type'] + '.yml'
        runtime_yml = data['runtime'] + '.yml'
        # ensure runtime exists
        if not os.path.isdir(runtime.path()):
            raise ConfigError("runtime path doesn't exist")
        # parse configs
        runtime_config = self.parse(runtime.path('rock.yml'))
        rock_type_config = self.parse(self.data_path('runtime',
                                      runtime_type_yml), require_exists=False)
        rock_config = self.parse(self.data_path('runtime', runtime_yml),
                                 require_exists=False)
        etc_type_config = self.parse(os.path.join(etc_path,
                                     runtime_type_yml), require_exists=False)
        etc_config = self.parse(os.path.join(etc_path, runtime_yml),
                                require_exists=False)
        # merge
        self.data = {
            'env': {
                'PROJECT_PATH': data['path'],
                'ROCK_ENV': self.env,
            },
        }
        # merge runtime
        self.merge(runtime_config, self.data)
        # merge runtime config
        if rock_config or etc_config:
            self.merge(rock_config, self.data)
            self.merge(etc_config, self.data)
        else:
            self.merge(rock_type_config, self.data)
            self.merge(etc_type_config, self.data)
        # merge project
        self.merge(data, self.data)

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
