import unittest

import os
import sys
import inspect

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/..'))
from mlc_tools.core.Object import *
from mlc_tools.core.Function import *
from mlc_tools.base.Parser import Parser


class TestParseObject(unittest.TestCase):
    
    def test_1(self):
        parser = Parser('client')
        text = 'map<int, list<Foo>> some_map'
        parser.parse_text(text)
        obj = parser.objects[0]
        self.assertTrue(isinstance(obj, Object))
        self.assertEqual(obj.type, 'map')
        self.assertEqual(obj.name, 'some_map')
        self.assertTrue(len(obj.template_args), 2)
        self.assertTrue(isinstance(obj.template_args[0], Object))
        self.assertTrue(isinstance(obj.template_args[1], Object))
        self.assertEqual(obj.template_args[0].type, 'int')
        self.assertEqual(obj.template_args[0].name, '')
        self.assertEqual(obj.template_args[1].type, 'list')
        self.assertEqual(obj.template_args[1].name, '')
        self.assertTrue(len(obj.template_args[1].template_args), 1)
        self.assertTrue(isinstance(obj.template_args[1].template_args[0], Object))
        self.assertEqual(obj.template_args[1].template_args[0].type, 'Foo')
        self.assertEqual(obj.template_args[1].template_args[0].name, '')


# class TestParseFunction(unittest.TestCase):
    
    # def test_1(self):
    #     parser = Parser('client')
    #     text = 'function map<int, list<Foo>> some_function(map<float, list<Bar>> arg0, list<int> arg1){}'
    #     parser.parse_text(text)
    #     func = parser.functions[0]
    #     self.assertTrue(isinstance(func, Function))
    #     self.assertEqual(func.name, 'some_function')
    #     self.assertEqual(len(func.args), 2)
    #
    #     self.assertTrue(isinstance(func.return_type, Object))
    #     self.assertEqual(func.return_type.type, 'map')
    #     self.assertEqual(func.return_type.name, '')
    #     self.assertEqual(len(func.return_type.template_args), 2)
    #     self.assertTrue(isinstance(func.return_type.template_args[0], Object))
    #     self.assertTrue(isinstance(func.return_type.template_args[1], Object))
    #     self.assertEqual(func.return_type.template_args[0].name, '')
    #     self.assertEqual(func.return_type.template_args[0].type, 'int')
    #     self.assertEqual(func.return_type.template_args[1].name, '')
    #     self.assertEqual(func.return_type.template_args[1].type, 'list')
    #     self.assertEqual(len(func.return_type.template_args[1].template_args), 1)
    #     self.assertTrue(isinstance(func.return_type.template_args[1].template_args[0], Object))
    #     self.assertEqual(func.return_type.template_args[1].template_args[0].name, '')
    #     self.assertEqual(func.return_type.template_args[1].template_args[0].type, 'Foo')



if __name__ == '__main__':
    unittest.main()