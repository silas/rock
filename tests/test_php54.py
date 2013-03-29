import unittest
from helper import RuntimeTests

class RuntimeTestCase(RuntimeTests, unittest.TestCase):

    name = 'php54'
    init_files = ['composer.json']
    init_directories = ['tests']

if __name__ == '__main__':
    unittest.main()
