from ..base import WriterBase
from ..core.Object import *


class Writer(WriterBase):

    def __init__(self, out_directory):
        WriterBase.__init__(self, out_directory)
        pass

    def write_class(self, cls):
        header = self.write_hpp(cls)
        source = self.write_cpp(cls)
        return [
            (self.get_filename(cls, 'h'), self.prepare_file(header)),
            (self.get_filename(cls, 'cpp'), self.prepare_file(source)),
            ]

    def write_hpp(self, cls):
        namespace = 'mg'
        class_name = cls.name
        includes, forward_declarations, forward_declarations_out = self.get_includes_for_header(cls)
        functions = ''
        for method in cls.functions:
            functions += self.write_function_hpp(method)
        members = ''
        for member in cls.members:
            assert(isinstance(member.type, str))
            if cls.type == 'class':
                members += self.write_member_declaration(member)
            elif cls.type == 'enum':
                members += self.write_member_enum_declaration(member)

        virtual = 'virtual '
        if not cls.is_virtual and len(cls.superclasses) == 0 and len(cls.subclasses) == 0:
            virtual = ''
        destructor = '{virtual}~{name}();'.format(virtual=virtual, name=cls.name)

        superclass = '' if not cls.superclasses else ' : public %s' % cls.superclasses[0].name
        
        return HEADER.format(namespace=namespace,
                             class_name=class_name,
                             destructor=destructor,
                             includes=includes,
                             forward_declarations=forward_declarations,
                             forward_declarations_out=forward_declarations_out,
                             functions=functions,
                             members=members,
                             superclass=superclass,
                             )

    def write_cpp(self, cls):
        namespace = 'mg'
        class_name = cls.name
        includes = self.get_includes_for_source(cls)
        functions = ''
        for method in cls.functions:
            if not method.is_abstract:
                functions += self.write_function_cpp(cls, method)
        static_initializations = ''
        initializations = ''
        for member in cls.members:
            if cls.type == 'enum' and member.name != 'value':
                continue
            if member.is_static:
                static_initializations += self.write_member_static_initialization(cls, member)
            else:
                div = ': ' if not initializations else ', '
                initializations += div + self.write_member_initialization(member)
        
        destructor = '''{name}::~{name}()
        {{
        }}
        '''.format(name=cls.name)
        
        registration = 'REGISTRATION_OBJECT({0});\n'.format(cls.name)
        has_get_type = False
        if cls.is_abstract:
            registration = ''
        for method in cls.functions:
            if method.name == 'get_type':
                has_get_type = True
        if not has_get_type:
            registration = ''
        
        return SOURCE.format(namespace=namespace,
                             class_name=class_name,
                             destructor=destructor,
                             includes=includes,
                             functions=functions,
                             static_initializations=static_initializations,
                             initializations=initializations,
                             registration=registration,
                             )

    def write_function_hpp(self, method):
        string = '{virtual}{static}{type} {name}({args}){const}{override}{abstract};\n'

        args = list()
        for arg in method.args:
            assert(isinstance(arg[1], Object))
            args.append(self.write_named_object(arg[1], arg[0], True, False))
        args = ', '.join(args)

        assert (isinstance(method.return_type, Object))
        return_type = self.write_named_object(method.return_type, '', False, False)
        
        return string.format(virtual='virtual ' if method.is_virtual else '',
                             static='static ' if method.is_static else '',
                             const=' const' if method.is_const else '',
                             override='',
                             abstract=' = 0' if method.is_abstract else '',
                             type=return_type,
                             name=method.name,
                             args=args
                             )

    def write_function_cpp(self, cls, method):
        if method.specific_implementations:
            return method.specific_implementations
        
        text = '''{type} {class_name}::{name}({args}){const}
        {{
        {body}
        }}
        
        '''
        return_type = self.write_named_object(method.return_type, '', False, False)

        args = list()
        for arg in method.args:
            assert(isinstance(arg[1], Object))
            args.append(self.write_named_object(arg[1], arg[0], True, False))
        args = ', '.join(args)

        body = method.body

        return text.format(const=' const' if method.is_const else '',
                           type=return_type,
                           name=method.name,
                           args=args,
                           class_name=cls.name,
                           body=body
                           )

    def write_member_declaration(self, obj):
        return self.write_named_object(obj, obj.name, False, True) + ';\n'
    
    def write_member_enum_declaration(self, obj):
        if obj.name == 'value':
            return self.write_member_declaration(obj)
        return 'static constexpr {type} {name} = {value};\n'.format(type=obj.type,
                                                                    name=obj.name,
                                                                    value=obj.initial_value)

    def write_member_static_initialization(self, cls, obj):
        string = '{const}{type}{pointer} {owner}::{name}({initial_value});\n'
        return string.format(const='const ' if obj.is_const else '',
                             type=self.convert_type(obj.type),
                             pointer='*' if obj.is_pointer else '',
                             owner=cls.name,
                             name=obj.name,
                             initial_value=obj.initial_value
                             )

    def write_member_initialization(self, obj):
        
        def convert_initial_value(object_):
            if object_.is_pointer and obj.initial_value == '0':
                return 'nullptr'
            type_class = self.parser.find_class(object_.type)
            if type_class and type_class.type == 'enum':
                assert (len(type_class.members) > 0)
                return '{}::{}'.format(type_class.name, type_class.members[0].name)
        
            if object_.initial_value is None:
                return ''
            return object_.initial_value
    
        string = '{name}({initial_value})\n'
        initial_value = convert_initial_value(obj)
        return string.format(name=obj.name,
                             initial_value=initial_value
                             )
    
    @staticmethod
    def write_named_object(obj, name, try_to_use_const_ref, use_intrusive):
    
        def can_use_const_ref(object_):
            assert (isinstance(object_, Object))
            return object_.type in ['string', 'list', 'map']
        
        string_non_pointer = '{static}{const}{type}{templates}{pointer}{ref}{name}'
        string_pointer = '{static}{const}intrusive_ptr<{type}{templates}>{ref}{name}'
        templates = []
        for arg in obj.template_args:
            assert(isinstance(arg, Object))
            templates.append(Writer.write_named_object(arg, '', False, use_intrusive))
        templates = ('<' + ', '.join(templates) + '>') if templates else ''
        is_ref = obj.is_ref
        is_const = obj.is_const
        if not is_ref and not is_const and try_to_use_const_ref and can_use_const_ref(obj):
            is_ref = True
            is_const = True
            
        if use_intrusive and obj.is_pointer and not obj.is_const and not obj.is_link:
            string = string_pointer
        else:
            string = string_non_pointer
        return string.format(static='static ' if obj.is_static else '',
                             const='const ' if is_const else '',
                             type=Writer.convert_type(obj.type),
                             name=(' ' + name) if name else '',
                             pointer='*' if obj.is_pointer else '',
                             ref='&' if is_ref else '',
                             templates=templates,
                             )

    @staticmethod
    def convert_type(type_of_object):
        types = {
            'list': 'std::vector',
            'map': 'std::map',
            'string': 'std::string',
            'Observer': 'Observer<std::function<void()>>',
        }
        if type_of_object in types:
            return types[type_of_object]
        if isinstance(type_of_object, Object):
            return Writer.convert_type(type_of_object.name)
        return type_of_object

    @staticmethod
    def prepare_file(body):
        tabs = 0

        lines = body.split('\n')
        body = list()

        def get_tabs(count):
            out = ''
            for i in range(count):
                out += '\t'
            return out

        for line in lines:
            line = line.strip()

            if line and line[0] == '}':
                tabs -= 1
            backward = False
            if 'public:' in line or 'protected:' in line or 'private:' in line:
                backward = True
                tabs -= 1
            line = get_tabs(tabs) + line
            if backward:
                tabs += 1
            if line.strip() and line.strip()[0] == '{':
                tabs += 1
            body.append(line)
        body = '\n'.join(body)
        return body
    
    @staticmethod
    def get_filename(cls, ext):
        filename = cls.name + '.' + ext
        if cls.group:
            filename = cls.group + '/' + filename
        return filename
    
    def get_includes_for_header(self, cls):
        includes = set()
        forward_declarations = set()
        forward_declarations_out = set()

        def add(set_, obj):
            set_.add(self.convert_type(obj.type))
            for arg in obj.template_args:
                add(forward_declarations, arg)
        
        # members
        for member in cls.members:
            def parse_object(obj):
                if obj.is_link:
                    add(forward_declarations, obj)
                else:
                    add(includes, obj)
                for arg in obj.template_args:
                    parse_object(arg)
                    
            parse_object(member)
            
        # functions
        for method in cls.functions:
            for name, argtype in method.args:
                if 'pugi::' in argtype.type or 'Json::' in argtype.type:
                    add(forward_declarations_out, argtype)
                else:
                    add(forward_declarations, argtype)
                
        # superclasses
        for superclass in cls.superclasses:
            includes.add(superclass.name)

        if cls.name in includes:
            includes.remove(cls.name)
        if cls.name in forward_declarations:
            forward_declarations.remove(cls.name)
        if cls.name in forward_declarations_out:
            forward_declarations_out.remove(cls.name)

        includes = self.build_includes_block(cls, includes)
        forward_declarations = self.build_forward_declarations_block(forward_declarations)
        forward_declarations_out = self.build_forward_declarations_block(forward_declarations_out)
        return includes, forward_declarations, forward_declarations_out
    
    def get_includes_for_source(self, cls):
        includes = set()
        includes.add(cls.name)

        def add(set_, obj):
            set_.add(self.convert_type(obj.type))
            for arg in obj.template_args:
                add(includes, arg)

        # members
        for member in cls.members:
            if member.is_link:
                add(includes, member)
    
        # functions
        for method in cls.functions:
            for name, argtype in method.args:
                add(includes, argtype)

        # method bodies
        for method in cls.functions:
            for operation in method.operations:
                if operation is None:
                    continue
                if 'DataStorage::shared()' in operation:
                    includes.add('DataStorage')
                for type_ in self.parser.classes:
                    if type_.name in operation:
                        includes.add(type_.name)
        return self.build_includes_block(cls, includes)
    
    def build_includes_block(self, cls, includes):
        types = {
            'std::list': '<vector>',
            'std::vector': '<vector>',
            'std::map': '<map>',
            'std::set': '<set>',
            'std::string': '<string>',
            'Json::Value': '"jsoncpp/json.h"',
            'pugi::xml_node': '"pugixml/pugixml.hpp"',
            'Observer': '"Observer.h"',
            'intrusive_ptr': '"intrusive_ptr.h"',
        }
        result = []
        for typename in includes:
            assert(isinstance(typename, str))
            if typename in types:
                result.append('#include %s' % types[typename])
                continue

            other_class = self.parser.find_class(typename)
            if other_class:
                include = '#include "'
                if cls.group and other_class.group != cls.group:
                    include += '../'
                if other_class.group:
                    include += other_class.group + '/'
                include += other_class.name + '.h"'
                result.append(include)
        
        result = sorted(result)
        return '\n'.join(result)
    
    @staticmethod
    def build_forward_declarations_block(declarations):
        ignore = [
            'std::list',
            'std::vector',
            'std::map',
            'std::set',
            'std::string',
            'int',
            'bool',
            'float',
        ]
        predefined = {
            'Json::Value': 'namespace Json\n{\nclass Value;\n}\n',
            'pugi::xml_node': 'namespace pugi\n{\nclass xml_node;\n}\n',
        }
        result = []
        for declaration in declarations:
            if declaration in ignore:
                continue
            if declaration in predefined:
                result.append(predefined[declaration])
            else:
                result.append('class %s;' % declaration)
        result = sorted(result)
        return '\n'.join(result)

        
HEADER = '''#ifndef __{namespace}_{class_name}_h__
#define __{namespace}_{class_name}_h__

#include "intrusive_ptr.h"
#include "pugixml/pugixml.hpp"
{includes}

{forward_declarations_out}
namespace {namespace}
{{
{forward_declarations}

    class {class_name}{superclass}
    {{
    public:
        {class_name}();
        {destructor}
{functions}
{members}
    }};
}} //namespace {namespace}

#endif //#ifndef __{namespace}_{class_name}_h__
'''

SOURCE = '''
#include "intrusive_ptr.h"
#include "{namespace}_Factory.h"
{includes}
#include "{namespace}_extensions.h"

namespace {namespace}
{{
    {static_initializations}
    {registration}
    {class_name}::{class_name}()
    {initializations}{{
    }}
    
    {destructor}
    
{functions}}} //namespace {namespace}

'''