import unittest

import os
import sys
import inspect

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/..'))
from mlc_tools.core.Function import *
from mlc_tools.core.Object import *


class TestParseReturnType(unittest.TestCase):
    
    def test_1(self):
        func = Function()
        func.parse('function ReturnValue* name()')
        self.assertEqual(func.return_type, 'ReturnValue*')
        
class TestParseArguments(unittest.TestCase):
    
    def _test_args_on_linked(self, func, name, type_of_object):
        self.assertTrue(func.args[0][0] == name)
        self.assertTrue(isinstance(func.args[0][1], Object))
        self.assertEqual(func.args[0][1].type, type_of_object)

    def test_0(self):
        func = Function()
        func.parse('function void name(int i)')
        self.assertEqual(func.args[0], ['i', 'int'])
        func.link()
        self._test_args_on_linked(func, 'i', 'int')
        
    def test_1(self):
        func = Function()
        func.parse('function void name(int i=0)')
        self.assertEqual(func.args[0], ['i=0', 'int'])
        func.link()
        self._test_args_on_linked(func, 'i', 'int')

    def test_2(self):
        func = Function()
        func.parse('function void name(map<string, int> some_map)')
        self.assertEqual(func.args[0], ['some_map', 'map<string, int>'])
        func.link()
        self._test_args_on_linked(func, 'some_map', 'map')

    def test_3(self):
        func = Function()
        func.parse('function void name(map<int, ReturnValue*>:const some_map)')
        self.assertEqual(func.args[0], ['some_map', 'map<int, ReturnValue*>:const'])
        func.link()
        self._test_args_on_linked(func, 'some_map', 'map')


if __name__ == '__main__':
    unittest.main()