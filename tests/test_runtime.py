from __future__ import unicode_literals

import helper
from rock import runtime


class RuntimeTestCase(helper.unittest.TestCase):

    def setUp(self):
        helper.setenv()

    def test_list(self):
        rs = runtime.list()
        self.assertEqual(rs[0].name, 'escape123')
        self.assertEqual(rs[1].name, 'parent123')
        self.assertEqual(rs[2].name, 'parse123')
        self.assertEqual(rs[3].name, 'test123')
        self.assertEqual(rs[4].name, 'user123')
        @staticmethod
        def not_found():
            return '/tmp/this-should-not-exist'
        old_root_path = runtime.Runtime.root_path
        old_user_path = runtime.Runtime.user_path
        runtime.Runtime.root_path = not_found
        runtime.Runtime.user_path = not_found
        rs = runtime.list()
        self.assertEqual(len(rs), 0)
        self.assertTrue(isinstance(rs, list))
        runtime.Runtime.root_path = old_root_path
        runtime.Runtime.user_path = old_user_path
