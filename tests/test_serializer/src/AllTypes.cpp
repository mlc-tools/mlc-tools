#include "intrusive_ptr.h"
#include "AllTypes.h"
#include "AllTypesChildren.h"
#include "TestEnum.h"
#include "../third/pugixml/pugixml.hpp"
#include <string>
#include "serialize/SerializerXml.h"
#include "serialize/SerializerJson.h"

namespace mg
{
    const std::string AllTypes::TYPE("AllTypes");

    AllTypes::AllTypes()
    : int_value0(0)
    , int_value1(0)
    , float_value0(0)
    , float_value1(0.0)
    , bool_value0(true)
    , bool_value1(false)
    , str_value0("")
    , str_value1("")
    , int_list()
    , float_list()
    , bool_list()
    , string_list()
    , int_string_map()
    , float_string_map()
    , bool_string_map()
    , string_string_map()
    , string_int_map()
    , string_float_map()
    , string_bool_map()
    , object()
    , object_ptr(nullptr)
    , object_list()
    , object_ptr_list()
    , object_map()
    , object_ptr_map()
    , enum_list()
    , enum_map()
    , _reference_counter(1)
    {

    }

    AllTypes::~AllTypes()
    {
    }

    void AllTypes::initialize()
    {
        this->int_value0 = 1;
        this->int_value1 = 1;
        this->float_value0 = 1.f;
        this->float_value1 = 1.0f;
        this->bool_value0 = false;
        this->bool_value1 = true;
        this->str_value0 = "test_string";
        this->str_value1 = "test_string";
        this->int_list.push_back(0);
        this->int_list.push_back(1);
        this->float_list.push_back(0.f);
        this->float_list.push_back(1.f);
        this->bool_list.push_back(true);
        this->bool_list.push_back(true);
        this->string_list.push_back("0");
        this->string_list.push_back("1");
        this->int_string_map[0] = "0";
        this->int_string_map[1] = "1";
        this->bool_string_map[true] = "0";
        this->bool_string_map[false] = "1";
        this->float_string_map[0.f] = "0";
        this->float_string_map[1.f] = "1";
        this->string_string_map["0"] = "0";
        this->string_string_map["1"] = "1";
        this->string_int_map["0"] = 0;
        this->string_int_map["1"] = 1;
        this->string_bool_map["0"] = true;
        this->string_bool_map["1"] = false;
        this->string_float_map["0"] = 0.f;
        this->string_float_map["1"] = 1.f;
        this->string_string_map["0"] = "0";
        this->string_string_map["1"] = "1";
        this->object.value = 0;
        this->object_ptr = make_intrusive<AllTypesChildren>();
        this->object_ptr->value = 0;
        this->enum_list.push_back(TestEnum::value1);
        this->enum_list.push_back(TestEnum::value2);
        this->enum_map[TestEnum::value1] = 1;
        this->enum_map[TestEnum::value2] = 2;
    }

    bool AllTypes::tests(Logger* logger)
    {
        bool result = true;
        auto inst = make_intrusive<AllTypes>();
        inst->initialize();
        return result;
    }

    bool AllTypes::operator ==(const AllTypes& rhs) const
    {
        bool result = true;
        result = result && this->int_value0 == rhs.int_value0;
        result = result && this->int_value1 == rhs.int_value1;
        result = result && this->float_value0 == rhs.float_value0;
        result = result && this->float_value1 == rhs.float_value1;
        result = result && this->bool_value0 == rhs.bool_value0;
        result = result && this->bool_value1 == rhs.bool_value1;
        result = result && this->str_value0 == rhs.str_value0;
        result = result && this->str_value1 == rhs.str_value1;
        result = result && this->int_list == rhs.int_list;
        result = result && this->float_list == rhs.float_list;
        result = result && this->bool_list == rhs.bool_list;
        result = result && this->string_list == rhs.string_list;
        result = result && this->int_string_map == rhs.int_string_map;
        result = result && this->float_string_map == rhs.float_string_map;
        result = result && this->bool_string_map == rhs.bool_string_map;
        result = result && this->string_string_map == rhs.string_string_map;
        result = result && this->string_int_map == rhs.string_int_map;
        result = result && this->string_float_map == rhs.string_float_map;
        result = result && this->string_bool_map == rhs.string_bool_map;
        result = result && this->object == rhs.object;
        result = result && ((this->object_ptr == rhs.object_ptr) || (this->object_ptr != nullptr && rhs.object_ptr != nullptr && *this->object_ptr == *rhs.object_ptr));
        result = result && this->object_list == rhs.object_list;
        result = result && this->object_ptr_list == rhs.object_ptr_list;
        result = result && this->object_map == rhs.object_map;
        result = result && this->object_ptr_map == rhs.object_ptr_map;
        result = result && this->enum_list == rhs.enum_list;
        result = result && this->enum_map == rhs.enum_map;
        return result;
    }

    bool AllTypes::operator !=(const AllTypes& rhs) const
    {
        return !(*this == rhs);
    }

    void AllTypes::retain()
    {
        this->_reference_counter += 1;
    }

    int AllTypes::release()
    {
        this->_reference_counter -= 1;
        auto counter = this->_reference_counter;
        if(counter == 0)
        delete this;
        return counter;
    }

    std::string AllTypes::get_type() const
    {
        return AllTypes::TYPE;
    }

    void AllTypes::serialize(SerializerXml& serializer) const
    {
        serializer.serialize(int_value0, "int_value0", 0);
        serializer.serialize(int_value1, "int_value1", 0);
        serializer.serialize(float_value0, "float_value0", 0.f);
        serializer.serialize(float_value1, "float_value1", 0.f);
        serializer.serialize(bool_value0, "bool_value0", true);
        serializer.serialize(bool_value1, "bool_value1", false);
        serializer.serialize(str_value0, "str_value0", std::string(""));
        serializer.serialize(str_value1, "str_value1", std::string(""));
        serializer.serialize(int_list, "int_list");
        serializer.serialize(float_list, "float_list");
        serializer.serialize(bool_list, "bool_list");
        serializer.serialize(string_list, "string_list");
        serializer.serialize(int_string_map, "int_string_map");
        serializer.serialize(float_string_map, "float_string_map");
        serializer.serialize(bool_string_map, "bool_string_map");
        serializer.serialize(string_string_map, "string_string_map");
        serializer.serialize(string_int_map, "string_int_map");
        serializer.serialize(string_float_map, "string_float_map");
        serializer.serialize(string_bool_map, "string_bool_map");
        serializer.serialize(object, "object");
        serializer.serialize(object_ptr, "object_ptr");
        serializer.serialize(object_list, "object_list");
        serializer.serialize(object_ptr_list, "object_ptr_list");
        serializer.serialize(object_map, "object_map");
        serializer.serialize(object_ptr_map, "object_ptr_map");
        serializer.serialize(enum_list, "enum_list");
        serializer.serialize(enum_map, "enum_map");
        serializer.serialize(object_object_ptr_map, "object_object_ptr_map");
    }
    void AllTypes::deserialize(DeserializerXml& serializer){
        serializer.deserialize(int_value0, "int_value0", 0);
        serializer.deserialize(int_value1, "int_value1", 0);
        serializer.deserialize(float_value0, "float_value0", 0.f);
        serializer.deserialize(float_value1, "float_value1", 0.f);
        serializer.deserialize(bool_value0, "bool_value0", true);
        serializer.deserialize(bool_value1, "bool_value1", false);
        serializer.deserialize(str_value0, "str_value0", std::string(""));
        serializer.deserialize(str_value1, "str_value1", std::string(""));
        serializer.deserialize(int_list, "int_list");
        serializer.deserialize(float_list, "float_list");
        serializer.deserialize(bool_list, "bool_list");
        serializer.deserialize(string_list, "string_list");
        serializer.deserialize(int_string_map, "int_string_map");
        serializer.deserialize(float_string_map, "float_string_map");
        serializer.deserialize(bool_string_map, "bool_string_map");
        serializer.deserialize(string_string_map, "string_string_map");
        serializer.deserialize(string_int_map, "string_int_map");
        serializer.deserialize(string_float_map, "string_float_map");
        serializer.deserialize(string_bool_map, "string_bool_map");
        serializer.deserialize(object, "object");
        serializer.deserialize(object_ptr, "object_ptr");
        serializer.deserialize(object_list, "object_list");
        serializer.deserialize(object_ptr_list, "object_ptr_list");
        serializer.deserialize(object_map, "object_map");
        serializer.deserialize(object_ptr_map, "object_ptr_map");
        serializer.deserialize(object_object_ptr_map, "object_object_ptr_map");
//        serializer.deserialize(enum_list, "enum_list");
//        serializer.deserialize(enum_map, "enum_map");
    }
    void AllTypes::serialize(SerializerJson& json) const
    {
        json.serialize(int_value0, "int_value0", 0);
        json.serialize(int_value1, "int_value1", 0);
        json.serialize(float_value0, "float_value0", 0.f);
        json.serialize(float_value1, "float_value1", 0.f);
        json.serialize(bool_value0, "bool_value0", true);
        json.serialize(bool_value1, "bool_value1", false);
        json.serialize(str_value0, "str_value0", std::string(""));
        json.serialize(str_value1, "str_value1", std::string(""));
        json.serialize(int_list, "int_list");
        json.serialize(float_list, "float_list");
        json.serialize(bool_list, "bool_list");
        json.serialize(string_list, "string_list");
        json.serialize(int_string_map, "int_string_map");
        json.serialize(float_string_map, "float_string_map");
        json.serialize(bool_string_map, "bool_string_map");
        json.serialize(string_string_map, "string_string_map");
        json.serialize(string_int_map, "string_int_map");
        json.serialize(string_float_map, "string_float_map");
        json.serialize(string_bool_map, "string_bool_map");
        json.serialize(object, "object");
        json.serialize(object_ptr, "object_ptr");
        json.serialize(object_list, "object_list");
        json.serialize(object_ptr_list, "object_ptr_list");
        json.serialize(object_map, "object_map");
        json.serialize(object_ptr_map, "object_ptr_map");
        json.serialize(enum_list, "enum_list");
        json.serialize(enum_map, "enum_map");
        json.serialize(object_object_ptr_map, "object_object_ptr_map");
    }
    void AllTypes::deserialize(DeserializerJson& json)
    {
//        json.deserialize(int_value0, "int_value0", 0);
//        json.deserialize(int_value1, "int_value1", 0);
//        json.deserialize(float_value0, "float_value0", 0.f);
//        json.deserialize(float_value1, "float_value1", 0.f);
//        json.deserialize(bool_value0, "bool_value0", true);
//        json.deserialize(bool_value1, "bool_value1", false);
//        json.deserialize(str_value0, "str_value0", std::string(""));
//        json.deserialize(str_value1, "str_value1", std::string(""));
//        json.deserialize(int_list, "int_list");
//        json.deserialize(float_list, "float_list");
//        json.deserialize(bool_list, "bool_list");
//        json.deserialize(string_list, "string_list");
//        json.deserialize(int_string_map, "int_string_map");
//        json.deserialize(float_string_map, "float_string_map");
//        json.deserialize(bool_string_map, "bool_string_map");
//        json.deserialize(string_string_map, "string_string_map");
//        json.deserialize(string_int_map, "string_int_map");
//        json.deserialize(string_float_map, "string_float_map");
//        json.deserialize(string_bool_map, "string_bool_map");
//        json.deserialize(object, "object");
//        json.deserialize(object_ptr, "object_ptr");
//        json.deserialize(object_list, "object_list");
//        json.deserialize(object_ptr_list, "object_ptr_list");
//        json.deserialize(object_map, "object_map");
//        json.deserialize(object_ptr_map, "object_ptr_map");
//        json.deserialize(enum_list, "enum_list");
//        json.deserialize(enum_map, "enum_map");
//        json.deserialize(object_object_ptr_map, "object_object_ptr_map");    
    }

} //namespace mg
