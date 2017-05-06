import re
from Writer import Writer
from Writer import add_dict
from Class import Class
from Function import Function

FLAG_HPP = 2
FLAG_CPP = 4
SERIALIZATION = 0
DESERIALIZATION = 1


def _convert_argument_type(type_):
    if type_ == 'string' or type_ == 'std::string':
        return 'const std::string&'
    return type_


def convert_return_type(parser, type_):
    if '*' in type_:
        t = re.sub('\*', '', type_)
        if parser.find_class(t):
            return 'IntrusivePtr<{}>'.format(t)
    return type_


def convert_type(type_):
    types = dict()
    types['list'] = 'std::vector'
    types['map'] = 'std::map'
    types['set'] = 'std::set'
    types['string'] = 'std::string'
    types['Observer'] = 'Observer<std::function<void()>>'
    if type_ in types:
        return types[type_]
    return type_


def get_include_file(parser, class_, filename):
    types = dict()
    types['list'] = '<vector>'
    types['map'] = '<map>'
    types['set'] = '<set>'
    types['string'] = '<string>'
    types['pugi::xml_node'] = '"pugixml/pugixml.hpp"'
    types['Json::Value'] = '"jsoncpp/json.h"'
    types['pugi::xml_node'] = '"pugixml/pugixml.hpp"'
    types['Observer'] = '"Observer.h"'
    types['std::vector<int>'] = '<vector>'
    types['std::vector<intrusive_ptr<CommandBase>>'] = '<vector>'
    if filename in types:
        return types[filename]
    if 'std::map' in filename:
        return '<map>'

    included_class = parser.find_class(filename)
    if included_class and included_class.name == filename and class_.group != included_class.group:
        back = ''
        backs = len(class_.group.split('/')) if class_.group else 0
        for i in range(backs):
            back += '../'
        f = '"{2}{1}/{0}.h"' if included_class.group else '"{2}{0}.h"'
        return f.format(included_class.name, included_class.group, back)
    return '"{0}.h"'.format(filename)


def _create_constructor_function_hpp(class_):
    if class_.type == 'enum':
        return ''
    pattern = class_.name + '()'
    if class_.is_abstract:
        pattern += '{}'
    pattern += ';\n'
    return pattern


def _create_destructor_function_hpp(class_):
    if class_.type == 'enum':
        return ''
    pattern = 'virtual ~{0}()'.format(class_.name)
    if class_.is_abstract:
        pattern += '{}'
    pattern += ';\n'
    return pattern


def _create_constructor_function_cpp(parser, class_):
    if class_.type == 'enum':
        return ''
    initialize = ''
    initialize2 = ''
    for obj in class_.members:
        if obj.is_key:
            str1 = '\nstatic {0} {1}_key = 0;'.format(obj.type, obj.name)
            str2 = '\n{0} = ++{0}_key;'.format(obj.name)
            initialize2 += str1 + str2
        elif obj.initial_value and not obj.is_static and (obj.side == parser.side or obj.side == 'both'):
            pattern = '\n{2} {0}({1})'
            s = ','
            if initialize == '':
                s = ':'
            string = pattern.format(obj.name, obj.initial_value, s)
            initialize += string
    
    pattern = '{0}::{0}(){1}\n__begin__{2}\n\n__end__\n'
    string = pattern.format(class_.name, initialize, initialize2)
    string = re.sub('__begin__', '{', string)
    string = re.sub('__end__', '}', string)
    return string


def _create_destructor_function_cpp(class_):
    if class_.type == 'enum':
        return ''
    pattern = '{0}::~{0}()\n__begin__\n__end__\n'
    string = pattern.format(class_.name)
    string = re.sub('__begin__', '{', string)
    string = re.sub('__end__', '}', string)
    return string


def _get_namespace():
    return 'mg'


class WriterCpp(Writer):
    def __init__(self, out_directory, parser):
        self.simple_types = list()
        self.serialize_formats = list()
        self.serialize_formats.append({})
        self.serialize_formats.append({})
        self.create_serialization_patterns()

        self._currentClass = None
        Writer.__init__(self, out_directory, parser)
        return
    
    def create_serialization_patterns(self):
        pass

    def write_object(self, object_, flags):
        out = Writer.write_object(self, object_, flags)
        if object_.side != 'both' and object_.side != self.parser.side:
            return out
        
        if flags == FLAG_HPP:
            args = list()
            for arg in object_.template_args:
                type_ = arg.name if isinstance(arg, Class) else arg.type
                type_ = convert_type(type_)
                if arg.is_link:
                    type_ = 'const {}* '.format(type_)
                else:
                    if arg.is_pointer:
                        type_ = 'IntrusivePtr<{}>'.format(type_)
                    if arg.is_const:
                        type_ = 'const ' + type_
                args.append(type_)
            args = ', '.join(args)
            type_ = object_.type
            if object_.is_pointer:
                if not object_.is_link:
                    f = '{}*'
                    class_ = self.parser.find_class(object_.type)
                    if class_:
                        for b in class_.behaviors:
                            if b.name == 'SerializedObject':
                                f = 'IntrusivePtr<{}>'
                else:
                    f = '{}*'
                
                type_ = f.format(convert_type(type_))
            modifiers = ''
            if object_.is_static:
                modifiers += 'static '
            if object_.is_const:
                modifiers += 'const '
            if len(object_.template_args) > 0:
                pattern = '{3}{0}<{2}> {1};\n'
            else:
                pattern = '{3}{0} {1};\n'
            out[flags] += pattern.format(convert_type(type_), object_.name, args, modifiers)
        if flags == FLAG_CPP:
            if object_.is_static:
                if object_.initial_value is None:
                    print 'static object_ {} of class {} have not initial_value'.\
                        format(object_.name, self._currentClass.name)
                    exit(-1)
                if len(object_.template_args) > 0:
                    print '#TODO: static object_ {} of class {} have template arguments'.\
                        format(object_.name, self._currentClass.name)
                    exit(-1)
                pattern = '{4}{0} {2}::{1} = {3}'
                pattern += ';\n'
                modifier = ''
                if object_.is_const:
                    modifier = 'const '
                out[flags] += pattern.format(
                    convert_type(object_.type), object_.name,
                    self._currentClass.name, object_.initial_value, modifier)
        return out
    
    def write_class(self, class_, flags):
        out = dict()
        if class_.side != 'both' and class_.side != self.parser.side:
            return out
        class_ = self.add_methods(class_)
        
        if flags & FLAG_HPP:
            out = add_dict(out, self._write_class_hpp(class_))
        if flags & FLAG_CPP:
            out = add_dict(out, self._write_class_cpp(class_))
        return out
    
    def _write_class_hpp(self, class_):
        out = Writer.write_class(self, class_, FLAG_HPP)
        self._currentClass = class_
        behaviors = list()
        for c in class_.behaviors:
            behaviors.append('public ' + c.name)
        behaviors = ', '.join(behaviors)
        objects = self.write_objects(class_.members, FLAG_HPP)
        functions = self.write_functions(class_.functions, FLAG_HPP)
        constructor = _create_constructor_function_hpp(class_)
        destructor = _create_destructor_function_hpp(class_)
        includes, forward_declarations = self._find_includes(class_, FLAG_HPP)
        
        includes = list(set(includes.split('\n')))
        includes.sort()
        includes = '\n'.join(includes)
        forward_declarations = list(set(forward_declarations.split('\n')))
        forward_declarations.sort()
        forward_declarations = '\n'.join(forward_declarations)
        
        self._currentClass = None
        
        pattern = ''
        if len(class_.behaviors) > 0:
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
            o = '\npublic:{3}'
        
        if class_.type != 'enum':
            pattern += '\n__begin__\npublic:\n{5}{6}' + f + o + '__end__;\n\n'
        else:
            pattern += '\n__begin__{5}' + o + f + '__end__;\n\n'
        
        pattern = 'namespace {0}\n__begin__{2}\n\n{1}__end__//namespace {0}'.\
            format(_get_namespace(), pattern, forward_declarations)
        pattern = '#ifndef __mg_{0}_h__\n#define __mg_{0}_h__\n{2}\n\n{1}\n\n#endif //#ifndef __{0}_h__'.\
            format(class_.name, pattern, includes)
        
        out[FLAG_HPP] += pattern.format('class', class_.name, behaviors, objects[FLAG_HPP],
                                        functions[FLAG_HPP], constructor, destructor)
        out[FLAG_HPP] = re.sub('__begin__', '{', out[FLAG_HPP])
        out[FLAG_HPP] = re.sub('__end__', '}', out[FLAG_HPP])
        return out
    
    def _write_class_cpp(self, class_):
        out = Writer.write_class(self, class_, FLAG_CPP)
        self._currentClass = class_
        objects = self.write_objects(class_.members, FLAG_CPP)
        functions = self.write_functions(class_.functions, FLAG_CPP)
        constructor = _create_constructor_function_cpp(self.parser, class_)
        destructor = _create_destructor_function_cpp(class_)
        includes, f = self._find_includes(class_, FLAG_CPP)
        includes = self._find_includes_in_function_operation(class_, includes)
        
        includes = list(set(includes.split('\n')))
        includes.sort()
        includes = '\n'.join(includes)
        
        self._currentClass = None
        if class_.type == 'class':
            pattern = '''#include "{0}.h"
                         #include "Generics.h"{4}
                         
                         namespace {3}
                         __begin__{5}{6}
                         {2}
                         {7}
                         {1}__end__'''
        else:
            pattern = '''#include "{0}.h"
                         #include "Generics.h"{4}
                         
                         namespace {3}
                         __begin__
                         {5}
                         {2}{7}
                         {1}__end__'''
        registration = 'REGISTRATION_OBJECT({0});\n'.format(class_.name)
        for func in class_.functions:
            if func.is_abstract:
                registration = ''
                break
        if not class_.is_serialized:
            registration = ''
        if class_.is_abstract:
            registration = ''
        out[FLAG_CPP] += pattern.format(class_.name, functions[FLAG_CPP], constructor, _get_namespace(),
                                        includes, objects[FLAG_CPP], registration, destructor)
        out[FLAG_CPP] = re.sub('__begin__', '{', out[FLAG_CPP])
        out[FLAG_CPP] = re.sub('__end__', '}', out[FLAG_CPP])
        return out

    def write_function(self, function, flags):
        out = dict()
        if function.side != 'both' and function.side != self.parser.side:
            return out
        if flags & FLAG_HPP:
            if not self._currentClass.is_abstract and not function.is_abstract:
                fstr = '{5}{0} {1}({2}){3}{4};\n'
            else:
                fstr = '{5}{0} {1}({2}){3}{4} = 0;\n'
            args = list()
            for arg in function.args:
                args.append(_convert_argument_type(convert_type(arg[1])) + ' ' + arg[0])
            args = ', '.join(args)
            modifier = 'virtual '
            if function.is_static:
                modifier = 'static '
            if function.name == self._currentClass.name or function.name.find('operator ') == 0:
                modifier = ''
            is_override = ''
            if self.parser.is_function_override(self._currentClass, function):
                is_override = ' override'
            is_const = ''
            if function.is_const:
                is_const = ' const'
            
            out[FLAG_HPP] = fstr.format(convert_return_type(self.parser, convert_type(function.return_type)),
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
                fline = '{0}'
                line = '\n' + fline.format(operation)
                body += line
            args = list()
            for arg in function.args:
                args.append(_convert_argument_type(convert_type(arg[1])) + ' ' + arg[0])
            args = ', '.join(args)
            out[FLAG_CPP] = fstr.format(convert_return_type(self.parser, convert_type(function.return_type)),
                                        function.name, args, body, self._currentClass.name, is_const)
        return out
    
    def write_classes(self, classes, flags):
        out = {FLAG_CPP: '', FLAG_HPP: ''}
        
        for class_ in classes:
            dictionary = self.write_class(class_, FLAG_HPP)
            if len(dictionary) > 0:
                filename = class_.name + '.h'
                if class_.group:
                    filename = class_.group + '/' + filename
                self.save_file(filename, dictionary[FLAG_HPP])
                out = add_dict(out, dictionary)
        for class_ in classes:
            if not class_.is_abstract:
                dictionary = self.write_class(class_, FLAG_CPP)
                if len(dictionary) > 0:
                    filename = class_.name + '.cpp'
                    if class_.group:
                        filename = class_.group + '/' + filename
                    self.save_file(filename, dictionary[FLAG_CPP])
                    out = add_dict(out, dictionary)
        return out
    
    def write_functions(self, functions, flags):
        out = {FLAG_CPP: '', FLAG_HPP: ''}
        for function in functions:
            out = add_dict(out, self.write_function(function, flags))
        return out

    def add_methods(self, class_):
        if class_.is_serialized or class_.type == 'enum':
            have = False
            for function in class_.functions:
                if function.name == 'serialize':
                    have = True
                    break
            if not have:
                self.add_serialization(class_, SERIALIZATION)
                self.add_serialization(class_, DESERIALIZATION)
        if class_.is_visitor:
            have = False
            for function in class_.functions:
                if function.name == 'accept':
                    have = True
                    break
            if not have:
                self.add_accept_method(class_)
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
        pass
    
    def get_behavior_call_format(self):
        pass
    
    def add_serialization(self, class_, serialization_type):
        function = Function()
        if serialization_type == SERIALIZATION:
            function.is_const = True
            function.name = 'serialize'
            function.args.append(self.get_serialization_object_arg(serialization_type))
        if serialization_type == DESERIALIZATION:
            function.name = 'deserialize'
            function.args.append(self.get_serialization_object_arg(serialization_type))
        function.return_type = 'void'
        
        for behabior in class_.behaviors:
            if not behabior.is_serialized or behabior.is_abstract:
                continue
            operation = self.get_behavior_call_format().format(behabior.name, function.name)
            function.operations.append(operation)
        
        for obj in class_.members:
            if obj.is_runtime or obj.is_static or (obj.is_const and not obj.is_link):
                continue
            if obj.side != 'both' and obj.side != self.parser.side:
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
        pass
    
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
                        print 'map should have 2 arguments'
                        exit(-1)
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
                        type_ = '{0}<simple>'.format(type_)
                    elif arg.is_pointer:
                        type_ = 'pointer_list'
                    else:
                        type_ = '{0}<serialized>'.format(type_)
            pattern = self.serialize_formats[serialization_type][type_][index]
            string = pattern.format(obj_name, convert_type(obj_type), obj_value, '{', '}', *template_args)
        return string
    
    def build_map_serialization(self, obj_name, obj_type, obj_value, obj_is_pointer, obj_template_args):
        pass
    
    def build_map_deserialization(self, obj_name, obj_type, obj_value, obj_is_pointer, obj_template_args):
        pass
    
    def add_accept_method(self, class_):
        visitor = self.parser.get_type_of_visitor(class_)
        if visitor == class_.name:
            return
        function = Function()
        function.name = 'accept'
        function.return_type = 'void'
        function.args.append(['visitor', visitor + '*'])
        function.operations.append('visitor->visit( this );')
        class_.functions.append(function)
    
    def add_equal_methods(self, class_):
        function = Function()
        function.name = 'operator =='
        function.return_type = 'bool'
        function.args.append(['rhs', 'const ' + class_.name + '&'])
        function.is_const = True
        fbody_line = 'result = result && {0} == rhs.{0};'
        function.operations.append('bool result = true;')
        for m in class_.members:
            if m.side != 'both' and m.side != self.parser.side:
                continue
            if m.is_static or m.is_const:
                continue
            function.operations.append(fbody_line.format(m.name))
        function.operations.append('return result;')
        class_.functions.append(function)
        
        function = Function()
        function.name = 'operator !='
        function.return_type = 'bool'
        function.args.append(['rhs', 'const ' + class_.name + '&'])
        function.is_const = True
        function.operations.append('return !(*this == rhs);')
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
        
        for t in class_.behaviors:
            include_types[t.name] = 1
        for t in class_.members:
            if t.side != 'both' and t.side != self.parser.side:
                continue
            type_ = t.type
            type_ = re.sub('const', '', type_).strip()
            type_ = re.sub('\*', '', type_).strip()
            type_ = re.sub('&', '', type_).strip()
            include_types[type_] = 1
            if t.is_pointer:
                include_types['IntrusivePtr'] = 1
            for arg in t.template_args:
                type_ = arg.name if isinstance(arg, Class) else arg.type
                if arg.is_pointer:
                    if flags == FLAG_CPP:
                        include_types[type_] = 1
                    if flags == FLAG_HPP:
                        include_types[type_] = 1
                    type_ = 'IntrusivePtr'
                include_types[type_] = 1
        
        for f in class_.functions:
            for t in f.args:
                def checkType(type_string):
                    typename = re.sub('const', '', type_string).strip()
                    typename = re.sub('\*', '', typename).strip()
                    typename = re.sub('&', '', typename).strip()
                    if 'IntrusivePtr' in typename:
                        return
                    if 'CommandBase' in typename:
                        include_types['CommandBase'] = 1
                    else:
                        if flags == FLAG_CPP or type_string != typename + '*':
                            include_types[typename] = 1
                        if flags == FLAG_HPP and type_string == typename + '*':
                            forward_types[typename] = 1
                
                checkType(t[1])
                if '<' in t[1] and '>' in t[1]:
                    type_ = t[1]
                    k = type_.find('<') + 1
                    l = type_.find('>')
                    args = type_[k:l].strip().split(',')
                    for arg in args:
                        checkType(arg)
            
            type_ = f.return_type
            type_ = re.sub('const', '', type_).strip()
            type_ = re.sub('\*', '', type_).strip()
            type_ = re.sub('&', '', type_).strip()
            include_types[type_] = 1
        
        for t in include_types:
            if t == self._currentClass.name:
                continue
            if need_include(t):
                out += pattern.format(get_include_file(self.parser, self._currentClass, t))
        
        for t in forward_types:
            if t == self._currentClass.name:
                continue
            type_ = convert_type(t)
            if type_.find('::') == -1:
                forward_declarations += '\nclass {0};'.format(type_)
            # else:
            #     continue
            #     ns = type[0:type.find('::')]
            #     type = type[type.find('::') + 2:]
            #     str = '\nnamespace {1}\n__begin__\nclass {0};\n__end__'.format(type, ns)
            #     forward_declarations += str
        
        if flags == FLAG_HPP:
            out += '\n#include "IntrusivePtr.h"'
        if flags == FLAG_CPP:
            out += '\n#include "Factory.h"'
            out += '\n#include <algorithm>'
        
        out = out.split('\n')
        out.sort()
        out = '\n'.join(out)
        
        forward_declarations = forward_declarations.split('\n')
        forward_declarations.sort()
        forward_declarations = '\n'.join(forward_declarations)
        
        return out, forward_declarations
    
    def _find_includes_in_function_operation(self, class_, current_includes):
        includes = current_includes
        for function in class_.functions:
            for operation in function.operations:
                if operation is None:
                    continue
                if 'throw Exception' in operation:
                    includes += '\n#include "Exception.h"'
                if 'std::sqrt' in operation:
                    includes += '\n#include <cmath>'
                if 'get_data_storage()' in operation:
                    includes += '\n#include "DataStorage.h"'
                    
                for type_ in self.parser.classes:
                    if type_.name in operation:
                        a = '"{}.h"'.format(type_.name)
                        b = '"{}.h"'.format(type_.name)
                        if a not in includes and b not in includes:
                            includes += '\n#include {0}'.\
                                format(get_include_file(self.parser, self._currentClass, type_.name))
        return includes
    
    def prepare_file(self, body):
        tabs = 0
        lines = body.split('\n')
        body = list()
        
        def get_tabs(count):
            out = ''
            for i in xrange(count):
                out += '\t'
            return out
        
        for line in lines:
            line = line.strip()
            
            if line and line[0] == '}':
                tabs -= 1
            if 'public:' in line:
                tabs -= 1
            line = get_tabs(tabs) + line
            if 'public:' in line:
                tabs += 1
            if line.strip() and line.strip()[0] == '{':
                tabs += 1
            body.append(line)
        body = '\n'.join(body)
        return body
