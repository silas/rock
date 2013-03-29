import unittest
from helper import RuntimeTests

class RuntimeTestCase(RuntimeTests, unittest.TestCase):

    name = 'perl516'
    init_files = ['cpanfile']
    init_directories = ['t']

if __name__ == '__main__':
    unittest.main()
