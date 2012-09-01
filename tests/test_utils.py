import helper
from rock import utils


class UtilsTestCase(helper.unittest.TestCase):

    def test_shell(self):
        def execute(self, *args):
            self.args = args
        utils.Shell.execute = execute
        s = utils.Shell()
        self.assertTrue(isinstance(s.__enter__(), utils.Shell))
        s.write('ok')
        self.assertEqual(s.stdin.getvalue(), 'ok\n')
