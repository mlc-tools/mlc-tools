#include "intrusive_ptr.h"
#include "mg_Factory.h"
#include "AllTypes.h"
#include "AllTypesChildren.h"
#include "TestEnum.h"
#include <string>
#include "mg_extensions.h"
#include "SerializerJson.h"
#include "SerializerXml.h"

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
        list_push(this->int_list, 0);
        list_push(this->int_list, 1);
        list_push(this->float_list, 0.f);
        list_push(this->float_list, 1.f);
        list_push(this->bool_list, true);
        list_push(this->bool_list, true);
        list_push(this->string_list, "0");
        list_push(this->string_list, "1");
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
        list_push(this->enum_list, TestEnum::value1);
        list_push(this->enum_list, TestEnum::value2);
        this->enum_map[TestEnum::value1] = 1;
        this->enum_map[TestEnum::value2] = 2;
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

    int AllTypes::retain()
    {
        this->_reference_counter += 1;
        return this->_reference_counter;
    }

    int AllTypes::release()
    {
        this->_reference_counter -= 1;
        auto c = this->_reference_counter;
        if( c == 0)
        {
            delete this;
        }
        return c;
    }

    std::string AllTypes::get_type() const
    {
        return AllTypes::TYPE;
    }

    void AllTypes::serialize_xml(SerializerXml& serializer) const
    {
        serializer.serialize(int_value0, "int_value0", int(0));
        serializer.serialize(int_value1, "int_value1", int(0));
        serializer.serialize(float_value0, "float_value0", float(0));
        serializer.serialize(float_value1, "float_value1", float(0.0));
        serializer.serialize(bool_value0, "bool_value0", bool(true));
        serializer.serialize(bool_value1, "bool_value1", bool(false));
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

    }

    void AllTypes::deserialize_xml(DeserializerXml& deserializer)
    {
        deserializer.deserialize(int_value0, "int_value0", int(0));
        deserializer.deserialize(int_value1, "int_value1", int(0));
        deserializer.deserialize(float_value0, "float_value0", float(0));
        deserializer.deserialize(float_value1, "float_value1", float(0.0));
        deserializer.deserialize(bool_value0, "bool_value0", bool(true));
        deserializer.deserialize(bool_value1, "bool_value1", bool(false));
        deserializer.deserialize(str_value0, "str_value0", std::string(""));
        deserializer.deserialize(str_value1, "str_value1", std::string(""));
        deserializer.deserialize(int_list, "int_list");
        deserializer.deserialize(float_list, "float_list");
        deserializer.deserialize(bool_list, "bool_list");
        deserializer.deserialize(string_list, "string_list");
        deserializer.deserialize(int_string_map, "int_string_map");
        deserializer.deserialize(float_string_map, "float_string_map");
        deserializer.deserialize(bool_string_map, "bool_string_map");
        deserializer.deserialize(string_string_map, "string_string_map");
        deserializer.deserialize(string_int_map, "string_int_map");
        deserializer.deserialize(string_float_map, "string_float_map");
        deserializer.deserialize(string_bool_map, "string_bool_map");
        deserializer.deserialize(object, "object");
        deserializer.deserialize(object_ptr, "object_ptr");
        deserializer.deserialize(object_list, "object_list");
        deserializer.deserialize(object_ptr_list, "object_ptr_list");
        deserializer.deserialize(object_map, "object_map");
        deserializer.deserialize(object_ptr_map, "object_ptr_map");
        deserializer.deserialize(enum_list, "enum_list");
        deserializer.deserialize(enum_map, "enum_map");

    }

    void AllTypes::serialize_json(SerializerJson& serializer) const
    {
        serializer.serialize(int_value0, "int_value0", int(0));
        serializer.serialize(int_value1, "int_value1", int(0));
        serializer.serialize(float_value0, "float_value0", float(0));
        serializer.serialize(float_value1, "float_value1", float(0.0));
        serializer.serialize(bool_value0, "bool_value0", bool(true));
        serializer.serialize(bool_value1, "bool_value1", bool(false));
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

    }

    void AllTypes::deserialize_json(DeserializerJson& deserializer)
    {
        deserializer.deserialize(int_value0, "int_value0", int(0));
        deserializer.deserialize(int_value1, "int_value1", int(0));
        deserializer.deserialize(float_value0, "float_value0", float(0));
        deserializer.deserialize(float_value1, "float_value1", float(0.0));
        deserializer.deserialize(bool_value0, "bool_value0", bool(true));
        deserializer.deserialize(bool_value1, "bool_value1", bool(false));
        deserializer.deserialize(str_value0, "str_value0", std::string(""));
        deserializer.deserialize(str_value1, "str_value1", std::string(""));
        deserializer.deserialize(int_list, "int_list");
        deserializer.deserialize(float_list, "float_list");
        deserializer.deserialize(bool_list, "bool_list");
        deserializer.deserialize(string_list, "string_list");
        deserializer.deserialize(int_string_map, "int_string_map");
        deserializer.deserialize(float_string_map, "float_string_map");
        deserializer.deserialize(bool_string_map, "bool_string_map");
        deserializer.deserialize(string_string_map, "string_string_map");
        deserializer.deserialize(string_int_map, "string_int_map");
        deserializer.deserialize(string_float_map, "string_float_map");
        deserializer.deserialize(string_bool_map, "string_bool_map");
        deserializer.deserialize(object, "object");
        deserializer.deserialize(object_ptr, "object_ptr");
        deserializer.deserialize(object_list, "object_list");
        deserializer.deserialize(object_ptr_list, "object_ptr_list");
        deserializer.deserialize(object_map, "object_map");
        deserializer.deserialize(object_ptr_map, "object_ptr_map");
        deserializer.deserialize(enum_list, "enum_list");
        deserializer.deserialize(enum_map, "enum_map");

    }

} //namespace mg
