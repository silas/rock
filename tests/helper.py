import os
try:
    import unittest2 as unittest
except:
    import unittest
from rock.config import Config


TESTS_PATH = os.path.join(os.path.dirname(__file__))
ASSETS_PATH = os.path.join(TESTS_PATH, 'assets')
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


def hook(name, project, args=None, **kwargs):
    args = args or []
    return ','.join(args) if args else 'ok'
