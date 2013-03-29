import unittest
from helper import RuntimeTests

class RuntimeTestCase(RuntimeTests, unittest.TestCase):

    name = 'node06'
    init_files = ['package.json']
    init_directories = ['test']

if __name__ == '__main__':
    unittest.main()
