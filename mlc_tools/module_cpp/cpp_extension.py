from mlc_tools.module_cpp.cpp.cpp_serializer_json import SERIALIZER_JSON_HPP, SERIALIZER_JSON_CPP
from mlc_tools.module_cpp.cpp.factory import FACTORY_HPP
from mlc_tools.module_cpp.cpp.functions import FUNCTIONS_HPP, FUNCTIONS_CPP
from mlc_tools.module_cpp.cpp.intrusive import INTRUSIVE_HPP
from mlc_tools.module_cpp.cpp.serializer_binary import SERIALIZER_BINARY_HPP, SERIALIZER_BINARY_CPP
from mlc_tools.module_cpp.cpp.serializer_common import SERIALIZER_COMMON
from mlc_tools.module_cpp.cpp.serializer_pimpl import SERIALIZER_PIMPL
from mlc_tools.module_cpp.cpp.serializer_xml import SERIALIZER_XML_HPP, SERIALIZER_XML_CPP

BASE_ENUM_HPP='''#ifndef __mg_BaseEnum_h__
#define __mg_BaseEnum_h__

#include <string>

namespace mg
{
    class BaseEnum
    {
    public:
        constexpr BaseEnum(int value_ = 0): value(value_) {}
        constexpr BaseEnum(const BaseEnum& rhs): value(rhs.value) {}
        constexpr operator int() const { return value; }
    protected:
        int value;
    };
}

#endif
'''


FILES_DICT = [
    ['@{namespace}_extensions.h', FUNCTIONS_HPP],
    ['@{namespace}_extensions.cpp', FUNCTIONS_CPP],
    ['intrusive_ptr.h', INTRUSIVE_HPP],
    ['@{namespace}_Factory.h', FACTORY_HPP],
    ['SerializerXml.h', SERIALIZER_XML_HPP],
    ['SerializerXml.cpp', SERIALIZER_XML_CPP],
    ['SerializerJson.h', SERIALIZER_JSON_HPP],
    ['SerializerJson.cpp', SERIALIZER_JSON_CPP],
    ['SerializerBinary.h', SERIALIZER_BINARY_HPP],
    ['SerializerBinary.cpp', SERIALIZER_BINARY_CPP],
    ['Pimpl.h', SERIALIZER_PIMPL],
    ['SerializerCommon.h', SERIALIZER_COMMON],
    ['BaseEnum.h', BASE_ENUM_HPP],
]
