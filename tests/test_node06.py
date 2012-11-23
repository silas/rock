import unittest
from helper import RuntimeTests, node_hook

class RuntimeTestCase(RuntimeTests, unittest.TestCase):

    name = 'node06'

    def test_full(self):
        self.runtime(self.name, post_test=node_hook)

if __name__ == '__main__':
    unittest.main()
