import ops
from rock.exceptions import BuildError


class Build(object):

    def __init__(self, project):
        self.project = project

    def __call__(self):
        self.project.runtime.env(setup=True)

        command = self.project.config.get('build',
                                          'rock-build-${type} ${path}')

        build = ops.run(command, type=self.project.runtime.type,
                        path=self.project.path)

        if not build:
            raise BuildError(build.stderr.strip())

        return build.stdout.strip()
