import unittest
from helper import RuntimeTests

class RuntimeTestCase(RuntimeTests, unittest.TestCase):

    name = 'python27'
    init_files = ['requirements.txt']
    init_directories = ['tests']

if __name__ == '__main__':
    unittest.main()
