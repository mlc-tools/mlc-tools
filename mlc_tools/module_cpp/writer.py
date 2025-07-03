import re
from ..base import WriterBase
from ..core.class_ import Class
from ..core.function import Function
from ..core.object import Object, AccessSpecifier
from .regex import RegexPatternCpp
from ..utils.error import Error


class Writer(WriterBase):

    def __init__(self, out_directory):
        WriterBase.__init__(self, out_directory)
        self.objects_cache = {}
        self.methods_cache = {}
        self.methods_cache_with_templates = []

    def write_class(self, cls):
        self.objects_cache = {}
        self.methods_cache = {}

        for member in cls.members:
            declaration, initialisation, static_initialization = self.write_object(member)
            self.objects_cache[member.name] = [declaration, initialisation, static_initialization]

        for method in cls.functions:
            hpp, cpp = self.write_function(method)
            self.methods_cache[method] = ([hpp, cpp])
            if method.template_types:
                self.methods_cache_with_templates.append(hpp)

        header, includes, forward_declarations, forward_declarations_out = self.write_hpp(cls)
        source = self.write_cpp(cls, includes, forward_declarations, forward_declarations_out)

        if self.model.custom_generator:
            header, source = self.model.custom_generator.modify_sources(self.model, cls, header, source)

        return [
            (self.get_filename(cls, 'h'), self.prepare_file(header)),
            (self.get_filename(cls, 'cpp'), self.prepare_file(source)),
        ]

    def write_object(self, obj):
        declaration = ''
        initialization = ''
        static_initialization = ''

        assert isinstance(obj.type, str)
        if self.current_class.type == 'class':
            declaration = self.write_member_declaration(obj)
        elif self.current_class.type == 'enum':
            declaration = self.write_member_enum_declaration(obj)

        if self.current_class.type == 'enum':
            pass
        elif obj.is_static:
            static_initialization = self.write_member_static_init(self.current_class, obj)
        else:
            initialization += self.write_member_initialization(obj)
        return declaration, initialization, static_initialization

    def write_function(self, method):
        return [self.write_function_hpp(method), self.write_function_cpp(method)]

    def write_hpp(self, cls):
        namespace = 'mg'
        class_name = cls.name
        includes, forward_declarations, forward_declarations_out = self.get_includes_for_header(cls)
        functions = ''
        if cls.type == 'enum':
            functions += '{name}(const BaseEnum& rhs):BaseEnum(rhs){{}}'.format(name=class_name)
            functions += '\nconst {name}& operator =(const BaseEnum& rhs) {{ this->value = rhs.operator int(); return *this; }}'.format(name=class_name)

        access = AccessSpecifier.public
        for method in cls.functions:
            if method.name == 'constructor':
                continue
            hpp = self.methods_cache[method][0]
            if access != method.access:
                functions += AccessSpecifier.to_string(method.access) + ':\n'
                access = method.access
            functions += hpp
        for method in self.methods_cache_with_templates:
            includes.update(self.get_includes_for_method(cls, method, includes))
        members = ''

        access = AccessSpecifier.public
        for member in cls.members:
            if access != member.access:
                members += AccessSpecifier.to_string(member.access) + ':\n'
                access = member.access
            declaration, _, _ = self.objects_cache[member.name]
            members += declaration + '\n'

        virtual = 'virtual ' if cls.has_virtual_table() else ''
        destructor = '{virtual}~{name}();'.format(virtual=virtual, name=cls.name) if cls.type != 'enum' else ''

        superclass = '' if not cls.superclasses else ' : public %s' % cls.superclasses[0].name

        includes_s = self.build_includes(cls, includes)
        forward_declarations_s = self.build_forward_declarations(forward_declarations)
        forward_declarations_out_s = self.build_forward_declarations(forward_declarations_out)

        constructor_args = ''
        if cls.constructor is not None:
            constructor_args = self.create_function_hpp_args_string(cls.constructor)

        header = HEADER.format(namespace=namespace,
                               class_name=class_name,
                               destructor=destructor,
                               includes=includes_s,
                               forward_declarations=forward_declarations_s,
                               forward_declarations_out=forward_declarations_out_s,
                               functions=functions,
                               members=members,
                               superclass=superclass,
                               constructor_args=constructor_args)
        return header, includes, forward_declarations, forward_declarations_out

    def write_cpp(self, cls, includes, forw_declarations, forw_declarations_out):
        namespace = 'mg'
        class_name = cls.name
        functions = ''
        for method in cls.functions:
            if method.name == 'constructor':
                continue
            cpp = self.methods_cache[method][1]
            functions += cpp
        static_initializations = ''
        initializations = ''
        for member in cls.members:
            _, initialisation, static_initialization = self.objects_cache[member.name]
            if initialisation:
                div = ': ' if not initializations else ', '
                initializations += div + initialisation + '\n'
            if static_initialization:
                static_initializations += static_initialization + '\n'

        destructor = '''{name}::~{name}()
        {{
        }}
        '''.format(name=cls.name) if cls.type != 'enum' else ''

        registration = 'REGISTRATION_OBJECT({});\n'.format(cls.name) if self.model.auto_registration else ''
        is_abstract = cls.is_abstract
        if not is_abstract:
            for method in cls.functions:
                if method.is_abstract:
                    is_abstract = True
                    break
        if is_abstract:
            registration = ''
        if registration and not cls.has_method_with_name('get_type'):
            registration = ''

        includes = self.get_includes_for_source(cls, functions, includes, forw_declarations, forw_declarations_out)

        constructor_args = ''
        constructor_body = ''
        if cls.constructor is not None:
            constructor_args = self.create_function_cpp_args_string(cls.constructor)
            constructor_body = cls.constructor.body

        return SOURCE.format(namespace=namespace,
                             path_to_root=Writer.get_path_to_root(cls),
                             class_name=class_name,
                             destructor=destructor,
                             includes=includes,
                             functions=functions,
                             static_initializations=static_initializations,
                             initializations=initializations,
                             registration=registration,
                             constructor_args=constructor_args,
                             constructor_body=constructor_body)

    def create_function_hpp_args_string(self, method):
        args = list()
        for arg in method.args:
            assert isinstance(arg[1], Object)
            args.append(self.write_named_object(arg[1], arg[0], True, False))
            if arg[1].initial_value is not None:
                args[-1] += '=' + self.convert_initial_value(arg[1])
        args = ', '.join(args)
        return args

    def is_overrides(self, method: Function):
        if not method.is_virtual:
            return False
        superclass: Class = self.current_class.superclasses[0] if self.current_class.superclasses else None
        allowed = ['visit']
        while superclass is not None:
            for function in superclass.functions:
                if function.name != method.name:
                    continue
                if function.return_type.type != method.return_type.type:
                    if not self.model.validate_allow_different_virtual_method:
                        Error.exit(Error.ERROR_VIRTUAL_METHOD_HAS_DIFFERENT_DECLARATION, self.current_class.name,
                                   method.name, superclass.name)
                    continue

                if len(function.args) != len(method.args):
                    if not self.model.validate_allow_different_virtual_method and method.name not in allowed:
                        Error.exit(Error.ERROR_VIRTUAL_METHOD_HAS_DIFFERENT_DECLARATION, self.current_class.name,
                                   method.name, superclass.name)
                    continue
                cont = False
                for i, args in enumerate(function.args):
                    if args[1].type != method.args[i][1].type:
                        if not self.model.validate_allow_different_virtual_method and method.name not in allowed:
                            Error.exit(Error.ERROR_VIRTUAL_METHOD_HAS_DIFFERENT_DECLARATION, self.current_class.name,
                                       method.name, superclass.name)
                        cont = True
                        break
                if cont:
                    continue
                return True

            superclass = superclass.superclasses[0] if superclass.superclasses else None
        return False

    def write_function_hpp(self, method):
        string = '{virtual}{static}{friend}{type} {name}({args}){const}{override}{abstract}'
        assert isinstance(method.return_type, Object)
        return_type = self.write_named_object(method.return_type, '', False, True) if method.name != self.current_class.name else ''
        args = self.create_function_hpp_args_string(method)
        virtual = 'virtual ' if method.is_virtual or method.is_abstract or self.current_class.is_virtual else ''
        if method.name == self.current_class.name:
            virtual = ''

        body = ''
        if method.template_types:
            body = method.body
            string += '''
            {{
            {body}
            }}
            '''
            templates = ['class %s' % x for x in method.template_types]
            templates = ', '.join(templates)
            templates = 'template<%s> ' % templates
            string = templates + string
        else:
            string += ';\n'

        is_overrides = self.is_overrides(method)

        return string.format(virtual=virtual,
                             static='static ' if method.is_static else '',
                             friend='friend ' if method.is_friend else '',
                             const=' const' if method.is_const else '',
                             abstract=' = 0' if method.is_abstract else '',
                             override=' override' if is_overrides else '',
                             type=return_type,
                             name=method.name,
                             args=args,
                             body=body)

    def create_function_cpp_args_string(self, method):
        args = list()
        for arg in method.args:
            assert isinstance(arg[1], Object)
            args.append(self.write_named_object(arg[1], arg[0], True, False))
        args = ', '.join(args)
        return args

    def write_function_cpp(self, method):
        if method.is_external or method.is_abstract:
            return ''
        if method.template_types:
            return ''
        if method.specific_implementations:
            return method.specific_implementations

        scope = (self.current_class.name + '::') if not method.is_friend else ''
        text = '''{type} {scope}{name}({args}){const}
        {{
        {body}
        }}
        
        '''
        return_type = self.write_named_object(method.return_type, '', False,
                                              True) if method.name != self.current_class.name else ''
        args = self.create_function_cpp_args_string(method)

        body = method.body

        return text.format(const=' const' if method.is_const else '',
                           type=return_type,
                           name=method.name,
                           args=args,
                           scope=scope,
                           body=body)

    def write_member_declaration(self, obj):
        return self.write_named_object(obj, obj.name, False, True) + ';'

    def write_member_enum_declaration(self, obj):
        if obj.name == 'value':
            return self.write_member_declaration(obj)
        return 'static constexpr BaseEnum {name} = {value};'.format(name=obj.name,
                                                                    value=obj.initial_value)

    def write_member_static_init(self, cls, obj, use_intrusive=True):
        string_pointer = '{const}intrusive_ptr<{type}{templates}> {owner}::{name}{initial_value};'
        string_non_pointer = '{const}{type}{templates}{pointer} {owner}::{name}{initial_value};'

        if use_intrusive and obj.is_pointer and not obj.is_const and not obj.is_link and not obj.denied_intrusive:
            string = string_pointer
        else:
            string = string_non_pointer

        templates = Writer.get_templates(obj)
        initial_value = self.convert_initial_value(obj)
        if initial_value:
            initial_value = f'({initial_value})'
        return string.format(const='const ' if obj.is_const else '',
                             type=self.convert_type(obj.type),
                             templates=templates,
                             pointer='*' if obj.is_pointer else '',
                             owner=cls.name,
                             name=obj.name,
                             initial_value=initial_value)

    def write_member_static_enum(self, cls, obj):
        assert self is not None
        return 'const int {}::{};'.format(cls.name, obj.name)

    def convert_initial_value(self, object_):
        if object_.is_pointer and (object_.initial_value == '0' or object_.initial_value is None):
            return 'nullptr'
        type_class = self.model.get_class(object_.type) if self.model.has_class(object_.type) else None
        if type_class is not None and type_class.type == 'enum' and object_.initial_value is None:
            assert type_class.members
            return '{}::{}'.format(type_class.name, type_class.members[0].name)

        if object_.initial_value is None:
            return ''
        return object_.initial_value

    def write_member_initialization(self, obj):
        initial_value = self.convert_initial_value(obj)
        return '{}({})'.format(obj.name, initial_value)

    @staticmethod
    def get_templates(obj):
        templates = []
        for arg in obj.template_args:
            assert isinstance(arg, Object)
            templates.append(Writer.write_named_object(arg, '', False, True))
            if arg.callable_args is not None:
                callable_args = []
                for callable_arg in arg.callable_args:
                    callable_args.append(Writer.write_named_object(callable_arg, '', True, False))
                callable_args = '({})'.format(', '.join(callable_args))
                templates[-1] += callable_args

        templates = ('<' + ', '.join(templates) + '>') if templates else ''
        return templates

    @staticmethod
    def write_named_object(obj, name, try_to_use_const_ref, use_intrusive):

        def can_use_const_ref(object_):
            assert isinstance(object_, Object)
            return object_.type in ['string', 'list', 'map']

        string_non_pointer = '{static}{const}{type}{templates}{pointer}{ref}{name}'
        string_pointer = '{static}{const}intrusive_ptr<{type}{templates}>{ref}{name}'
        templates = Writer.get_templates(obj)
        is_ref = obj.is_ref
        is_const = obj.is_const
        if not is_ref and not is_const and try_to_use_const_ref and can_use_const_ref(obj):
            is_ref = True
            is_const = True

        modified_type = obj.type
        if '(' in modified_type and ')' in modified_type:
            left = modified_type.index('(')
            right = modified_type.index(')')
            args = modified_type[left + 1:right]
            args = args.split(',')
            args = [Writer.convert_type(x.strip()) for x in args]
            args = ', '.join(args)
            modified_type = modified_type[0:left + 1] + args + modified_type[right:]

        if use_intrusive and obj.is_pointer and not obj.is_const and not obj.is_link and not obj.denied_intrusive:
            string = string_pointer
        else:
            string = string_non_pointer
        return string.format(static='static ' if obj.is_static else '',
                             const='const ' if is_const else '',
                             type=Writer.convert_type(modified_type),
                             name=(' ' + name) if name else '',
                             pointer='*' if obj.is_pointer else '',
                             ref='&' if is_ref else '',
                             templates=templates)

    @staticmethod
    def convert_type(type_of_object):
        assert isinstance(type_of_object, str)
        types = {
            'list': 'std::vector',
            'map': 'std::map',
            'string': 'std::string',
            'Observer': 'Observer<std::function<void()>>',
        }
        if type_of_object in types:
            return types[type_of_object]
        return type_of_object

    def prepare_file(self, text):
        tabs = 0

        lines = text.split('\n')
        text = list()

        def get_tabs(count):
            return '    ' * count

        for line in lines:
            line = line.strip()

            backward = False
            if line and line[0] == '}':
                tabs -= 1
            elif 'public:' in line or 'protected:' in line or 'private:' in line:
                backward = True
                tabs -= 1
            line_strip = line
            if line:
                line = get_tabs(tabs) + line
            if backward:
                tabs += 1
            if line_strip and line_strip[0] == '{':
                tabs += 1
            text.append(line)
        text = '\n'.join(text)
        text = text.strip().replace('\n\n\n', '\n\n') + '\n'
        return WriterBase.prepare_file(self, text)

    @staticmethod
    def get_filename(class_, ext):
        filename = class_.name + '.' + ext
        if class_.group:
            filename = class_.group + '/' + filename
        return filename

    def get_includes_for_header(self, cls):
        includes = set()
        forward_declarations = set()
        forward_declarations_out = set()

        def add(set_, obj):
            set_.add(self.convert_type(obj.type))
            for arg in obj.template_args:
                add(forward_declarations, arg)
            if obj.callable_args is not None:
                for arg in obj.callable_args:
                    add(forward_declarations, arg)

        # members
        for member in cls.members:
            def parse_object(container, obj):
                add(container, obj)
                for arg in obj.template_args:
                    if cls.name == 'DataStorage' or cls.prefer_use_forward_declarations:
                        parse_object(forward_declarations, arg)
                    else:
                        parse_object(container, arg)
            parse_object(includes, member)
            if 'std::atomic' in member.type:
                includes.add('std::atomic')



        # functions
        std_includes = ['map', 'list', 'string']
        for method in cls.functions:
            for _, argtype in method.args:
                if argtype.type in std_includes:
                    add(includes, argtype)
                elif 'pugi::' in argtype.type or 'Json::' in argtype.type:
                    add(forward_declarations_out, argtype)
                else:
                    add(forward_declarations, argtype)
            if not self.model.user_includes or method.return_type.type in std_includes:
                add(includes, method.return_type)
            else:
                add(forward_declarations, method.return_type)

        # superclasses
        for superclass in cls.superclasses:
            includes.add(superclass.name)

        if cls.name in includes:
            includes.remove(cls.name)
        if cls.name in forward_declarations:
            forward_declarations.remove(cls.name)
        if cls.name in forward_declarations_out:
            forward_declarations_out.remove(cls.name)

        return includes, forward_declarations, forward_declarations_out

    def get_includes_for_source(self, cls: Class, functions_text, hpp_includes, forw_declarations, forw_declarations_out):
        includes = set()
        includes.add(cls.name)
        includes.update(forw_declarations)
        includes.update(forw_declarations_out)

        includes.update(self.get_includes_for_method(cls, functions_text, hpp_includes))
        includes.update(cls.user_includes)

        return self.build_includes(cls, includes)

    def get_includes_for_method(self, cls, functions_text, hpp_includes):
        includes = list()

        for type_ in self.model.classes:
            name = type_.name
            if name not in hpp_includes and name in functions_text:
                pattern = None
                if name not in RegexPatternCpp.regs_class_names:
                    pattern = re.compile(r'\b{}\b'.format(name))
                    RegexPatternCpp.regs_class_names[name] = pattern
                pattern = pattern or RegexPatternCpp.regs_class_names[name]
                need = cls.name is name
                need = need or pattern.search(functions_text) is not None
                if need:
                    includes.append(name)
        return includes

    def build_includes(self, cls, includes):
        types = {
            'std::list': '<vector>',
            'std::atomic': '<atomic>',
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
            assert isinstance(typename, str)
            if typename in types:
                result.append('#include %s' % types[typename])
                continue

            if self.model.has_class(typename):
                other_class = self.model.get_class(typename)
                include = '#include '
                include += self.get_include_path_to_class(cls, other_class)
                result.append(include)

        result = sorted(result)
        return '\n'.join(result)

    @staticmethod
    def get_include_path_to_class(cls_, to_cls):
        include = '"'
        if cls_.group and to_cls.group != cls_.group:
            include += '../'
        if to_cls.group and to_cls.group != cls_.group:
            include += to_cls.group + '/'
        include += to_cls.name + '.h"'
        return include

    @staticmethod
    def get_path_to_root(cls_):
        if cls_.group:
            return '../'
        return ''

    def build_forward_declarations(self, declarations):
        ignore = [
            'std::list',
            'std::vector',
            'std::map',
            'std::set',
            'std::string',
            'int',
            'bool',
            'float',
            'void',
            'Observable',
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
            elif self.model.has_class(declaration):
                result.append('class %s;' % declaration)
        result = sorted(result)
        return '\n'.join(result)


HEADER = '''#ifndef __{namespace}_{class_name}_h__
#define __{namespace}_{class_name}_h__

#include <cstdint>
#include "intrusive_ptr.h"
#include "pugixml/pugixml.hpp"
{includes}

{forward_declarations_out}
namespace {namespace}
{{
    class SerializerXml;
    class DeserializerXml;
    class SerializerJson;
    class DeserializerJson;
{forward_declarations}

    class {class_name}{superclass}
    {{
    public:
        {class_name}({constructor_args});
        {destructor}
{functions}
{members}
    }};
}} //namespace {namespace}

#endif //#ifndef __{namespace}_{class_name}_h__
'''

SOURCE = '''
#include "intrusive_ptr.h"
#include "{path_to_root}{namespace}_Factory.h"
{includes}
#include "{path_to_root}{namespace}_extensions.h"
#include "{path_to_root}SerializerJson.h"
#include "{path_to_root}SerializerXml.h"

namespace {namespace}
{{
    {static_initializations}
    {registration}
    {class_name}::{class_name}({constructor_args})
    {initializations}{{
    {constructor_body}
    }}
    
    {destructor}
    
{functions}}} //namespace {namespace}

'''
