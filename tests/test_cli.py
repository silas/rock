import helper
from rock import cli
from rock.project import Project


class Args(object):
    verbose = True
    dry_run = True
    runtime = 'node08'
    path = '/tmp'


class CliTestCase(helper.unittest.TestCase):

    def test_project(self):
        self.assertTrue(isinstance(cli.project(Args), Project))
