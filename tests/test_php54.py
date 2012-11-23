import unittest
from helper import RuntimeTests

class RuntimeTestCase(RuntimeTests, unittest.TestCase):

    name = 'php54'

    def test_full(self):
        self.runtime(self.name)

if __name__ == '__main__':
    unittest.main()
