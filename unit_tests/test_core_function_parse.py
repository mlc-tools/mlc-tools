import unittest

import os
import sys
import inspect

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/..'))
from mlc_tools.base.Parser import *
from mlc_tools.core.Object import *


class TestParseReturnType(unittest.TestCase):
    
    def test_1(self):
        func = Parser.create_function('function ReturnValue* name()')
        self.assertEqual(func.return_type.type, 'ReturnValue')
        self.assertTrue(func.return_type.is_pointer)
        
        
class TestParseArguments(unittest.TestCase):
    
    def _test_args_on_linked(self, func, name, type_of_object):
        self.assertTrue(func.args[0][0] == name)
        self.assertTrue(isinstance(func.args[0][1], Object))
        self.assertEqual(func.args[0][1].type, type_of_object)

    def test_0(self):
        func = Parser.create_function('function void name(int i)')
        self._test_args_on_linked(func, 'i', 'int')
        
    def test_1(self):
        func = Parser.create_function('function void name(int i=0)')
        self._test_args_on_linked(func, 'i', 'int')

    def test_2(self):
        func = Parser.create_function('function void name(map<string, int> some_map)')
        self._test_args_on_linked(func, 'some_map', 'map')

    def test_3(self):
        func = Parser.create_function('function void name(map<int, ReturnValue*>:const some_map)')
        self._test_args_on_linked(func, 'some_map', 'map')


if __name__ == '__main__':
    unittest.main()