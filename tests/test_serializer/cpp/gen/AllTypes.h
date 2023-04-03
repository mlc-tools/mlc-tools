#ifndef __mg_AllTypes_h__
#define __mg_AllTypes_h__

#include "intrusive_ptr.h"
#include "pugixml/pugixml.hpp"
#include "AllTypesChildren.h"
#include "TestEnum.h"
#include <map>
#include <string>
#include <vector>

namespace mg
{
    class SerializerXml;
    class DeserializerXml;
    class SerializerJson;
    class DeserializerJson;
    class AllTypesChildren;
    class Logger;
    class TestEnum;

    class AllTypes
    {
    public:
        AllTypes();
        ~AllTypes();
        void initialize();
        bool operator ==(const AllTypes& rhs) const;
        bool operator !=(const AllTypes& rhs) const;
        int retain();
        int release();
        std::string get_type() const;
        void serialize_xml(SerializerXml& serializer) const;
        void deserialize_xml(DeserializerXml& deserializer);
        void serialize_json(SerializerJson& serializer) const;
        void deserialize_json(DeserializerJson& deserializer);

        int int_value0;
        int int_value1;
        float float_value0;
        float float_value1;
        bool bool_value0;
        bool bool_value1;
        std::string str_value0;
        std::string str_value1;
        std::vector<int> int_list;
        std::vector<float> float_list;
        std::vector<double> double_list;
        std::vector<bool> bool_list;
        std::vector<std::string> string_list;
        std::map<int, std::string> int_string_map;
        std::map<float, std::string> float_string_map;
        std::map<bool, std::string> bool_string_map;
        std::map<std::string, std::string> string_string_map;
        std::map<std::string, int> string_int_map;
        std::map<std::string, float> string_float_map;
        std::map<std::string, bool> string_bool_map;
        AllTypesChildren object;
        intrusive_ptr<AllTypesChildren> object_ptr;
        std::vector<AllTypesChildren> object_list;
        std::vector<intrusive_ptr<AllTypesChildren>> object_ptr_list;
        std::map<std::string, AllTypesChildren> object_map;
        std::map<std::string, intrusive_ptr<AllTypesChildren>> object_ptr_map;
        std::vector<TestEnum> enum_list;
        std::map<TestEnum, int> enum_map;
        int _reference_counter;
        static const std::string TYPE;

    };
} //namespace mg

#endif //#ifndef __mg_AllTypes_h__
