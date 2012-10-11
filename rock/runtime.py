import os
from rock.config import Config


class Runtime(object):

    def __init__(self, name):
        self.name = name

    @staticmethod
    def root_path(*args):
        return Config.mount_path(*('opt', 'rock', 'runtime') + args)

    @staticmethod
    def user_path(*args):
        return Config.user_path(*('runtime',) + args)

    def path(self, *args):
        if os.path.exists(self.user_path(self.name, 'rock.yml')):
            return self.user_path(*(self.name,) + args)
        return self.root_path(*(self.name,) + args)

    def exists(self, *args):
        return os.path.exists(self.path(*args))


def list():
    path = Runtime.root_path()
    if not os.path.isdir(path):
        return []
    rs = map(Runtime, os.listdir(path))
    rs = [r for r in rs if r.exists('rock.yml')]
    return sorted(rs, key=lambda r: r.name)
