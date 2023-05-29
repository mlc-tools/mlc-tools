import unittest

import os
import sys
import inspect

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/..'))
from mlc_tools.core.object import Object, Objects
from mlc_tools.core.class_ import *
from mlc_tools.core.function import *
from mlc_tools.base.model import Model
from mlc_tools.base.parser import Parser
from mlc_tools.base.language import Language
from mlc_tools.base.linker import Linker
from mlc_tools.base.validator import Validator


def create_test_model(with_ctr=False):
    cls = Class()
    cls.name = 'Test'

    m = Object()
    m.type = 'int'
    m.name = 'int_value'
    m.initial_value = '42'
    cls.members.append(m)

    m = Parser.create_object('list<string>:static test_list')
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

    if with_ctr:
        ctr = Function()
        ctr.name = 'const'
        ctr.name += 'ructor'
        ctr.return_type = Object()
        ctr.args = []
        ctr.operations = ['this->int_value = 1;']
        cls.functions.append(ctr)
        cls.generate_constructor()

    model = Model()
    # model.parser = Parser(model)
    model.add_class(cls)
    model.out_directory = '/Users/stereo7/mlc_tools_temp/'
    model.generate_tests = False
    model.generate_factory = False
    model.generate_intrusive = False
    model.generate_ref_counter = True
    model.out_dict = {}
    return model


def create_lang(lang, model):
    model.language = lang
    language = Language(lang, model)
    language.get_generator().generate(model)

    Linker().link(model)
    Validator().validate(model)

    language.get_translator().translate(model)
    return language


def save(lang, model):
    lang = create_lang(lang, model)
    lang.get_writer().save(model)
    lang.save_plugin.save_files()


def save_object(lang, model):
    cls = model.get_class('Test')
    writer = create_lang(lang, model).get_writer()
    writer.current_class = cls
    return writer.write_object(cls.members[0])


def save_function(lang, model):
    cls = model.get_class('Test')
    writer = create_lang(lang, model).get_writer()
    writer.current_class = cls
    return writer.write_function(cls.functions[0])


class TestWriteClass(unittest.TestCase):

    def test_cpp(self):
        model = create_test_model()
        model.generate_ref_counter = True
        save('cpp', model)

        self.assertTrue('Test.h' in model.out_dict)
        self.assertTrue('Test.cpp' in model.out_dict)

        hpp = model.out_dict['Test.h']
        cpp = model.out_dict['Test.cpp']
        self.assertEqual(cpp, get_cpp(False))
        self.assertEqual(hpp, get_hpp())

    def test_cpp_with_ctr(self):
        model = create_test_model(True)
        save('cpp', model)

        self.assertTrue('Test.h' in model.out_dict)
        self.assertTrue('Test.cpp' in model.out_dict)

        hpp = model.out_dict['Test.h']
        cpp = model.out_dict['Test.cpp']
        self.assertEqual(cpp, get_cpp(True))
        self.assertEqual(hpp, get_hpp())


class TestWriteObject(unittest.TestCase):

    def test_cpp(self):
        model = create_test_model()
        result = save_object('cpp', model)
        self.assertEqual(result, ('int int_value;', 'int_value(42)', ''))

    def test_python(self):
        model = create_test_model()
        result, imports = save_object('py', model)
        self.assertEqual(result, 'self.int_value = 42')
        self.assertEqual(imports, [])

    def test_php(self):
        model = create_test_model()
        result = save_object('php', model)
        self.assertEqual(result, ('public $int_value = 42;', ''))


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
        self.assertEqual(result[0], hpp)
        self.assertEqual(result[1], cpp)

    def test_python(self):
        model = create_test_model()
        result = save_function('py', model)
        self.assertEqual(result, '\n    def foo(self, a0, a1):\n        result = self.int_value\n        result += a0\n        return result\n        \n')

    def test_php(self):
        model = create_test_model()
        result = save_function('php', model)
        self.assertEqual(result, 'public function foo(int $a0, string $a1)\n{\n    $result = $this->int_value;\n$result += $a0;\nreturn $result;\n\n}\n')


class TestCppWriterBuildIncludesWithGroups(unittest.TestCase):

    def test_build_include(self):
        from mlc_tools.module_cpp.writer import Writer
        cls1 = Class()
        cls1.name = 'cls1'
        cls2 = Class()
        cls2.name = 'cls2'

        cls1.group = ''
        cls2.group = ''
        self.assertEqual(Writer.get_include_path_to_class(cls1, cls2), '"cls2.h"')
        cls1.group = 'a'
        cls2.group = ''
        self.assertEqual(Writer.get_include_path_to_class(cls1, cls2), '"../cls2.h"')
        cls1.group = ''
        cls2.group = 'a'
        self.assertEqual(Writer.get_include_path_to_class(cls1, cls2), '"a/cls2.h"')
        cls1.group = 'a'
        cls2.group = 'a'
        self.assertEqual(Writer.get_include_path_to_class(cls1, cls2), '"cls2.h"')
        cls1.group = 'a'
        cls2.group = 'b'
        self.assertEqual(Writer.get_include_path_to_class(cls1, cls2), '"../b/cls2.h"')

    def test_get_path_to_root(self):
        from mlc_tools.module_cpp.writer import Writer
        cls = Class()
        cls.name = 'cls'

        cls.group = 'b'
        self.assertEqual(Writer.get_path_to_root(cls), '../')
        cls.group = ''
        self.assertEqual(Writer.get_path_to_root(cls), '')

    def test_get_includes_for_header_cpp(self):
        from mlc_tools.module_cpp.writer import Writer
        # get_includes_for_header
        cls = Class()
        cls.name = 'cls'

        method = Parser.create_function('function void assertInMap(int key, map<int, int>:const:ref map)')
        cls.functions.append(method)

        writer = Writer('')
        writer.model = Model()
        includes, f, f_out = writer.get_includes_for_header(cls)
        self.assertIn('std::map', includes, '<map> in includes')


class TestCppWriterWriteObject(unittest.TestCase):

    def test_0(self):
        from mlc_tools.module_cpp.writer import Writer
        model = create_test_model()
        lang = create_lang('cpp', model)
        writer = lang.get_writer()

        member = Parser.create_object('DataBase*:static db')
        model.classes[0].members.append(member)

        self.assertEqual(writer.write_member_declaration(member), 'static intrusive_ptr<DataBase> db;')
        self.assertEqual(writer.write_member_static_init(model.classes[0], member),
                         'intrusive_ptr<DataBase> Test::db(nullptr);')


class TestWriterPrepareFile(unittest.TestCase):

    def test_xml(self):
        from mlc_tools.base.model import SerializeFormat
        writer = self.create_writer()
        writer.model.serialize_formats = SerializeFormat.xml
        text = writer.prepare_file(TestWriterPrepareFile.get_text())
        self.assertIn('xml_functional', text)
        self.assertNotIn('json_functional', text)
        self.assertNotIn('both_functional', text)
        self.assertNotIn('format=', text)

    def test_json(self):
        from mlc_tools.base.model import SerializeFormat
        writer = self.create_writer()
        writer.model.serialize_formats = SerializeFormat.json
        text = writer.prepare_file(TestWriterPrepareFile.get_text())
        self.assertNotIn('xml_functional', text)
        self.assertIn('json_functional', text)
        self.assertNotIn('both_functional', text)
        self.assertNotIn('format=', text)

    def test_both(self):
        from mlc_tools.base.model import SerializeFormat
        writer = self.create_writer()
        writer.model.serialize_formats = SerializeFormat.xml | SerializeFormat.json
        text = writer.prepare_file(TestWriterPrepareFile.get_text())
        self.assertNotIn('xml_functional', text)
        self.assertNotIn('json_functional', text)
        self.assertIn('both_functional', text)
        self.assertNotIn('format=', text)

    @staticmethod
    def create_writer():
        from mlc_tools.base.writer_base import WriterBase
        writer = WriterBase('')
        writer.model = Model()
        writer.model.generate_ref_counter = True
        return writer

    @staticmethod
    def get_text():
        text = '''
        {{format=xml}}xml_functional{{end_format=xml}}
        {{format=json}}json_functional{{end_format=json}}
        {{format=both}}both_functional{{end_format=both}}
        '''
        return text


def get_cpp(with_ctr):
    return '''#include "intrusive_ptr.h"
#include "mg_Factory.h"
#include "Test.h"
#include <string>
#include "mg_extensions.h"
#include "SerializerJson.h"
#include "SerializerXml.h"

namespace mg
{
    std::vector<std::string> Test::test_list;
    const std::string Test::TYPE("Test");

    REGISTRATION_OBJECT(Test);

    Test::Test()
    : int_value(42)
    , _reference_counter(1)
    {
{ctr}
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
        result = result && this->int_value == rhs.int_value;
        return result;
    }

    bool Test::operator !=(const Test& rhs) const
    {
        return !(*this == rhs);
    }

    void Test::retain()
    {
        this->_reference_counter += 1;
    }

    int Test::release()
    {
        this->_reference_counter -= 1;
        auto counter = this->_reference_counter;
        if(counter == 0)
        delete this;
        return counter;
    }

    std::string Test::get_type() const
    {
        return Test::TYPE;
    }

} //namespace mg
'''.replace('{ctr}', '        this->int_value = 1;' if with_ctr else '')


def get_hpp():
    return '''#ifndef __mg_Test_h__
#define __mg_Test_h__

#include <cstdint>
#include "intrusive_ptr.h"
#include "pugixml/pugixml.hpp"
#include <string>
#include <vector>

namespace mg
{
    class SerializerXml;
    class DeserializerXml;
    class SerializerJson;
    class DeserializerJson;

    class Test
    {
    public:
        Test();
        ~Test();
        int foo(int a0, const std::string& a1);
        bool operator ==(const Test& rhs) const;
        bool operator !=(const Test& rhs) const;
        void retain();
        int release();
        std::string get_type() const;

        int int_value;
        static std::vector<std::string> test_list;
    private:
        int _reference_counter;
    public:
        static const std::string TYPE;

    };
} //namespace mg

#endif //#ifndef __mg_Test_h__
'''


def get_hpp_with_ctr():
    return ''''''


if __name__ == '__main__':
    unittest.main()
