import helper
from rock import runtime


class RuntimeTestCase(helper.unittest.TestCase):

    def setUp(self):
        helper.setenv()

    def test_list(self):
        rs = runtime.list()
        self.assertEqual(rs[0].name, 'parent123')
        self.assertEqual(rs[1].name, 'parse123')
        self.assertEqual(rs[2].name, 'test123')
        self.assertEqual(rs[3].name, 'user123')
        @staticmethod
        def not_found():
            return '/tmp/this-should-not-exist'
        runtime.Runtime.root_path = not_found
        runtime.Runtime.user_path = not_found
        rs = runtime.list()
        self.assertEqual(len(rs), 0)
        self.assertTrue(isinstance(rs, list))
