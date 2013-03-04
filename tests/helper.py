import os
try:
    import unittest2 as unittest
except:
    import unittest
from rock.config import Config


ROOT_PATH = os.path.dirname(os.path.dirname(__file__))
TESTS_PATH = os.path.join(ROOT_PATH, 'tests')
ASSETS_PATH = os.path.join(TESTS_PATH, 'assets')
CONFIG_PATH = os.path.join(ASSETS_PATH, 'config')
ENV_PATH = os.path.join(ASSETS_PATH, 'env')
DATA_PATH = os.path.join(ASSETS_PATH, 'data')
PROJECT_PATH = os.path.join(ASSETS_PATH, 'project')
USER_PATH = os.path.join(ASSETS_PATH, 'user')


def setenv(mount='test', data='test', user='test'):
    @staticmethod
    def mount_path(*args):
        return os.path.join(*(ENV_PATH, mount) + args)

    @staticmethod
    def data_path(*args):
        return os.path.join(*(DATA_PATH, data) + args)

    @staticmethod
    def user_path(*args):
        return os.path.join(*(USER_PATH, data) + args)

    Config.mount_path = mount_path
    Config.data_path = data_path
    Config.user_path = user_path


class Args(object):

    def __init__(self, **kwargs):
        self.path = os.path.join(PROJECT_PATH, kwargs.get('name', 'simple'))
        self.verbose = True
        self.dry_run = True
        self.runtime = 'test123'
        self.env = 'local'
        for name, value in kwargs.items():
            setattr(self, name, value)


def project(args=None):
    args = args or Args()
    config = {'path': args.path}
    if args.verbose:
        config['verbose'] = True
    if args.dry_run:
        config['dry_run'] = True
        config['verbose'] = True
    if args.runtime:
        config['runtime'] = args.runtime
    from rock.project import Project
    return Project(config, env=args.env)
