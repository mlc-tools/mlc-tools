#ifndef __mg_AllTypes_h__
#define __mg_AllTypes_h__

#include "intrusive_ptr.h"
#include "../third/pugixml/pugixml.hpp"
#include "AllTypesChildren.h"
#include "TestEnum.h"
#include <map>
#include <string>
#include <vector>

namespace pugi
{
    class xml_node;
}

class Serializer;
class Deserializer;
namespace mg
{
    class AllTypesChildren;
    class Logger;
    class TestEnum;

    class AllTypes
    {
    public:
        AllTypes();
        ~AllTypes();
        void initialize();
        static bool tests(Logger* logger);
        bool operator ==(const AllTypes& rhs) const;
        bool operator !=(const AllTypes& rhs) const;
        void retain();
        int release();
        std::string get_type() const;
        void serialize(Serializer& xml) const;
        void deserialize(Deserializer& xml);

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
        std::map<AllTypesChildren, intrusive_ptr<AllTypesChildren>> object_object_ptr_map;
        std::vector<TestEnum> enum_list;
        std::map<TestEnum, int> enum_map;
    private:
        int _reference_counter;
    public:
        static const std::string TYPE;

    };
} //namespace mg

#endif //#ifndef __mg_AllTypes_h__
