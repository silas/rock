import ops
from rock.exceptions import TestError


class Test(object):

    def __init__(self, project):
        self.project = project

    def __call__(self):
        self.project.runtime.env(setup=True)

        command = self.project.config.get('test')

        if command is None:
            raise TestError('No test command specified')

        test = ops.run(command, path=self.project.path, cwd=self.project.path)

        if not test:
            raise TestError(test.stdout)
