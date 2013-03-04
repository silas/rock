import helper
from rock import utils
from rock.exceptions import ConfigError


class UtilsTestCase(helper.unittest.TestCase):

    def test_shell(self):
        utils.Shell.run = lambda self: self
        s = utils.Shell()
        self.assertTrue(isinstance(s.__enter__(), utils.Shell))
        s.write('ok')
        s.__exit__(None, None, None)
        self.assertEqual(s.stdin.getvalue(), 'ok\n')
        def execl(*args):
            self.assertEqual(len(args), 4)
            self.assertEqual(args[0], '/bin/bash')
            self.assertEqual(args[1], '-l')
            self.assertEqual(args[2], '-c')
            self.assertEqual(args[3], 'ok\n')
        utils.os.execl = execl
        s.__exit__('type', 'value', 'tracebook')

    def test_noshell(self):
        utils.ROCK_SHELL = '/tmp/hopefully-no-exists'
        s = utils.Shell()
        s.__enter__()
        self.assertRaises(ConfigError, s.__exit__, 'type', 'value', 'tracebook')
