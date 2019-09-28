from ..core.class_ import Class
from .writer import Writer


class Registrar(object):

    def __init__(self):
        pass

    @staticmethod
    def get_mock():
        cls = Class()
        cls.name = 'Registrar'
        cls.type = 'class'
        cls.auto_generated = False
        return cls

    def generate(self, model):
        if model.auto_registration:
            return
        mock = Registrar.get_mock()
        model.add_class(mock)

        includes = ''
        registrations = ''

        for cls in model.classes:
            if cls.is_abstract or cls.has_abstract_method():
                continue
            if not cls.has_method_with_name('get_type'):
                continue
            includes += '#include {}\n'.format(Writer.get_include_path_to_class(mock, cls))
            registrations += '    Factory::shared().registrationCommand<{0}>({0}::TYPE);\n'.format(cls.name)

        model.add_file(None, 'Registrar.h', REGISTRAR_HPP)
        model.add_file(None, 'Registrar.cpp', REGISTRAR_CPP.format(includes=includes,
                                                                   registrations=registrations))


REGISTRAR_HPP = '''#ifndef __Registrar_h__
#define __Registrar_h__

namespace mg
{
    void register_classes();
}

#endif
'''

REGISTRAR_CPP = '''#include "Registrar.h"
#include "mg_Factory.h"
{includes}
void mg::register_classes()
{{
{registrations}}}
'''