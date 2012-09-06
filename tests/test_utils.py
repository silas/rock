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
        def execl(*args):
            self.assertEqual(len(args), 5)
            self.assertEqual(args[0], '/usr/bin/env')
            self.assertEqual(args[1], 'bash')
            self.assertEqual(args[2], 'bash')
            self.assertEqual(args[3], '-c')
            self.assertEqual(args[4], 'ok\n')
        utils.os.execl = execl
        s.__exit__('type', 'value', 'tracebook')
