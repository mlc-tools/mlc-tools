import unittest

import os
import sys
import inspect

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/..'))
from mlc_tools.core.function import *
from mlc_tools.base.parser import Parser
from mlc_tools.base.model import Model


class TestParseObject(unittest.TestCase):

    def test_1(self):
        parser = Parser(Model())
        text = 'map<int, list<Foo>> some_map'
        parser.parse_text(text)
        obj = parser.model.objects[0]
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

    def test_observable_parse(self):
        parser = Parser(Model())

        text = 'void()'
        parser.parse_text(text)
        obj = parser.model.objects[0]
        self.assertEqual(obj.type, 'void')
        self.assertEqual(len(obj.callable_args), 0)

        parser.model.objects = []
        text = 'void(int)'
        parser.parse_text(text)
        obj = parser.model.objects[0]
        self.assertEqual(obj.type, 'void')
        self.assertEqual(len(obj.callable_args), 1)
        self.assertTrue(isinstance(obj.callable_args[0], Object))
        self.assertEqual(obj.callable_args[0].type, 'int')
        self.assertIsNotNone(obj.callable_args)

        parser.model.objects = []
        text = 'Observable<void()> eventTest'
        parser.parse_text(text)
        obj = parser.model.objects[0]
        self.assertEqual(obj.type, 'Observable')
        self.assertEqual(obj.name, 'eventTest')
        self.assertEqual(len(obj.template_args), 1)
        self.assertEqual(obj.template_args[0].type, 'void')
        self.assertEqual(len(obj.template_args[0].callable_args), 0)
        self.assertIsNotNone(obj.template_args[0].callable_args)

        parser.model.objects = []
        text = 'Observable<void(int, int)> eventTest'
        parser.parse_text(text)
        obj = parser.model.objects[0]
        self.assertEqual(obj.type, 'Observable')
        self.assertEqual(obj.name, 'eventTest')
        self.assertEqual(len(obj.template_args), 1)
        self.assertEqual(obj.template_args[0].type, 'void')
        self.assertEqual(len(obj.template_args[0].callable_args), 2)
        self.assertEqual(obj.template_args[0].callable_args[0].type, 'int')
        self.assertEqual(obj.template_args[0].callable_args[1].type, 'int')
        self.assertIsNotNone(obj.template_args[0].callable_args)

        parser.model.objects = []
        text = 'Observable<void(DataUnit:link)> eventTest'
        parser.parse_text(text)
        obj = parser.model.objects[0]
        self.assertEqual(obj.type, 'Observable')
        self.assertEqual(obj.name, 'eventTest')
        self.assertEqual(len(obj.template_args), 1)
        self.assertEqual(obj.template_args[0].type, 'void')
        self.assertEqual(len(obj.template_args[0].callable_args), 1)
        self.assertEqual(obj.template_args[0].callable_args[0].type, 'DataUnit')
        self.assertEqual(obj.template_args[0].callable_args[0].is_link, True)
        self.assertIsNotNone(obj.template_args[0].callable_args)

    def test_observable_parse_with_arg(self):
        parser = Parser(Model())
        text = 'void(int)'
        parser.parse_text(text)
        obj = parser.model.objects[0]
        self.assertEqual(obj.type, 'void')


class TestParseFunction(unittest.TestCase):

    def test_1(self):
        parser = Parser(Model())
        text = 'function map<int, list<Foo>> some_function(map<float, list<Bar>> arg0, list<int> arg1){}'
        parser.parse_text(text)
        func = parser.model.functions[0]
        self.assertTrue(isinstance(func, Function))
        self.assertEqual(func.name, 'some_function')
        self.assertEqual(len(func.args), 2)
        self.assertEqual(len(func.operations), 0)

        self.assertTrue(isinstance(func.return_type, Object))
        self.assertEqual(func.return_type.type, 'map')
        self.assertEqual(func.return_type.name, '')
        self.assertEqual(len(func.return_type.template_args), 2)
        self.assertTrue(isinstance(func.return_type.template_args[0], Object))
        self.assertTrue(isinstance(func.return_type.template_args[1], Object))
        self.assertEqual(func.return_type.template_args[0].name, '')
        self.assertEqual(func.return_type.template_args[0].type, 'int')
        self.assertEqual(func.return_type.template_args[1].name, '')
        self.assertEqual(func.return_type.template_args[1].type, 'list')
        self.assertEqual(len(func.return_type.template_args[1].template_args), 1)
        self.assertTrue(isinstance(func.return_type.template_args[1].template_args[0], Object))
        self.assertEqual(func.return_type.template_args[1].template_args[0].name, '')
        self.assertEqual(func.return_type.template_args[1].template_args[0].type, 'Foo')

        self.assertEqual(func.args[0][0], 'arg0')
        self.assertEqual(func.args[1][0], 'arg1')
        self.assertTrue(isinstance(func.args[0][1], Object))
        self.assertTrue(isinstance(func.args[1][1], Object))
        self.assertEqual(func.args[0][1].name, 'arg0')
        self.assertEqual(func.args[0][1].type, 'map')
        self.assertTrue(isinstance(func.args[0][1].template_args[0], Object))
        self.assertTrue(isinstance(func.args[0][1].template_args[1], Object))
        self.assertEqual(func.args[1][1].name, 'arg1')
        self.assertEqual(func.args[1][1].type, 'list')
        self.assertTrue(isinstance(func.args[0][1].template_args[0], Object))

    def test_2(self):
        text = 'function void visit(Request* ctx)'
        parser = Parser(Model())
        parser.parse_text(text)
        func = parser.model.functions[0]
        self.assertTrue(isinstance(func.return_type, Object))
        self.assertEqual(func.return_type.type, 'void')
        self.assertEqual(func.return_type.name, '')

    def test_3(self):
        parser = Parser(Model())
        parser.parse_text('function void initialize(ModelUser*user){}')
        func = parser.model.functions[0]
        self.assertEqual(func.args[0][0], 'user')
        self.assertEqual(func.args[0][1].type, 'ModelUser')

    def test_4(self):
        parser = Parser(Model())
        parser.parse_text('function DataAbility*:link get_non_random_ability():const:client')
        func = parser.model.functions[0]
        self.assertEqual(func.return_type.type, 'DataAbility')
        self.assertEqual(func.return_type.is_link, True)


class TestParseClass(unittest.TestCase):

    def test_1(self):
        text = '''
        class Foo
        {
            int int_name
            float float_name
            Bar bar_name

            string:const:static INAPP = "inapp"

            function void function_1(int a){}
            function map<int, int> function_2(list<int> a){}
        }
        '''
        parser = Parser(Model())
        parser.parse_text(text)
        foo = parser.model.classes[0]
        self.assertEqual(foo.name, 'Foo')
        self.assertEqual(foo.type, 'class')
        self.assertEqual(len(foo.members), 4)

        self.assertEqual(foo.members[0].type, 'int')
        self.assertEqual(foo.members[0].name, 'int_name')

        self.assertEqual(foo.members[3].type, 'string')
        self.assertEqual(foo.members[3].name, 'INAPP')

    def test_2(self):
        text = '''
        class RewardsListHelper
        {
            list<DataReward*> rewards
        }
        '''
        parser = Parser(Model())
        parser.parse_text(text)
        foo = parser.model.classes[0]
        self.assertEqual(foo.name, 'RewardsListHelper')
        self.assertEqual(foo.type, 'class')
        self.assertEqual(len(foo.members), 1)

    def test_3(self):
        text = '''
        class RewardsListHelper
        {
            constructor()
            {
            }
        }
        '''
        parser = Parser(Model())
        parser.parse_text(text)
        foo = parser.model.classes[0]
        self.assertEqual(foo.name, 'RewardsListHelper')
        self.assertEqual(foo.type, 'class')
        self.assertIsNotNone(foo.constructor)
        self.assertEqual(foo.constructor.args, [])

    def test_4(self):
        text = '''
        class RewardsListHelper
        {
            constructor(int a=0, float b=1)
            {
            }
        }
        '''
        parser = Parser(Model())
        parser.parse_text(text)
        foo = parser.model.classes[0]
        self.assertEqual(foo.name, 'RewardsListHelper')
        self.assertEqual(foo.type, 'class')
        self.assertIsNotNone(foo.constructor)
        self.assertEqual(len(foo.constructor.args), 2)
        self.assertTrue(isinstance(foo.constructor.args[0][1], Object))
        self.assertTrue(isinstance(foo.constructor.args[1][1], Object))
        self.assertEqual(foo.constructor.args[0][1].type, 'int')
        self.assertEqual(foo.constructor.args[1][1].type, 'float')
        self.assertEqual(foo.constructor.args[0][0], 'a')
        self.assertEqual(foo.constructor.args[1][0], 'b')
        self.assertEqual(foo.constructor.args[0][1].initial_value, '0')
        self.assertEqual(foo.constructor.args[1][1].initial_value, '1')

    def test_5(self):
        text = '''
        class RewardsListHelper
        {
            int a
            float b
            
            constructor():generate
        }
        '''
        parser = Parser(Model())
        parser.parse_text(text)
        foo = parser.model.classes[0]
        self.assertEqual(foo.name, 'RewardsListHelper')
        self.assertEqual(foo.type, 'class')
        self.assertIsNotNone(foo.constructor)
        self.assertEqual(foo.constructor.name, 'constructor')
        self.assertEqual(foo.constructor.return_type.type, 'void')

        self.assertEqual(len(foo.constructor.args), 2)
        self.assertTrue(isinstance(foo.constructor.args[0][1], Object))
        self.assertTrue(isinstance(foo.constructor.args[1][1], Object))
        self.assertEqual(foo.constructor.args[0][1].type, 'int')
        self.assertEqual(foo.constructor.args[1][1].type, 'float')
        self.assertEqual(foo.constructor.args[0][0], 'a')
        self.assertEqual(foo.constructor.args[1][0], 'b')
        self.assertEqual(foo.constructor.args[0][1].initial_value, '0')
        self.assertEqual(foo.constructor.args[1][1].initial_value, '0.0')


class TestParseFunctionArgs(unittest.TestCase):

    def test_arg_default_params(self):
        parser = Parser(Model())
        text = 'function ReturnValue& test_9(int i=0)'
        parser.parse_text(text)
        func = parser.model.functions[0]
        self.assertTrue(isinstance(func, Function))
        self.assertEqual(func.name, 'test_9')
        self.assertEqual(len(func.args), 1)
        self.assertEqual(len(func.operations), 0)

        arg = func.args[0][1]
        self.assertTrue(isinstance(arg, Object))
        self.assertEqual(arg.type, 'int')
        self.assertEqual(arg.initial_value, '0')

    def test_arg_count_3(self):
        parser = Parser(Model())
        text = 'function ReturnValue& test_9(int a, int b, int c)'
        parser.parse_text(text)
        func = parser.model.functions[0]
        self.assertEqual(len(func.args), 3)

        self.assertTrue(isinstance(func.args[0][1], Object))
        self.assertEqual(func.args[0][0], 'a')
        self.assertEqual(func.args[0][1].type, 'int')

        self.assertTrue(isinstance(func.args[1][1], Object))
        self.assertEqual(func.args[1][0], 'b')
        self.assertEqual(func.args[1][1].type, 'int')

        self.assertTrue(isinstance(func.args[2][1], Object))
        self.assertEqual(func.args[2][0], 'c')
        self.assertEqual(func.args[2][1].type, 'int')


if __name__ == '__main__':
    unittest.main()
