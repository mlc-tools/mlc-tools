import re
from . import constants
from .Writer import Writer
from .Writer import add_dict
from .Class import Class
from .Object import Object
from .Function import Function
from .DataStorageCreators import DataStorageCppXml
from .DataStorageCreators import DataStorageCppJson
from .Error import Error
from .cpp_extension import cpp_files
from .Object import AccessSpecifier
from .regex import RegexPatternCpp

FLAG_HPP = 2
FLAG_CPP = 4
SERIALIZATION = 0
DESERIALIZATION = 1


def _convert_argument_type(type_):
    if isinstance(type_, str):
        if type_ == 'string' or type_ == 'std::string':
            return 'const std::string&'
        return type_
    else:
        return _convert_argument_type(type_.type)


def convert_return_type(parser, type_object):
    result = type_object
    if isinstance(type_object, str):
        if '*' in type_object and 'const ' not in type_object:
            t = type_object.replace(r'\*', '')
            if parser.find_class(t):
                result = 'intrusive_ptr<{}>'.format(t)
    else:
        result = type_object.type
        if (type_object.is_link or type_object.is_const) and parser.find_class(type_object.type):
            result = '{}*'.format(type_object.type)
        elif type_object.is_pointer and parser.find_class(type_object.type):
            result = 'intrusive_ptr<{}>'.format(type_object.type)
        if type_object.is_const:
            result = 'const ' + result
    if result == 'string':
        result = 'std::string'
    return result


def convert_type(type_):
    if isinstance(type_, str):
        types = dict()
        types['list'] = 'std::vector'
        types['map'] = 'std::map'
        types['set'] = 'std::set'
        types['string'] = 'std::string'
        types['Observer'] = 'Observer<std::function<void()>>'
        if type_ in types:
            return types[type_]
        if '<' in type_ and '>' in type_ and not type_.startswith('template'):
            object = Object()
            object.parse(type_)
            args = []
            for arg in object.template_args:
                obj = Object()
                obj.parse(arg)
                args.append(convert_type(obj))
            result = '{}<{}>'.format(convert_type(object.type), ', '.join(args))
            if object.is_const:
                if object.is_pointer:
                    result = 'const %s' % result
                else:
                    result = 'const %s&' % result
            return result
    elif isinstance(type_, Object):
        s = convert_type(type_.type)
        if type_.template_args:
            s += '<'
            for i, arg in enumerate(type_.template_args):
                obj = Object()
                obj.parse(arg)
                s += convert_type(obj)
                if i < len(type_.template_args) - 1:
                    s += ', '
            s += '>'
        if type_.is_pointer:
            if type_.is_const:
                s = s + '*'
            else:
                s = 'intrusive_ptr<%s>' % s
        if type_.is_const:
            s = 'const ' + s
        return s
    else:
        # TODO: add error
        print('TODO: add error')
        print(type_)
        exit(-1)
    return type_


def get_include_file(parser, class_, filename, namespace):
    types = dict()
    types['list'] = '<vector>'
    types['vector'] = '<vector>'
    types['map'] = '<map>'
    types['set'] = '<set>'
    types['string'] = '<string>'
    types['pugi::xml_node'] = '"pugixml/pugixml.hpp"'
    types['Json::Value'] = '"jsoncpp/json.h"'
    types['pugi::xml_node'] = '"pugixml/pugixml.hpp"'
    types['Observer'] = '"Observer.h"'
    types['std::vector<int>'] = '<vector>'
    types['std::vector<intrusive_ptr<CommandBase>>'] = '<vector>'
    types['std::istream'] = '<istream>'
    types['intrusive_ptr'] = '"intrusive_ptr.h"'
    if filename in types:
        return types[filename]
    if 'map<' in filename:
        return '<map>'
    root_classes = ['DataStorage', 'Observable']
    for pair in cpp_files:
        file = pair[0].replace('@{namespace}', namespace)
        file = file.replace('.h', '')
        file = file.replace('.cpp', '')
        root_classes.append(file)
    if filename in root_classes:
        back = ''
        backs = len(class_.group.split('/')) if class_.group else 0
        for i in range(backs):
            back += '../'
        return '"' + back + filename + '.h"'

    included_class = parser.find_class(filename)
    if included_class and included_class.name == filename and class_.group != included_class.group:
        back = ''
        backs = len(class_.group.split('/')) if class_.group else 0
        for i in range(backs):
            back += '../'
        f = '"{2}{1}/{0}.h"' if included_class.group else '"{2}{0}.h"'
        return f.format(included_class.name, included_class.group, back)
    return '"{0}.h"'.format(filename)


def is_class_has_cpp_definitions(class_):
    if not class_.is_abstract:
        return True
    for function in class_.functions:
        if not function.is_abstract:
            return True
    for member in class_.members:
        if member.initial_value is not None:
            return True
    return False


def _create_constructor_function_hpp(class_):
    if class_.type == 'enum':
        return ''
    pattern = class_.name + '()'
    if not is_class_has_cpp_definitions(class_):
        pattern += '{}'
    pattern += ';\n'
    return pattern


def _create_destructor_function_hpp(class_):
    if class_.type == 'enum':
        return ''
    virtual = 'virtual '
    if not class_.is_virtual and len(class_.superclasses) == 0 and len(class_.subclasses) == 0:
        virtual = ''
    pattern = '{0}~{1}()'.format(virtual, class_.name)
    if not is_class_has_cpp_definitions(class_):
        pattern += '{}'
    pattern += ';\n'
    return pattern


def _create_constructor_function_cpp(parser, class_):
    if class_.type == 'enum':
        return ''
    if not is_class_has_cpp_definitions(class_):
        return ''
    initialize = ''
    initialize2 = ''

    accesses = [
        AccessSpecifier.public,
        AccessSpecifier.protected,
        AccessSpecifier.private,
    ]
    for access in accesses:
        for obj in class_.members:
            if obj.access != access:
                continue
            if obj.is_key:
                str1 = '\nstatic {0} {1}_key = 0;'.format(obj.type, obj.name)
                str2 = '\n{0} = ++{0}_key;'.format(obj.name)
                initialize2 += str1 + str2
            elif obj.initial_value and not obj.is_static:
                pattern = '\n{2} {0}({1})'
                s = ','
                if initialize == '':
                    s = ':'
                string = pattern.format(obj.name, obj.initial_value, s)
                initialize += string

    pattern = '{0}::{0}(){1}\n__begin__{2}\n\n__end__\n'
    string = pattern.format(class_.name, initialize, initialize2)
    return string


def _create_destructor_function_cpp(class_):
    if class_.type == 'enum':
        return ''
    if not is_class_has_cpp_definitions(class_):
        return ''
    pattern = '{0}::~{0}()\n__begin__\n__end__\n'
    string = pattern.format(class_.name)
    return string


class WriterCpp(Writer):

    def __init__(self, parser, serialize_format, namespace):
        Writer.__init__(self, parser, serialize_format)
        self.namespace = namespace
        self._current_class = None

    def get_namespace(self):
        return self.namespace

    def build_type_str(self, object_, with_name=True):
        args = list()
        for arg in object_.template_args:
            type_ = arg.name if isinstance(arg, Class) else arg.type
            type_ = convert_type(type_)
            if len(arg.template_args):
                type_ = self.build_type_str(arg)
            elif arg.is_pointer and arg.is_const:
                type_ = 'const {}* '.format(type_)
            else:
                if arg.is_pointer:
                    type_ = 'intrusive_ptr<{}>'.format(type_)
                if arg.is_const:
                    type_ = 'const ' + type_
            args.append(type_)
        args = ', '.join(args)
        type_ = object_.type
        if object_.is_pointer:
            if not (object_.is_pointer and object_.is_const):
                f = '{}*'
                class_ = self.parser.find_class(object_.type)
                if class_:
                    if class_.is_serialized:
                        f = 'intrusive_ptr<{}>'
            else:
                f = '{}*'

            type_ = f.format(convert_type(type_))
        modifiers = ''
        initial_value = ''
        if object_.is_static:
            modifiers += 'static '
        if object_.is_const:
            if object_.is_static and self._current_class.type == 'enum':
                modifiers += 'constexpr '
                initial_value = ' = {}'.format(object_.initial_value)
            else:
                modifiers += 'const '
        if len(object_.template_args) > 0:
            pattern = '{3}{0}<{2}>'
        else:
            pattern = '{3}{0}'
        if with_name:
            pattern += ' {1}'
            pattern += initial_value
        return pattern.format(convert_type(type_), object_.name, args, modifiers)

    def write_objects(self, objects, flags):

        accesses = [
            (AccessSpecifier.public, 'public: '),
            (AccessSpecifier.protected, 'protected: '),
            (AccessSpecifier.private, 'private: '),
        ]

        out = {flags: '\n'}
        for access in accesses:
            add = flags == FLAG_HPP
            for object_ in objects:
                if object_.access == access[0]:
                    if add:
                        out[flags] += access[1] + '\n'
                        add = False
                    out = add_dict(out, self.write_object(object_, flags))
        return out

    def write_object(self, object_, flags):

        out = Writer.write_object(self, object_, flags)

        if flags == FLAG_HPP:
            out[flags] += self.build_type_str(object_) + ';\n'

        if flags == FLAG_CPP:
            if object_.is_static:
                if object_.initial_value is None and self._current_class.type != 'enum':
                    Error.exit(Error.STATIS_MEMBER_SHOULD_HAVE_INITIALISATION, self._current_class.name, object_.name)
                if self._current_class.type == 'enum':
                    pattern = '{0} {2}::{1}'
                else:
                    pattern = '{0} {2}::{1} = {3}'
                pattern += ';\n'
                out[flags] += pattern.format(convert_type(object_), object_.name, self._current_class.name, object_.initial_value)
                pass
        return out

    def write_class(self, class_, flags):
        out = dict()
        class_ = self.add_methods(class_)

        if flags & FLAG_HPP:
            out = add_dict(out, self._write_class_hpp(class_))
        if flags & FLAG_CPP:
            out = add_dict(out, self._write_class_cpp(class_))
        return out

    def _write_class_hpp(self, class_):
        out = Writer.write_class(self, class_, FLAG_HPP)
        self._current_class = class_
        superclasses = list()
        for c in class_.superclasses:
            superclasses.append('public ' + c.name)
        superclasses = ', '.join(superclasses)
        objects = self.write_objects(class_.members, FLAG_HPP)
        functions = self.write_functions(class_.functions, FLAG_HPP)
        constructor = _create_constructor_function_hpp(class_)
        destructor = _create_destructor_function_hpp(class_)
        includes, forward_declarations, forward_declarations_out = self._find_includes(class_, FLAG_HPP)

        includes = list(set(includes.split('\n')))
        includes.sort()
        includes = '\n'.join(includes)
        forward_declarations = list(set(forward_declarations.split('\n')))
        forward_declarations.sort()
        forward_declarations = '\n'.join(forward_declarations)

        self._current_class = None

        pattern = ''
        if len(class_.superclasses) > 0:
            pattern += '{0} {1} : {2}'
        else:
            pattern += '{0} {1}'
        if functions[FLAG_HPP].strip() == '':
            f = ''
        else:
            f = '\n{4}'
        if objects[FLAG_HPP].strip() == '':
            o = ''
        else:
            o = '{3}'

        if class_.type != 'enum':
            pattern += '\n__begin__\npublic:\n{5}{6}' + f + o + '__end__;\n\n'
        else:
            pattern += '\n__begin__{5}' + o + 'public:' + f + '__end__;\n\n'

        pattern = '{3}\nnamespace {0}\n__begin__{2}\n\n{1}__end__//namespace {0}'.\
            format(self.get_namespace(), pattern, forward_declarations, forward_declarations_out)
        pattern = '#ifndef __{3}_{0}_h__\n#define __{3}_{0}_h__\n{2}\n{1}\n\n#endif //#ifndef __{3}_{0}_h__'.\
            format(class_.name, pattern, includes, self.get_namespace())

        out[FLAG_HPP] += pattern.format('class', class_.name, superclasses, objects[FLAG_HPP],
                                        functions[FLAG_HPP], constructor, destructor)
        return out

    def _write_class_cpp(self, class_):
        out = Writer.write_class(self, class_, FLAG_CPP)
        self._current_class = class_
        objects = self.write_objects(class_.members, FLAG_CPP)
        functions = self.write_functions(class_.functions, FLAG_CPP)
        constructor = _create_constructor_function_cpp(self.parser, class_)
        destructor = _create_destructor_function_cpp(class_)
        includes, f, f_out = self._find_includes(class_, FLAG_CPP)
        includes = self._find_includes_in_function_operation(class_, includes)

        includes = list(set(includes.split('\n')))
        includes.sort()
        includes = '\n'.join(includes)

        self._current_class = None
        if class_.type == 'class':
            pattern = '''#include "{0}.h"{4}

                         namespace {3}
                         __begin__{5}{6}
                         {2}
                         {7}
                         {1}__end__'''
        else:
            pattern = '''#include "{0}.h"{4}

                         namespace {3}
                         __begin__
                         {5}
                         {2}{7}
                         {1}__end__'''
        registration = 'REGISTRATION_OBJECT({0});\n'.format(class_.name)
        has_get_type = False
        if class_.is_abstract:
            registration = ''
        for func in class_.functions:
            if func.name == constants.CLASS_FUNCTION_GET_TYPE:
                has_get_type = True
        if not has_get_type:
            registration = ''

        if not class_.is_serialized:
            registration = ''
        if class_.is_abstract:
            registration = ''

        if not registration and \
                not constructor and \
                not destructor and \
                not objects[FLAG_CPP] and \
                not functions[FLAG_CPP]:
            return out

        out[FLAG_CPP] += pattern.format(class_.name, functions[FLAG_CPP], constructor, self.get_namespace(),
                                        includes, objects[FLAG_CPP], registration, destructor)
        return out

    def write_function(self, function, flags):
        out = dict()
        if flags & FLAG_HPP:
            if not function.is_abstract:
                fstr = '{5}{0} {1}({2}){3}{4};\n'
            else:
                fstr = '{5}{0} {1}({2}){3}{4} = 0;\n'
            args = list()
            for arg in function.args:
                args.append(_convert_argument_type(convert_type(arg[1])) + ' ' + arg[0])
            args = ', '.join(args)
            modifier = 'virtual ' if function.is_virtual else ''
            if function.is_static:
                modifier = 'static '
            if function.name == self._current_class.name or \
               function.name.find('operator ') == 0 or \
               function.is_template:
                modifier = ''
            is_override = ''
            if function.is_virtual and self.parser.is_function_override(self._current_class, function):
                is_override = ' override'
            is_const = ''
            if function.is_const:
                is_const = ' const'

            out[FLAG_HPP] = fstr.format(convert_return_type(self.parser, convert_type(function.get_return_type())),
                                        function.name, args, is_const, is_override, modifier)
        if flags & FLAG_CPP and not function.is_external and not function.is_abstract:
            is_const = ''
            if function.is_const:
                is_const = 'const'
            header = '{0} {4}::{1}({2}) {5}\n'
            body = '__begin__{3}\n__end__\n\n'
            fstr = header + body
            body = ''
            for operation in function.operations:
                convert_c17_toc14 = True
                if operation and convert_c17_toc14:
                    reg = RegexPatternCpp.convert_c17_to_c14
                    operation2 = reg[0].sub(reg[1], operation)
                    if operation2 != operation:
                        operation = operation2
                operation = operation.replace('std::round', 'round')
                fline = '{0}'
                line = '\n' + fline.format(operation)
                body += line

            body = convert_function_to_cpp(body, self.parser)

            args = list()
            for arg in function.args:
                args.append(_convert_argument_type(convert_type(arg[1])) + ' ' + RegexPatternCpp.FUNC_ARGS[0].sub(RegexPatternCpp.FUNC_ARGS[1], arg[0]))
            args = ', '.join(args)
            out[FLAG_CPP] = fstr.format(convert_return_type(self.parser, convert_type(function.get_return_type())),
                                        function.name, args, body, self._current_class.name, is_const)
        return out

    def write_classes(self, classes, flags):
        for class_ in classes:
            if class_.type == 'enum':
                self.convert_to_enum(class_)

        for class_ in classes:
            if not class_.auto_generated:
                continue
            dictionary = self.write_class(class_, FLAG_HPP)
            if len(dictionary) > 0:
                filename = class_.name + '.h'
                if class_.group:
                    filename = class_.group + '/' + filename
                self.files[filename] = dictionary[FLAG_HPP]
        for class_ in classes:
            if not class_.auto_generated:
                continue
            dictionary = self.write_class(class_, FLAG_CPP)
            if len(dictionary) > 0:
                filename = class_.name + '.cpp'
                if class_.group:
                    filename = class_.group + '/' + filename
                self.files[filename] = dictionary[FLAG_CPP]

    def write_functions(self, functions, flags):
        out = {FLAG_CPP: '', FLAG_HPP: ''}
        accesses = {
            AccessSpecifier.public: 'public: ',
            AccessSpecifier.protected: 'protected: ',
            AccessSpecifier.private: 'private: ',
        }
        for access in accesses:
            add = flags == FLAG_HPP
            for function in functions:
                if function.is_abstract and flags == FLAG_CPP:
                    continue
                if add:
                    out[flags] += accesses[access] + '\n'
                    add = False
                if function.access == access:
                    out = add_dict(out, self.write_function(function, flags))
        return out

    def add_methods(self, class_):
        if not class_.auto_generated:
            return class_
        if class_.is_serialized or class_.type == 'enum':
            have = False
            for function in class_.functions:
                if function.name == 'serialize':
                    have = True
                    break
            if not have:
                self.add_serialization(class_, SERIALIZATION)
                self.add_serialization(class_, DESERIALIZATION)
        if not class_.is_abstract:
            have = False
            for function in class_.functions:
                if function.name == 'operator ==':
                    have = True
                    break
            if not have:
                self.add_equal_methods(class_)
        return class_

    def get_serialization_object_arg(self, serialization_type):
        if self.serialize_format == 'json' and serialization_type == SERIALIZATION:
            return ['json', 'Json::Value&']
        if self.serialize_format == 'json' and serialization_type == DESERIALIZATION:
            return ['json', 'const Json::Value&']
        if self.serialize_format == 'xml' and serialization_type == SERIALIZATION:
            return ['xml', 'pugi::xml_node']
        if self.serialize_format == 'xml' and serialization_type == DESERIALIZATION:
            return ['xml', 'const pugi::xml_node&']

    def get_superclass_call_format(self):
        return '{0}::{1}(' + self.serialize_format + ');'

    def add_serialization(self, class_, serialization_type):
        function = Function()
        if serialization_type == SERIALIZATION:
            function.is_const = True
            function.name = 'serialize'
            function.args.append(self.get_serialization_object_arg(serialization_type))
        if serialization_type == DESERIALIZATION:
            function.name = 'deserialize'
            function.args.append(self.get_serialization_object_arg(serialization_type))
        function.is_virtual = len(class_.superclasses) > 0 or len(class_.subclasses) > 0
        function.return_type = Object.VOID
        function.link()

        for behabior in class_.superclasses:
            if not behabior.is_serialized:
                continue
            operation = self.get_superclass_call_format().format(behabior.name, function.name)
            function.operations.append(operation)

        for obj in class_.members:
            if obj.is_runtime or obj.is_static or (obj.is_const and not obj.is_link):
                continue
            operation = self._build_serialize_object_operation(obj, serialization_type)
            function.operations.append(operation)
        class_.functions.append(function)

    def _build_serialize_object_operation(self, obj, serialization_type):
        type_ = obj.name if isinstance(obj, Class) else obj.type
        return self._build_serialize_operation(obj.name, type_, obj.initial_value, obj.is_pointer, obj.template_args,
                                               serialization_type, is_link=obj.is_link)

    def _build_serialize_operation_enum(self, obj_name, obj_type, obj_value, obj_is_pointer, obj_template_args,
                                        serialization_type):
        pattern = self.serialize_protocol[serialization_type]['enum'][0].format(obj_name)
        pattern = pattern.replace('@__begin__namespace__end__', self.namespace)
        return pattern

    def _build_serialize_operation(self, obj_name, obj_type, obj_value, obj_is_pointer, obj_template_args,
                                   serialization_type, is_link=False):
        index = 0
        if obj_value is None:
            index = 1

        type_ = obj_type
        if self.parser.find_class(type_) and self.parser.find_class(type_).type == 'enum':
            string = self._build_serialize_operation_enum(obj_name, obj_type, obj_value,
                                                          obj_is_pointer, obj_template_args, serialization_type)
        else:
            if obj_type not in self.simple_types and type_ != 'list' and type_ != 'map':
                if is_link:
                    type_ = 'link'
                elif obj_is_pointer:
                    type_ = 'pointer'
                else:
                    type_ = 'serialized'
            template_args = list()
            if len(obj_template_args) > 0:
                if type_ == 'map':
                    if len(obj_template_args) != 2:
                        Error.exit(Error.MAP_TWO_ARGS, self._current_class.name, obj_name)
                    if serialization_type == SERIALIZATION:
                        return self.build_map_serialization(obj_name, obj_type, obj_value,
                                                            obj_is_pointer, obj_template_args)
                    if serialization_type == DESERIALIZATION:
                        return self.build_map_deserialization(obj_name, obj_type, obj_value,
                                                              obj_is_pointer, obj_template_args)
                else:
                    arg = obj_template_args[0]
                    arg_type = arg.name if isinstance(arg, Class) else arg.type
                    template_args.append(convert_type(arg_type))
                    if arg.is_link:
                        type_ = 'list<link>'
                    elif arg_type in self.simple_types:
                        type_ = '{0}<{1}>'.format(type_, arg_type)
                    elif arg.is_pointer:
                        type_ = 'list<pointer>'
                    elif arg.type == 'enum':
                        type_ = 'list<enum>'
                    else:
                        type_ = '{0}<serialized>'.format(type_)
            if type_ not in self.serialize_protocol[serialization_type]:
                Error.exit(Error.UNKNOWN_SERIALISED_TYPE, type_, obj_type)
            pattern = self.serialize_protocol[serialization_type][type_][index]
            pattern = pattern.replace('@__begin__namespace__end__', self.namespace)
            string = pattern.format(obj_name, convert_type(obj_type), obj_value, '{', '}', *template_args)
        return string

    def build_map_serialization(self, obj_name, obj_type, obj_value, obj_is_pointer, obj_template_args):
        key = obj_template_args[0]
        value = obj_template_args[1]
        key_type = key.name if isinstance(key, Class) else key.type
        value_type = value.name if isinstance(value, Class) else value.type
        pattern = self.serialize_protocol[SERIALIZATION]['map'][0]
        _value_is_pointer = value.is_pointer
        a0 = obj_name
        a1 = self._build_serialize_operation('key', key_type, None, key.is_pointer, [], SERIALIZATION, key.is_link)
        a2 = self._build_serialize_operation('value', value_type, None, _value_is_pointer, value.template_args,
                                             SERIALIZATION, value.is_link)
        return pattern.format(a0, a1, a2)

    def build_map_deserialization(self, obj_name, obj_type, obj_value, obj_is_pointer, obj_template_args):
        key = obj_template_args[0]
        value = obj_template_args[1]
        key_type = key.name if isinstance(key, Class) else key.type
        value_type = value.name if isinstance(value, Class) else value.type
        pattern = self.serialize_protocol[DESERIALIZATION]['map'][0]
        if key.is_link:
            key_str = 'const {}* key(nullptr);'.format(key_type)
        elif key.is_pointer:
            key_str = 'auto key = make_intrusive<{}>();'.format(key_type)
        else:
            key_str = '{} key;'.format(convert_type(key_type))

        _value_is_pointer = value.is_pointer if isinstance(value, Object) else False
        a0 = obj_name
        a1 = self._build_serialize_operation('key', key_type, None, key.is_pointer, [], DESERIALIZATION, key.is_link)
        a2 = self._build_serialize_operation('value', value_type, None, _value_is_pointer, value.template_args,
                                             DESERIALIZATION, value.is_link)
        a3 = key_str
        a4 = self.build_type_str(value)
        if value.is_pointer:
            a4 = 'intrusive_ptr<{}>'.format(value_type)
        return pattern.format(a0, a1, a2, a3, a4)

    def add_equal_methods(self, class_):
        function = Function()
        function.name = 'operator =='
        function.return_type = Object.BOOL
        function.args.append(['rhs', 'const ' + class_.name + '&'])
        function.is_const = True
        function.link()
        fbody_line = 'result = result && {0} == rhs.{0};'
        function.operations.append('bool result = true;')
        for m in class_.members:
            if m.is_static or m.is_const or m.type == 'Observable':
                continue
            function.operations.append(fbody_line.format(m.name))
        function.operations.append('return result;')
        class_.functions.append(function)

        function = Function()
        function.name = 'operator !='
        function.return_type = Object.BOOL
        function.args.append(['rhs', 'const ' + class_.name + '&'])
        function.is_const = True
        function.operations.append('return !(*this == rhs);')
        function.link()
        class_.functions.append(function)

    def _find_includes(self, class_, flags):
        out = ''
        forward_declarations = ''

        pattern = '\n#include {0}'

        def need_include(typename):
            if typename == '':
                return False
            types = list()
            types.append('int')
            types.append('float')
            types.append('bool')
            types.append('void')
            return typename not in types

        include_types = dict()
        forward_types = dict()

        for t in class_.superclasses:
            include_types[t.name] = 1
        for t in class_.members:
            type_ = t.type
            type_ = type_.replace('const', '').strip()
            type_ = type_.replace('*', '').strip()
            type_ = type_.replace('&', '').strip()
            include_types[type_] = 1
            if t.is_pointer:
                include_types['intrusive_ptr'] = 1
            for arg in t.template_args:
                type_ = arg.name if isinstance(arg, Class) else arg.type
                if arg.is_pointer:
                    if flags == FLAG_CPP:
                        include_types[type_] = 1
                    if flags == FLAG_HPP:
                        include_types[type_] = 1
                    type_ = 'intrusive_ptr'
                include_types[type_] = 1

        for f in class_.functions:
            for t in f.args:
                def checkType(type_string):
                    is_pointer_ = '*' in type_string
                    is_ref_ = '&' in type_string

                    typename = type_string.replace('const', '').strip()
                    typename = typename.replace('*', '').strip()
                    typename = typename.replace('&', '').strip()
                    if 'intrusive_ptr' in typename:
                        return
                    if 'CommandBase' in typename:
                        include_types['CommandBase'] = 1
                    else:
                        # if flags == FLAG_CPP or type_string != typename + '*':
                        #     include_types[typename] = 1
                        # if flags == FLAG_HPP and type_string == typename + '*':
                        #     forward_types[typename] = 1
                        if flags == FLAG_CPP:
                            include_types[typename] = 1
                        if flags == FLAG_HPP:
                            if is_pointer_ or is_ref_:
                                forward_types[typename] = 1
                            else:
                                include_types[typename] = 1

                checkType(t[1])
                if '<' in t[1] and '>' in t[1]:
                    type_ = t[1]
                    k = type_.find('<') + 1
                    l = type_.find('>')
                    args = type_[k:l].strip().split(',')
                    for arg in args:
                        checkType(arg)

                for cls in self.parser.classes:
                    if cls.name in t[1]:
                        if flags == FLAG_HPP:
                            forward_types[cls.name] = 1
                        else:
                            include_types[cls.name] = 1

            if not f.is_template:
                type_ = f.get_return_type().type
                type_ = type_.replace('const', '').strip()
                type_ = type_.replace('*', '').strip()
                type_ = type_.replace('&', '').strip()
                type_ = type_.replace('std::', '').strip()
                include_types[type_] = 1

        forward_declarations_out = ''
        for t in forward_types:
            if t == self._current_class.name:
                continue
            type_ = convert_type(t)
            if need_include(t):
                if type_.find('::') == -1:
                    forward_declarations += '\nclass {0};'.format(type_)
                else:
                    k = type_.index('::')
                    ns = type_[0:k]
                    type_ns = type_[k + 2:]
                    if ns == 'mg':
                        forward_declarations += '\nclass {0};'.format(type_ns)
                    elif not ns == 'std':
                        forward_declarations_out += '\nnamespace {}\n__begin__\nclass {};\n__end__'.format(ns, type_ns)
                    elif ns == 'std':
                        if '<' in type_ns:
                            type_ns = type_ns[0:type_ns.index('<')]
                        include_types[type_ns] = 1

        for t in include_types:
            if t == self._current_class.name:
                continue
            if need_include(t):
                out += pattern.format(get_include_file(self.parser, self._current_class, t, self.get_namespace()))

            # else:
            #     continue
            #     ns = type[0:type.find('::')]
            #     type = type[type.find('::') + 2:]
            #     str = '\nnamespace {1}\n__begin__\nclass {0};\n__end__'.format(type, ns)
            #     forward_declarations += str

        if flags == FLAG_HPP:
            out += pattern.format(get_include_file(self.parser, self._current_class, 'intrusive_ptr', self.get_namespace()))
        if flags == FLAG_CPP:
            out += pattern.format(get_include_file(self.parser, self._current_class, self.get_namespace() + '_Factory', self.get_namespace()))
            out += pattern.format(get_include_file(self.parser, self._current_class, self.get_namespace() + '_extensions', self.get_namespace()))
            out += '\n#include <algorithm>'

        out = out.split('\n')
        out.sort()
        out = '\n'.join(out)

        forward_declarations = forward_declarations.split('\n')
        forward_declarations.sort()
        forward_declarations = '\n'.join(forward_declarations)

        return out, forward_declarations, forward_declarations_out

    def _find_includes_in_function_operation(self, class_, current_includes):
        includes = current_includes
        for function in class_.functions:
            for operation in function.operations:
                if operation is None:
                    continue
                if 'throw Exception' in operation:
                    includes += '\n#include "Exception.h"'
                if 'DataStorage::shared()' in operation:
                    includes += '\n#include {}'.\
                        format(get_include_file(self.parser, self._current_class, 'DataStorage', self.get_namespace()))
                for type_ in self.parser.classes:
                    if type_.name in operation:
                        a = '"{}.h"'.format(type_.name)
                        b = '"{}.h"'.format(type_.name)
                        if a not in includes and b not in includes:
                            includes += '\n#include {0}'.\
                                format(get_include_file(self.parser, self._current_class, type_.name, self.get_namespace()))
        return includes

    def prepare_file(self, body):
        tabs = 0
        body = body.replace('__begin__', '{')
        body = body.replace('__end__', '}')

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

    def create_data_storage_class(self, name, classes):
        if self.serialize_format == 'xml':
            return DataStorageCppXml(name, classes, self.parser)
        else:
            return DataStorageCppJson(name, classes, self.parser)

    def create_data_storage(self):
        storage = self.create_data_storage_class('DataStorage', self.parser.classes)
        getter_h = storage.get_header_getter()
        getters_cpp = storage.get_source_getters(self.parser.classes)

        storage.functions.append(getter_h)
        header = self.write_class(storage, FLAG_HPP)[FLAG_HPP]
        del storage.functions[storage.functions.index(getter_h)]

        storage.functions.extend(getters_cpp)
        source = self.write_class(storage, FLAG_CPP)[FLAG_CPP]

        header = self.prepare_file(header)
        self.save_file(storage.name + '.h', header)

        source = self.prepare_file(source)
        self.save_file(storage.name + '.cpp', source)

    def save_config_file(self):
        pattern = '#ifndef __{0}_Config_h__\n#define __{0}_Config_h__\n\n{1}\n\n#endif //#ifndef __{0}_Config_h__'
        configs = list()
        configs.append('#define {}_JSON 1'.format(self.get_namespace().upper()))
        configs.append('#define {}_XML 2'.format(self.get_namespace().upper()))
        configs.append('\n#define {0}_SERIALIZE_FORMAT {0}_{1}'.format(self.get_namespace().upper(), self.serialize_format.upper()))
        filename_config = '{}_config.h'.format(self.get_namespace())
        self.save_file(filename_config, pattern.format(self.get_namespace(), '\n'.join(configs)))

        for pair in cpp_files:
            filename = pair[0]
            content = pair[1]
            content = content.replace('@{namespace}', self.get_namespace())
            content = content.replace('@{namespace_upper}', self.get_namespace().upper())
            filename = filename.replace('@{namespace}', self.get_namespace())
            if (not filename.startswith('intrusive_ptr.') or self.parser.generate_intrusive) and \
                    (not filename.startswith(self.get_namespace() + '_Factory.') or self.parser.generate_factory):
                self.save_file(filename, content)

    def convert_to_enum(self, cls):
        shift = 0
        cast = 'int'
        values = []

        def get_enum_value(cls, index):
            return '(1 << {})'.format(index) if not cls.is_numeric else str(index)
        for m in cls.members:
            if len(m.name):
                continue
            m.name = m.type
            m.type = cast
            m.is_static = True
            m.is_const = True
            if m.initial_value is None:
                if cast == 'int':
                    m.initial_value = get_enum_value(cls, shift)
            values.append(1 << shift)
            shift += 1

        def add_function(type_, name, args, const):
            function = Function()
            function.return_type = Object()
            function.return_type.parse(type_)
            function.name = name
            function.args = args
            function.is_const = const
            cls.functions.append(function)
            return function

        add_function(
            '',
            cls.name,
            [],
            False). \
            operations = ['value = {};'.format(cls.members[0].name)]
        add_function(
            '',
            cls.name,
            [['_value', cast]],
            False). \
            operations = ['value = _value;']
        add_function(
            '',
            cls.name,
            [['rhs', 'const {0}&'.format(cls.name)]],
            False). \
            operations = ['value = rhs.value;']
        add_function(
            '',
            'operator int',
            [],
            True). \
            operations = ['return value;']
        add_function(
            '{0}&:const'.format(cls.name),
            'operator =',
            [['rhs', 'const {0}&'.format(cls.name)]],
            False). \
            operations = ['value = rhs.value;', 'return *this;']
        add_function(
            'bool',
            'operator ==',
            [['rhs', 'const {0}&'.format(cls.name)]],
            True). \
            operations = ['return value == rhs.value;']
        add_function(
            'bool',
            'operator ==',
            [['rhs', 'int']],
            True). \
            operations = ['return value == rhs;']
        add_function('bool', 'operator <', [['rhs', 'const {0}&'.format(cls.name)]], True). \
            operations = ['return value < rhs.value;']

        function1 = add_function('', cls.name, [['_value', 'string']], False)
        function2 = add_function('{0}&:const'.format(cls.name), 'operator =', [['_value', 'string']], False)
        function3 = add_function('', 'operator std::string', [], True)
        function4 = add_function('string', 'str', [], True)
        index = 0
        for m in cls.members:
            if m.name == 'value':
                continue
            if index >= len(values):
                continue
            function1.operations.append('if(_value == "{0}") {1}value = {0}; return; {2};'.format(m.name, '{', '}'))
            function2.operations.append(
                'if(_value == "{0}") {1}value = {0}; return *this; {2};'.format(m.name, '{', '}'))
            # function1.operations.append(
            #     'if(value == "{0}") {1}value = {0}; return; {2};'.format(values[index], '{', '}'))
            # function2.operations.append(
            #     'if(value == "{0}") {1}value = {0}; return *this; {2};'.format(values[index], '{', '}'))
            function3.operations.append('if(value == {0}) return "{0}";'.format(m.name))
            function4.operations.append('if(value == {0}) return "{0}";'.format(m.name))
            index += 1
        function1.operations.append('value = 0;')
        function2.operations.append('return *this;')
        function3.operations.append('return "";')
        function4.operations.append('return "";')

        value = Object()
        value.initial_value = cls.members[0].name
        value.name = 'value'
        value.type = cast
        value.access = AccessSpecifier.private
        cls.members.append(value)
        return values


def convert_function_to_cpp(func, parser):
    for reg in RegexPatternCpp.FUNCTION:
        func = reg[0].sub(reg[1], func)
    return func
