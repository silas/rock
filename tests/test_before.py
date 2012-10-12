import helper
import os
from rock.config import Config

class BeforeTestCase(helper.unittest.TestCase):

    def test_config(self):
        c = Config({'path': ''}, env='local')
        self.assertEqual(c.data_path(), os.path.realpath(os.path.join(
            os.path.dirname(__file__), '..', 'rock', 'data')))
        self.assertEqual(c.mount_path(), '/')
        self.assertEqual(c.user_path(), os.path.expanduser('~/.rock'))
