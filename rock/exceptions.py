class Error(Exception):
    pass


class BuildError(Error):
    pass


class ConfigError(Error):
    pass


class EnvError(Error):
    pass


class TestError(Error):
    pass
