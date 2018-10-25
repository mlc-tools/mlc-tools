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
            ('%s.h' % cls.name, header),
            ('%s.cpp' % cls.name, source),
            ]

    def write_hpp(self, cls):
        namespace = 'mg'
        class_name = cls.name
        includes = '' # TODO: find headers includes
        forward_declarations = '' # TODO: find forward declarations
        functions = ''
        for method in cls.functions:
            functions += self.write_function_hpp(cls, method)
        members = '' # self.write_members(cls);
        for member in cls.members:
            members += self.write_member_declaration(cls, member)
        return HEADER.format(namespace=namespace,
                             class_name=class_name,
                             includes=includes,
                             forward_declarations=forward_declarations,
                             functions=functions,
                             members=members,
                             )

    def write_cpp(self, cls):
        namespace = 'mg'
        class_name = cls.name
        includes = '' # TODO: find source includes
        functions = '' # self.write_functions(cls);
        static_initializations=''
        initializations=''
        return SOURCE.format(namespace=namespace,
                             class_name=class_name,
                             includes=includes,
                             functions=functions,
                             static_initializations=static_initializations,
                             initializations=initializations
                             )

    def write_function_hpp(self, cls, function):
        string = '{virtual}{static}{type}{name}({args}){const}{override}{abstract};\n'

        args = list()
        for arg in function.args:
            assert(isinstance(arg[1], Object))
            args.append(self.write_named_object(arg[1], arg[0]))
        args = ', '.join(args)

        assert (isinstance(function.return_type, Object))
        return_type = self.write_named_object(function.return_type, '')

        return string.format(virtual='virtual ' if function.is_virtual else '',
                             static='static ' if function.is_virtual else '',
                             const=' const' if function.is_const else '',
                             override='',
                             abstract=' = 0' if function.is_abstract else '',
                             type=return_type,
                             name=function.name,
                             args=args
                             )

    def write_member_declaration(self, cls, obj):
        return self.write_named_object(obj, obj.name) + ';\n'

    def write_named_object(self, obj, name):
        string = '{static}{const}{type}{templates}{pointer} {name}'
        templates = []
        for arg in obj.template_args:
            assert(isinstance(arg, Object))
            templates.append(self.write_named_object(arg, ''))
        if len(templates):
            templates = '<' + ', '.join(templates) + '>'
        return string.format(static='static ' if obj.is_static else '',
                             const='const ' if obj.is_const else '',
                             type=self.convert_type(obj.type),
                             name=name,
                             pointer='*' if obj.is_pointer else '',
                             templates=templates,
                             )

    def convert_type(self, type_of_object):
        types = {
            'list': 'std::vector',
            'map': 'std::map',
            'string': 'std::string',
            'Observer': 'Observer<std::function<void()>>',
        }
        if type_of_object in types:
            return types[type_of_object]
        return type_of_object


HEADER = '''#ifndef __{namespace}_{class_name}_h__
#define __{namespace}_{class_name}_h__

#include "intrusive_ptr.h"
{includes}

namespace {namespace}
{{
{forward_declarations}
    class {class_name}
    {{
    public:
        {class_name}();
        virtual ~{class_name}();
{functions}
{members}
    }};
}} //namespace {namespace}

#endif //#ifndef __{namespace}_{class_name}_h__
'''

SOURCE = '''
#include "intrusive_ptr.h"
{includes}

namespace {namespace}
{{
    {static_initializations}

    {class_name}::{class_name}()
    {initializations}
    {{
    }}
    
    {class_name}::~{class_name}()
    {{
    }}
    
{functions}

}} //namespace {namespace}

'''