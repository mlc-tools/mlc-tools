import unittest
from mlc_tools.base.model import Model
from mlc_tools.core.class_ import Class

class TestModel(unittest.TestCase):

    def setUp(self):
        self.model = Model()

    def test_empty_copy(self):
        new_model = self.model.empty_copy()
        self.assertNotEqual(id(new_model), id(self.model))
        self.assertEqual(new_model.classes, [])
        self.assertEqual(new_model.classes_for_data, [])
        self.assertEqual(new_model.objects, [])
        self.assertEqual(new_model.functions, [])
        self.assertEqual(new_model.classes_dict, {})

    def test_clear_data(self):
        self.model.parser = 'some_parser'
        self.model.classes = ['some_class']
        self.model.classes_for_data = ['some_class_for_data']
        self.model.objects = ['some_object']
        self.model.functions = ['some_function']
        self.model.classes_dict = {'some_class': Class('some_class')}

        self.model.clear_data()

        self.assertIsNone(self.model.parser)
        self.assertEqual(self.model.classes, [])
        self.assertEqual(self.model.classes_for_data, [])
        self.assertEqual(self.model.objects, [])
        self.assertEqual(self.model.functions, [])
        self.assertEqual(self.model.classes_dict, {})
        self.assertIsNone(self.model.out_dict)
        self.assertEqual(self.model.files, [])
        self.assertEqual(self.model.created_files, [])

    def test_add_class(self):
        cls = Class('TestClass')
        self.model.add_class(cls)
        self.assertEqual(len(self.model.classes), 1)
        self.assertEqual(self.model.classes[0], cls)
        self.assertEqual(len(self.model.classes_dict), 1)
        self.assertEqual(self.model.classes_dict['TestClass'], cls)

    def test_add_classes(self):
        classes = [Class('TestClass1'), Class('TestClass2')]
        self.model.add_classes(classes)
        self.assertEqual(len(self.model.classes), 2)
        self.assertEqual(self.model.classes[0], classes[0])
        self.assertEqual(self.model.classes[1], classes[1])
        self.assertEqual(len(self.model.classes_dict), 2)
        self.assertEqual(self.model.classes_dict['TestClass1'], classes[0])
        self.assertEqual(self.model.classes_dict['TestClass2'], classes[1])

    def test_get_class(self):
        cls = Class('TestClass')
        self.model.add_class(cls)
        self.assertEqual(self.model.get_class('TestClass'), cls)

    def test_has_class(self):
        cls = Class('TestClass')
        self.model.add_class(cls)
        self.assertTrue(self.model.has_class('TestClass'))
        self.assertFalse(self.model.has_class('NonExistentClass'))

    def test_is_side(self):
        self.model.side = 'server'
        self.assertTrue(self.model.is_side('server'))
        self.assertFalse(self.model.is_side('client'))
        self.assertTrue(self.model.is_side('both'))

    def test_is_lang(self):
        self.model.language = 'py'
        self.assertTrue(self.model.is_lang('py'))
        self.assertFalse(self.model.is_lang('cpp'))
        self.assertTrue(self.model.is_lang(None))
