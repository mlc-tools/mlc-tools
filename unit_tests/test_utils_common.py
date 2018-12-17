import unittest

import os
import sys
import inspect

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/..'))
from mlc_tools.utils.common import smart_split


class TestParseObject(unittest.TestCase):
    
    def test_1(self):
        parts = smart_split('int a, int b, int c', ',')
        self.assertEqual(len(parts), 3)
        self.assertEqual(parts[0], 'int a')
        self.assertEqual(parts[1], ' int b')
        self.assertEqual(parts[2], ' int c')


if __name__ == '__main__':
    unittest.main()