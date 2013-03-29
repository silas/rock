import unittest
from helper import RuntimeTests

class RuntimeTestCase(RuntimeTests, unittest.TestCase):

    name = 'ruby19'
    init_files = ['Gemfile', 'Rakefile']
    init_directories = ['test']

if __name__ == '__main__':
    unittest.main()
