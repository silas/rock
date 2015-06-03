import unittest
import sample

class TestCase(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(sample.convert('# Test'), '<h1>Test</h1>')
