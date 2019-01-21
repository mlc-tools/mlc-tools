import unittest

import os
import sys
import inspect

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/..'))
from mlc_tools.base.parser import *
from mlc_tools.core.object import *


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


class TestParseTemplates(unittest.TestCase):

    def test_parse(self):
        func = Parser.create_function('function<T> T add(T a, T b)')
        self.assertEqual(func.name, 'add')
        self.assertEqual(func.args[0][0], 'a')
        self.assertEqual(func.args[0][1].type, 'T')
        self.assertEqual(func.args[1][0], 'b')
        self.assertEqual(func.args[1][1].type, 'T')
        self.assertEqual(func.return_type.type, 'T')
        self.assertEqual(len(func.return_type.template_args), 0)
        self.assertEqual(len(func.template_args), 1)
        self.assertEqual(func.template_args[0], 'T')

    def test_1(self):
        func = Parser.create_function('function bool std_functions(Logger* logger):static')
        self.assertEqual(func.name, 'std_functions')


if __name__ == '__main__':
    unittest.main()
