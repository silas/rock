import os
try:
    import unittest2 as unittest
except:
    import unittest
from rock.config import Config


TESTS_PATH = os.path.join(os.path.dirname(__file__))
ENV_PATH = os.path.join(TESTS_PATH, 'assets', 'env')


def setenv(mount='test', data='test'):
    @staticmethod
    def mount_path(*args):
        return os.path.join(*(ENV_PATH, mount) + args)

    @staticmethod
    def data_path(*args):
        return os.path.join(*(TESTS_PATH, 'assets', 'data', data) + args)

    Config.mount_path = mount_path
    Config.data_path = data_path
