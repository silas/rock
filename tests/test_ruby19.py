import unittest
from helper import RuntimeTests

class RuntimeTestCase(RuntimeTests, unittest.TestCase):

    name = 'ruby19'

    def test_full(self):
        self.runtime(self.name)

if __name__ == '__main__':
    unittest.main()
