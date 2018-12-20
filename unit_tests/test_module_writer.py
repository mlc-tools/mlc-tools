import unittest

import os
import sys
import inspect

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/..'))
from mlc_tools.core.object import Object, Objects
from mlc_tools.core.class_ import *
from mlc_tools.core.function import *
from mlc_tools.base.model import Model
from mlc_tools.base.language import Language
from mlc_tools.base.linker import Linker
from mlc_tools.base.validator import Validator


def create_test_model():
    cls = Class()
    cls.name = 'Test'

    m = Object()
    m.type = 'int'
    m.name = 'int_value'
    m.initial_value = '42'
    cls.members.append(m)

    f = Function()
    f.name = 'foo'
    f.return_type = Object()
    f.return_type.type = 'int'
    f.args = [['a0', Objects.INT], ['a1', Objects.STRING]]
    f.operations = [
        'auto result = this->int_value;\n'
        'result += a0;\n'
        'return result;\n'
    ]
    cls.functions.append(f)

    model = Model()
    # model.parser = Parser(model)
    model.classes.append(cls)
    model.out_directory = '/Users/stereo7/mlc_tools_temp/'
    model.generate_tests = False
    model.generate_factory = False
    model.generate_intrusive = False
    model.out_dict = {}
    return model


def create_lang(lang, model):
    model.language = lang
    language = Language(lang, model)
    language.get_generator().generate(model, language.get_writer())

    Linker().link(model)
    Validator().validate(model)

    language.get_translator().translate(model)
    return language


def save(lang, model):
    create_lang(lang, model).get_writer().save(model)


def save_object(lang, model):
    cls = model.get_class('Test')
    writer = create_lang(lang, model).get_writer()
    writer.current_cls = cls
    return writer.write_object(cls.members[0])


def save_function(lang, model):
    cls = model.get_class('Test')
    writer = create_lang(lang, model).get_writer()
    writer.current_cls = cls
    return writer.write_function(cls.functions[0])


class TestWriteClass(unittest.TestCase):

    def test_cpp(self):
        model = create_test_model()
        save('cpp', model)

        self.assertTrue('Test.h' in model.out_dict)
        self.assertTrue('Test.cpp' in model.out_dict)

        hpp = model.out_dict['Test.h']
        cpp = model.out_dict['Test.cpp']
        self.assertEquals(cpp, get_cpp())
        self.assertEquals(hpp, get_hpp())


class TestWriteObject(unittest.TestCase):

    def test_cpp(self):
        model = create_test_model()
        result = save_object('cpp', model)
        self.assertEquals(result, ('int int_value;', 'int_value(42)', ''))

    def test_python(self):
        model = create_test_model()
        result = save_object('py', model)
        self.assertEquals(result, 'self.int_value = 42')

    def test_php(self):
        model = create_test_model()
        result = save_object('php', model)
        self.assertEquals(result, ('public $int_value = 42;', ''))


class TestWriteFunction(unittest.TestCase):

    def test_cpp(self):
        model = create_test_model()
        result = save_function('cpp', model)
        hpp = 'int foo(int a0, const std::string& a1);\n'
        cpp = '''int Test::foo(int a0, const std::string& a1)
        {
        auto result = this->int_value;
result += a0;
return result;

        }
        \n        '''
        self.assertEquals(result[0], hpp)
        self.assertEquals(result[1], cpp)

    def test_python(self):
        model = create_test_model()
        result = save_function('py', model)
        self.assertEquals(result, '\n    def foo(self, a0, a1):\n        result = self.int_value\n        result += a0\n        return result\n        \n        pass\n')

    def test_php(self):
        model = create_test_model()
        result = save_function('php', model)
        self.assertEquals(result, 'function foo($a0, $a1)\n{\n    $result = $this->int_value;\n$result += $a0;\nreturn $result;\n\n}\n')


def get_cpp():
    return '''#include "intrusive_ptr.h"
#include "mg_Factory.h"
#include "Test.h"
#include <string>
#include "mg_extensions.h"

namespace mg
{
    const std::string Test::TYPE("Test");

    REGISTRATION_OBJECT(Test);

    Test::Test()
    : int_value(42)
    {
    }

    Test::~Test()
    {
    }

    int Test::foo(int a0, const std::string& a1)
    {
        auto result = this->int_value;
        result += a0;
        return result;

    }

    bool Test::operator ==(const Test& rhs) const
    {
        bool result = true;
        result = result && int_value == rhs.int_value;
        return result;
    }

    bool Test::operator !=(const Test& rhs) const
    {
        bool result = false;
        result = result || int_value != rhs.int_value;
        return result;
    }

    std::string Test::get_type() const
    {
        return Test::TYPE;
    }

} //namespace mg
'''


def get_hpp():
    return '''#ifndef __mg_Test_h__
#define __mg_Test_h__

#include "intrusive_ptr.h"
#include "pugixml/pugixml.hpp"
#include <string>

namespace mg
{

    class Test
    {
    public:
        Test();
        ~Test();
        int foo(int a0, const std::string& a1);
        bool operator ==(const Test& rhs) const;
        bool operator !=(const Test& rhs) const;
        std::string get_type() const;

        int int_value;
        static const std::string TYPE;

    };
} //namespace mg

#endif //#ifndef __mg_Test_h__
'''


if __name__ == '__main__':
    unittest.main()
