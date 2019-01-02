import unittest

import os
import sys
import inspect

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/..'))
from mlc_tools.core.object import *
from mlc_tools.base.parser import Parser
from mlc_tools.base.model import Model


class TestParseModifiersTypes(unittest.TestCase):

    def test_1(self):
        obj = Parser.create_object('int:client')
        self.assertEqual(obj.side, 'client')

    def test_2(self):
        obj = Parser.create_object('int:server')
        self.assertEqual(obj.side, 'server')

    def test_3(self):
        obj = Parser.create_object('int*')
        self.assertTrue(obj.is_pointer)

    def test_4(self):
        obj = Parser.create_object('int&')
        self.assertTrue(obj.is_ref)

    def test_5(self):
        obj = Parser.create_object('int:runtime')
        self.assertTrue(obj.is_runtime)

    def test_6(self):
        obj = Parser.create_object('int:static')
        self.assertTrue(obj.is_static)

    def test_7(self):
        obj = Parser.create_object('int:const')
        self.assertTrue(obj.is_const)

    def test_8(self):
        obj = Parser.create_object('int:key')
        self.assertTrue(obj.is_key)

    def test_9(self):
        obj = Parser.create_object('int:link')
        self.assertTrue(obj.is_link)

    def test_10(self):
        obj = Parser.create_object('int:private')
        self.assertTrue(obj.access == AccessSpecifier.private)

    def test_11(self):
        obj = Parser.create_object('int:protected')
        self.assertTrue(obj.access == AccessSpecifier.protected)

    def test_12(self):
        obj = Parser.create_object('int:public')
        self.assertTrue(obj.access == AccessSpecifier.public)


class TestParseComplexTypes(unittest.TestCase):
    
    def test_1(self):
        obj = Parser.create_object('int key')
        self.assertEqual(obj.type, 'int')
        self.assertEqual(obj.name, 'key')
        self.assertEqual(obj.template_args, [])
        self.assertFalse(obj.is_pointer)
        self.assertFalse(obj.is_ref)
        self.assertFalse(obj.is_runtime)
        self.assertFalse(obj.is_static)
        self.assertFalse(obj.is_const)
        self.assertFalse(obj.is_key)
        self.assertFalse(obj.is_link)
        self.assertEqual(obj.side, 'both')
        self.assertEqual(obj.access, AccessSpecifier.public)

    def test_2(self):
        obj = Parser.create_object('DataStorage&:static')
        self.assertEqual(obj.type, 'DataStorage')
        self.assertEqual(obj.name, '')
        self.assertEqual(obj.template_args, [])
        self.assertFalse(obj.is_pointer)
        self.assertTrue(obj.is_ref)
        self.assertFalse(obj.is_runtime)
        self.assertTrue(obj.is_static)
        self.assertFalse(obj.is_const)
        self.assertFalse(obj.is_key)
        self.assertFalse(obj.is_link)
        self.assertEqual(obj.side, 'both')
        self.assertEqual(obj.access, AccessSpecifier.public)

    def test_3(self):
        obj = Parser.create_object('list<int>:static name')
        self.assertEqual(obj.type, 'list')
        self.assertEqual(obj.name, 'name')
        self.assertEqual(obj.template_args[0].type, 'int')
        self.assertFalse(obj.is_pointer)
        self.assertFalse(obj.is_ref)
        self.assertFalse(obj.is_runtime)
        self.assertTrue(obj.is_static)
        self.assertFalse(obj.is_const)
        self.assertFalse(obj.is_key)
        self.assertFalse(obj.is_link)
        self.assertEqual(obj.side, 'both')
        self.assertEqual(obj.access, AccessSpecifier.public)
    
    def test_4(self):
        obj = Parser.create_object('map<string, list<int>:static>:const name')
        self.assertEqual(obj.type, 'map')
        self.assertEqual(obj.name, 'name')
        self.assertEqual(obj.template_args[0].type, 'string')
        self.assertEqual(obj.template_args[1].type, 'list')
        self.assertTrue(obj.template_args[1].is_static)
        self.assertFalse(obj.is_pointer)
        self.assertFalse(obj.is_ref)
        self.assertFalse(obj.is_runtime)
        self.assertFalse(obj.is_static)
        self.assertTrue(obj.is_const)
        self.assertFalse(obj.is_key)
        self.assertFalse(obj.is_link)
        self.assertEqual(obj.side, 'both')
        self.assertEqual(obj.access, AccessSpecifier.public)


class TestParserOther(unittest.TestCase):

    def test_1(self):
        parser = Parser(Model())
        
        parser.model.language = 'cpp'
        self.assertTrue(parser.check_skip('function bool test(Logger* logger):static:py:php')[0])
        self.assertFalse(parser.check_skip('function bool test(Logger* logger):static:py:cpp')[0])
        self.assertFalse(parser.check_skip('function bool test(Logger* logger):static:cpp')[0])
        self.assertTrue(parser.check_skip('function bool test(Logger* logger):static:php')[0])
        self.assertTrue(parser.check_skip('function bool test(Logger* logger):static:py')[0])
        
        parser.model.language = 'py'
        self.assertFalse(parser.check_skip('function bool test(Logger* logger):static:py:php')[0])
        self.assertFalse(parser.check_skip('function bool test(Logger* logger):static:py:cpp')[0])
        self.assertTrue(parser.check_skip('function bool test(Logger* logger):static:cpp')[0])
        self.assertTrue(parser.check_skip('function bool test(Logger* logger):static:php')[0])
        self.assertFalse(parser.check_skip('function bool test(Logger* logger):static:py')[0])
        
        parser.model.language = 'php'
        self.assertFalse(parser.check_skip('function bool test(Logger* logger):static:py:php')[0])
        self.assertTrue(parser.check_skip('function bool test(Logger* logger):static:py:cpp')[0])
        self.assertTrue(parser.check_skip('function bool test(Logger* logger):static:cpp')[0])
        self.assertFalse(parser.check_skip('function bool test(Logger* logger):static:php')[0])
        self.assertTrue(parser.check_skip('function bool test(Logger* logger):static:py')[0])

    def test_2(self):
        parser = Parser(Model())
    
        parser.model.language = 'cpp'
        self.assertFalse(parser.check_skip('int:cpp test')[0])
        self.assertEqual(parser.check_skip('int:client:cpp test')[1], 'int:client test')
        
    def test_3(self):
        parser = Parser(Model())
    
        parser.model.language = 'cpp'
        parser.parse_text('list<int>:static:cpp name')
        obj = parser.model.objects[0]
        self.assertEqual(obj.type, 'list')
        self.assertEqual(obj.name, 'name')
    
        parser.model.language = 'py'
        parser.parse_text('list<int>:static:cpp name')
        obj = parser.model.objects[0]
        self.assertEqual(obj.type, 'list')
        self.assertEqual(obj.name, 'name')
        

if __name__ == '__main__':
    unittest.main()
