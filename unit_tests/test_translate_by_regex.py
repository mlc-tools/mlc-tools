import unittest

import os
import sys
import inspect

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/..'))
from mlc_tools.module_cpp.translator import Translator as t_cpp
from mlc_tools.module_python.translator import Translator as t_py
from mlc_tools.module_php.translator import Translator as t_php
from mlc_tools.module_js.translator import Translator as t_js
from mlc_tools.core.function import Function
from mlc_tools.base.model import Model


class Test(unittest.TestCase):

    def test_simple(self):
        func = Function()
        model = Model()
        args = []

        body = 'auto foo = value ?? defaultValue'
        self.assertEqual(t_cpp().replace_by_regex(func, body, model, args), 'auto foo = (value != nullptr) ? value : (defaultValue)')
        self.assertEqual(t_py().replace_by_regex(func, body, model, args), 'foo = (value) if (value is not None) else (defaultValue)')
        self.assertEqual(t_php().replace_by_regex(func, body, model, args), '$foo = (value) ?? (defaultValue)')
        self.assertEqual(t_js().replace_by_regex(func, body, model, args), 'let foo = ((value) !== null && (value) !== undefined) ? (value) : (defaultValue)')

        body = 'Foo* foo = value->data.foo ?? defaultValue->data.foo'
        self.assertEqual(t_cpp().replace_by_regex(func, body, model, args), 'Foo* foo = (value->data.foo != nullptr) ? value->data.foo : (defaultValue->data.foo)')
        self.assertEqual(t_py().replace_by_regex(func, body, model, args), 'foo = (value.data.foo) if (value.data.foo is not None) else (defaultValue.data.foo)')
        self.assertEqual(t_php().replace_by_regex(func, body, model, args), '$foo = (value->data->foo) ?? (defaultValue->data->foo)')
        self.assertEqual(t_js().replace_by_regex(func, body, model, args), 'let foo = ((value.data.foo) !== null && (value.data.foo) !== undefined) ? (value.data.foo) : (defaultValue.data.foo)')


if __name__ == '__main__':
    unittest.main()
