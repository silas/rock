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
        @staticmethod
        def root_path():
            return '/tmp/this-should-not-exist'
        runtime.Runtime.root_path = root_path
        rs = runtime.list()
        self.assertEqual(len(rs), 0)
        self.assertTrue(isinstance(rs, list))
