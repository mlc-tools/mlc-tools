#include <iostream>
#include <vector>
#include <map>
#include "third/jsoncpp/json.h"
#include "third/pugixml/pugixml.hpp"
#include "src/serialize/SerializerXml.h"
#include "src/serialize/SerializerJson.h"
#include "src/serialize/SerializerCommon.h"
#include "src/FooObject.h"
#include "intrusive_ptr.h"
#include "AllTypes.h"
#include "AllTypesChildren.h"
#include "TestEnum.h"
#include "mg_extensions.h"
#include "tests.h"

using namespace mg;

std::string getAllTypesSourcesXML() {
    return
#include "src/xml.h"
}

std::string getAllTypesSourcesJSON() {
    return
#include "src/json.h"
}

std::string rand_str()
{
    return "1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}";
}


AllTypes build_object(){
    AllTypes objA;
    
    objA.int_value0 = 1234;
    objA.int_value1= 6346363;
    objA.float_value0 = 100.f;
    objA.float_value1 = 1000.f;
    objA.bool_value0 = true;
    objA.bool_value1 = false;
    objA.str_value0 = rand_str();
    objA.str_value1 = rand_str();
    
    int count = 10;
    for(int i=0; i<count;++i)
        objA.int_list.push_back(i * 13);
    for(int i=0; i<count;++i)
        objA.float_list.push_back(i * 7.5f);
    for(int i=0; i<count;++i)
        objA.bool_list.push_back(i % 2 == 1);
    for(int i=0; i<count;++i)
        objA.string_list.push_back(rand_str());
    
    for (int i = 0; i < count; ++i)
        objA.int_string_map[i] = rand_str();
    for (int i = 0; i < count; ++i)
        objA.float_string_map[static_cast<float>(i)] = rand_str();
    for (int i = 0; i < 2; ++i)
        objA.bool_string_map[static_cast<bool>(i)] = rand_str();
    for (int i = 0; i < count; ++i)
        objA.string_string_map[toStr(i)] = rand_str();
    for (int i = 0; i < count; ++i)
        objA.string_int_map[toStr(i)] = i;
    for (int i = 0; i < count; ++i)
        objA.string_float_map[toStr(i)] = static_cast<float>(i);
    for (int i = 0; i < 2; ++i)
        objA.string_bool_map[toStr(i)] = static_cast<bool>(i);
    
    objA.object.value = 487998;
    
    objA.object_ptr = make_intrusive<AllTypesChildren>();
    objA.object_ptr->value = 243525235;
    
    for (int i = 0; i < count; ++i)
    {
        AllTypesChildren object;
        object.value = 132123123;
        objA.object_list.push_back(object);
    }
    for (int i = 0; i < count; ++i)
    {
        auto object_ptr = make_intrusive<AllTypesChildren>();
        object_ptr->value = 234234;
        objA.object_ptr_list.push_back(object_ptr);
    }
    for (int i = 0; i < count; ++i)
    {
        AllTypesChildren object;
        object.value = 547987;
        objA.object_map[toStr(i)] = object;
    }
    for (int i = 0; i < count; ++i)
    {
        auto object_ptr = make_intrusive<AllTypesChildren>();
        object_ptr->value = 6879;
        objA.object_ptr_map[toStr(i)] = object_ptr;
    }
    
    objA.enum_list.push_back(TestEnum::value1);
    objA.enum_list.push_back(TestEnum::value2);
    objA.enum_map[TestEnum::value1] = 1;
    objA.enum_map[TestEnum::value2] = 2;
    return objA;
}

void compare_objects(const AllTypes& objA, const AllTypes& objB){
    auto result = true;
    result = result && objA.int_value0 == objB.int_value0;
    result = result && objA.int_value1 == objB.int_value1;
    result = result && std::fabs(objA.float_value0 - objB.float_value0) < 0.0001f;
    result = result && std::fabs(objA.float_value1 - objB.float_value1) < 0.0001f;
    result = result && objA.bool_value0 == objB.bool_value0;
    result = result && objA.bool_value1 == objB.bool_value1;
    result = result && objA.str_value0 == objB.str_value0;
    result = result && objA.str_value1 == objB.str_value1;
    result = result && objA.int_list == objB.int_list;
    result = result && objA.float_list == objB.float_list;
    result = result && objA.bool_list == objB.bool_list;
    result = result && objA.string_list == objB.string_list;
    result = result && objA.int_string_map == objB.int_string_map;
    result = result && objA.float_string_map == objB.float_string_map;
    result = result && objA.bool_string_map == objB.bool_string_map;
    result = result && objA.string_string_map == objB.string_string_map;
    result = result && objA.string_int_map == objB.string_int_map;
    result = result && objA.string_float_map == objB.string_float_map;
    result = result && objA.string_bool_map == objB.string_bool_map;
    result = result && objA.object == objB.object;
    result = result && *objA.object_ptr == *objB.object_ptr;
    result = result && objA.object_list == objB.object_list;
    result = result && objA.object_map == objB.object_map;
    result = result && objA.object_ptr_list.size() == objB.object_ptr_list.size();
    result = result && objA.enum_list == objB.enum_list;
    result = result && objA.enum_map == objB.enum_map;
    
    for(size_t i=0; i<objA.object_ptr_list.size(); ++i)
        result = result && *objA.object_ptr_list[i] == *objB.object_ptr_list[i];
    for (auto& pair : objA.object_ptr_map)
    {
        auto ptrA = pair.second;
        auto ptrB = objB.object_ptr_map.at(pair.first);
        result = result && *ptrA == *ptrB;
    }
    assert(result);
    if(!result) {
        exit(1);
    }
}

void test_all_types_equals_with_old_format_xml() {
    auto objA = build_object();
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("AllTypes");
    SerializerXml serializer(node);
    objA.serialize_xml(serializer);

//    SerializerXml::log(doc);
    
    if(toStr(doc) != getAllTypesSourcesXML()) {
        std::cout << "XML:\n" << getAllTypesSourcesXML() << "END\n";
        std::cout << "XML:\n" << toStr(doc) << "END\n";
        assert(toStr(doc) == getAllTypesSourcesXML());
        exit(1);
    }
    
    DeserializerXml deserializer(node);
    AllTypes objB;
    objB.deserialize_xml(deserializer);
    
    compare_objects(objA, objB);
}

void test_all_types_equals_with_old_format_json() {
    auto objA = build_object();
    
    Json::Value json;
    SerializerJson serializer(json);
    objA.serialize_json(serializer);
    
    Json::Value jsonSource;
    Json::Reader reader;
    reader.parse(getAllTypesSourcesJSON(), jsonSource);
    
//    SerializerJson::log(json);
//    SerializerJson::log(jsonSource);

    DeserializerJson deserializer(json);
    AllTypes objB;
    objB.deserialize_json(deserializer);
    
    compare_objects(objA, objB);
}

int test_xml() {
    FooObject foo;
    foo.value = 1;
    
    intrusive_ptr<FooObject> foo_ptr = make_intrusive<FooObject>();
    foo_ptr->value = 2;
    
    BarObject bar;
    bar.foo_ptr = &foo;
    
    BarObject bar2;
    bar2.foo_ptr = &bar;
    foo.name = "data_name";

    const_cast<DataStorage&>(DataStorage::shared()).foo_objects["data_name"].name = "data_name";
    const FooObject* data = DataStorage::shared().get<FooObject>("data_name");

    int int_type = 123;
    bool bool_type = true;
    float float_type = 25.f;
    std::string string_type = "gdhsih";
    TestEnum enum_value = TestEnum::value1;
    std::vector<int> v_int = {1, 2, 3};
    std::vector<bool> v_bool = {true, false};
    std::vector<float> v_float = {1.f, 2.f, 5.f};
    std::vector<std::string> v_string = {std::string("123"), std::string("234")};
    std::vector<std::vector<bool>> list_list_bool = {{false, true}, {true, false, true, false}};
    std::vector<std::vector<FooObject>> list_foo_foo = {{foo, foo}, {foo, foo, foo, foo}};
    std::map<int, int> map_i_i = {std::make_pair(1, 2)};
    std::map<bool, bool> map_b_b = {std::make_pair(true, false)};
    std::map<float, float> map_f_f = {std::make_pair(1.5f, 2.5f)};
    std::map<std::string, std::string> map_s_s = {std::make_pair("key_v", "value_v"), std::make_pair("1", "2")};
    std::map<FooObject, intrusive_ptr<FooObject>> map_t6 = {std::make_pair(foo, foo_ptr)};
    std::map<intrusive_ptr<FooObject>, intrusive_ptr<FooObject>> map_t7 = {std::make_pair(foo_ptr, foo_ptr)};
    std::map<std::string, int> map_t8 = {std::make_pair("123", 1)};
    std::map<float, std::string> map_t9 = {std::make_pair(1.f, "adf")};
    std::map<int, FooObject> map_t10 = {std::make_pair(1.f, foo)};
    std::map<std::string, FooObject> map_t11 = {std::make_pair("asd", foo)};
    std::map<FooObject, FooObject> map_t12 = {std::make_pair(foo, foo)};
    std::map<BarObject, BarObject> map_t13 = {std::make_pair(bar, bar2)};
    std::map<FooObject, int> map_t14 = {std::make_pair(foo, 123)};
    std::map<int, intrusive_ptr<FooObject>> map_t15 = {std::make_pair(1, make_intrusive<FooObject>())};
    std::map<std::string, intrusive_ptr<FooObject>> map_t16 = {std::make_pair("dsfg", nullptr)};
    std::map<int, std::vector<int>> map_t17 = {std::make_pair<int, std::vector<int>>(1, {2, 3})};
    std::vector<const DataUnit*> units = {DataStorage::shared().get<DataUnit>("unit1")};
    std::map<const DataUnit*, int> map_units_1 = {
            std::make_pair(DataStorage::shared().get<DataUnit>("unit1"), 1),
    };
    std::map<int, const DataUnit*> map_units_2 = {
            std::make_pair(1, DataStorage::shared().get<DataUnit>("unit1")),
    };
    std::map<const DataUnit*, const DataUnit*> map_units_3 = {
            std::make_pair(DataStorage::shared().get<DataUnit>("unit1"), DataStorage::shared().get<DataUnit>("unit1")),
    };

    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");
    
    SerializerXml serializer(node);
    serializer.serialize(int_type, "int_type", 0);
    serializer.serialize(bool_type, "bool_type", false);
    serializer.serialize(float_type, "float_type", 0.f);
    serializer.serialize(string_type, "string_type", std::string(""));
    serializer.serialize(enum_value, "enum_value");
    serializer.serialize(foo, "foo");
    serializer.serialize(foo_ptr, "foo_ptr");
    serializer.serialize(bar, "bar");
    serializer.serialize(bar2, "bar2");
    serializer.serialize(v_int, "v_int");
    serializer.serialize(v_bool, "v_bool");
    serializer.serialize(v_float, "v_float");
    serializer.serialize(v_string, "v_string");
    serializer.serialize(map_i_i, "map_i_i");
    serializer.serialize(map_b_b, "map_b_b");
    serializer.serialize(map_f_f, "map_f_f");
    serializer.serialize(map_s_s, "map_s_s");
    serializer.serialize(map_t6, "map_t6");
    serializer.serialize(map_t7, "map_t7");
    serializer.serialize(map_t8, "map_t8");
    serializer.serialize(map_t9, "map_t9");
    serializer.serialize(map_t10, "map_t10");
    serializer.serialize(map_t11, "map_t11");
    serializer.serialize(map_t12, "map_t12");
    serializer.serialize(map_t13, "map_t13");
    serializer.serialize(map_t14, "map_t14");
    serializer.serialize(map_t15, "map_t15");
    serializer.serialize(map_t16, "map_t16");
    serializer.serialize(map_t17, "map_t17");
    serializer.serialize(list_list_bool, "list_list_bool");
    serializer.serialize(list_foo_foo, "list_foo_foo");
    serializer.serialize(data, std::string("data"));
    serializer.serialize(units, std::string("units"));
    serializer.serialize(map_units_1, std::string("map_units_1"));
    serializer.serialize(map_units_2, std::string("map_units_2"));
    serializer.serialize(map_units_3, std::string("map_units_3"));
    log(doc);

    TestEnum d_enum_value;
    auto d_v_int = v_int;
    auto d_v_bool = v_bool;
    auto d_v_float = v_float;
    auto d_v_string = v_string;
    auto d_map_i_i = map_i_i;
    auto d_map_b_b = map_b_b;
    auto d_map_f_f = map_f_f;
    auto d_map_s_s = map_s_s;
    auto d_map_t6 = map_t6;
    auto d_map_t7 = map_t7;
    auto d_map_t8 = map_t8;
    auto d_map_t9 = map_t9;
    auto d_map_t10 = map_t10;
    auto d_map_t11 = map_t11;
    auto d_map_t12 = map_t12;
    auto d_map_t13 = map_t13;
    auto d_map_t14 = map_t14;
    auto d_map_t15 = map_t15;
    auto d_map_t16 = map_t16;
    auto d_map_t17 = map_t17;
    auto d_list_list_bool = list_list_bool;
    auto d_list_foo_foo = list_foo_foo;
    auto d_units = units;
    auto d_map_units_1 = map_units_1;
    auto d_map_units_2 = map_units_2;
    auto d_map_units_3 = map_units_3;
    
    d_v_int.clear();
    d_v_bool.clear();
    d_v_float.clear();
    d_v_string.clear();
    d_map_i_i.clear();
    d_map_b_b.clear();
    d_map_f_f.clear();
    d_map_s_s.clear();
    d_map_t6.clear();
    d_map_t7.clear();
    d_map_t8.clear();
    d_map_t9.clear();
    d_map_t10.clear();
    d_map_t11.clear();
    d_map_t12.clear();
    d_map_t13.clear();
    d_map_t14.clear();
    d_map_t15.clear();
    d_map_t16.clear();
    d_map_t17.clear();
    d_list_list_bool.clear();
    d_list_foo_foo.clear();
    d_units.clear();
    d_map_units_1.clear();
    d_map_units_2.clear();
    d_map_units_3.clear();
    
    DeserializerXml deserializer(node);
    deserializer.deserialize(int_type, "int_type", 0);
    deserializer.deserialize(bool_type, "bool_type", false);
    deserializer.deserialize(float_type, "float_type", 0.f);
    deserializer.deserialize(string_type, "string_type", std::string(""));
    deserializer.deserialize(d_enum_value, "enum_value");
    deserializer.deserialize(foo, "foo");
    deserializer.deserialize(foo_ptr, "foo_ptr");
    deserializer.deserialize(bar, "bar");
    deserializer.deserialize(bar2, "bar2");
    deserializer.deserialize(d_v_int, "v_int");
    deserializer.deserialize(d_v_bool, "v_bool");
    deserializer.deserialize(d_v_float, "v_float");
    deserializer.deserialize(d_v_string, "v_string");
    deserializer.deserialize(d_map_i_i, "map_i_i");
    deserializer.deserialize(d_map_b_b, "map_b_b");
    deserializer.deserialize(d_map_f_f, "map_f_f");
    deserializer.deserialize(d_map_s_s, "map_s_s");
    deserializer.deserialize(d_map_t6, "map_t6");
    deserializer.deserialize(d_map_t7, "map_t7");
    deserializer.deserialize(d_map_t8, "map_t8");
    deserializer.deserialize(d_map_t9, "map_t9");
    deserializer.deserialize(d_map_t10, "map_t10");
    deserializer.deserialize(d_map_t11, "map_t11");
    deserializer.deserialize(d_map_t12, "map_t12");
    deserializer.deserialize(d_map_t13, "map_t13");
    deserializer.deserialize(d_map_t14, "map_t14");
    deserializer.deserialize(d_map_t15, "map_t15");
    deserializer.deserialize(d_map_t16, "map_t16");
    deserializer.deserialize(d_map_t17, "map_t17");
    deserializer.deserialize(d_list_list_bool, "list_list_bool");
    deserializer.deserialize(d_list_foo_foo, "list_foo_foo");
    deserializer.deserialize(data, std::string("data"));
    deserializer.deserialize(d_units, std::string("units"));
    deserializer.deserialize(d_map_units_1, std::string("map_units_1"));
    deserializer.deserialize(d_map_units_2, std::string("map_units_2"));
    deserializer.deserialize(d_map_units_3, std::string("map_units_3"));

    assert(enum_value == d_enum_value);
    assert (v_int == d_v_int);
    assert (v_bool == d_v_bool);
    assert (v_float == d_v_float);
    assert (v_string == d_v_string);
    assert (map_i_i == d_map_i_i);
    assert (map_b_b == d_map_b_b);
    assert (map_f_f == d_map_f_f);
    assert (map_s_s == d_map_s_s);
    assert (map_t6.size() == d_map_t6.size());
    assert (map_t7.size() == d_map_t7.size());
    assert (map_t8.size() == d_map_t8.size());
    assert (map_t9.size() == d_map_t9.size());
    assert (map_t10.size() == d_map_t10.size());
    assert (map_t11.size() == d_map_t11.size());
    assert (map_t12.size() == d_map_t12.size());
    assert (map_t13.size() == d_map_t13.size());
    assert (map_t14.size() == d_map_t14.size());
    assert (map_t15.size() == d_map_t15.size());
    assert (map_t16.size() == d_map_t16.size());
    assert (map_t17 == d_map_t17);
    assert (list_list_bool == d_list_list_bool);
    assert (list_foo_foo.size() == d_list_foo_foo.size());
    assert (d_units == units);
    assert (d_map_units_1 == map_units_1);
    assert (d_map_units_2 == map_units_2);
    assert (d_map_units_3 == map_units_3);

    return 0;
}

int test_json() {
    FooObject foo;
    foo.value = 1;
    
    intrusive_ptr<FooObject> foo_ptr = make_intrusive<FooObject>();
    foo_ptr->value = 2;
    
    BarObject bar;
    bar.foo_ptr = &foo;
    
    BarObject bar2;
    bar2.foo_ptr = &bar;

    const_cast<DataStorage&>(DataStorage::shared()).foo_objects["data_name"].name = "data_name";
    const FooObject* data = DataStorage::shared().get<FooObject>("data_name");

    int int_type = 123;
    bool bool_type = true;
    float float_type = 25.f;
    std::string string_type = "gdhsih";
    TestEnum enum_value = TestEnum::value1;
    std::vector<int> v_int = {0, 1, 2, 3};
    std::vector<bool> v_bool = {true, false};
    std::vector<float> v_float = {1.f, 2.f, 5.f};
    std::vector<std::string> v_string = {std::string("123"), std::string("234")};
    std::vector<std::vector<bool>> list_list_bool = {{false, true}, {true, false, true, false}};
    std::vector<intrusive_ptr<FooObject>> list_foo_ptr = {foo_ptr, foo_ptr};
    std::vector<std::vector<FooObject>> list_foo_foo = {{foo, foo}, {foo, foo, foo, foo}};
    std::map<int, int> map_i_i = {std::make_pair(1, 2)};
    std::map<bool, bool> map_b_b = {std::make_pair(true, false)};
    std::map<float, float> map_f_f = {std::make_pair(1.5f, 2.5f)};
    std::map<std::string, std::string> map_s_s = {std::make_pair("key_v", "value_v"), std::make_pair("1", "2")};
    std::map<FooObject, intrusive_ptr<FooObject>> map_t6 = {std::make_pair(foo, foo_ptr)};
    std::map<intrusive_ptr<FooObject>, intrusive_ptr<FooObject>> map_t7 = {std::make_pair(foo_ptr, foo_ptr)};
    std::map<std::string, int> map_t8 = {std::make_pair("123", 1)};
    std::map<float, std::string> map_t9 = {std::make_pair(1.f, "adf")};
    std::map<int, FooObject> map_t10 = {std::make_pair(1.f, foo)};
    std::map<std::string, FooObject> map_t11 = {std::make_pair("asd", foo)};
    std::map<FooObject, FooObject> map_t12 = {std::make_pair(foo, foo)};
    std::map<BarObject, BarObject> map_t13 = {std::make_pair(bar, bar2)};
    std::map<FooObject, int> map_t14 = {std::make_pair(foo, 123)};
    std::map<int, intrusive_ptr<FooObject>> map_t15 = {std::make_pair(1, make_intrusive<FooObject>())};
    std::map<std::string, intrusive_ptr<FooObject>> map_t16 = {std::make_pair("dsfg", nullptr)};
    std::map<int, std::vector<int>> map_t17 = {std::make_pair<int, std::vector<int>>(1, {2, 3})};
    std::vector<const DataUnit*> units = {DataStorage::shared().get<DataUnit>("unit1"), DataStorage::shared().get<DataUnit>("unit1")};
    std::map<const DataUnit*, int> map_units_1 = {
            std::make_pair(DataStorage::shared().get<DataUnit>("unit1"), 1),
    };
    std::map<int, const DataUnit*> map_units_2 = {
            std::make_pair(1, DataStorage::shared().get<DataUnit>("unit1")),
    };
    std::map<const DataUnit*, const DataUnit*> map_units_3 = {
            std::make_pair(DataStorage::shared().get<DataUnit>("unit1"), DataStorage::shared().get<DataUnit>("unit1")),
    };


    Json::Value json;
    
    SerializerJson serializer(json);
    serializer.serialize(int_type, "int_type", 0);
    serializer.serialize(bool_type, "bool_type", false);
    serializer.serialize(float_type, "float_type", 0.f);
    serializer.serialize(string_type, "string_type", std::string(""));
    serializer.serialize(enum_value, "enum_value");
    serializer.serialize(foo, "foo");
    serializer.serialize(foo_ptr, "foo_ptr");
    serializer.serialize(bar, "bar");
    serializer.serialize(bar2, "bar2");
    serializer.serialize(v_int, "v_int");
    serializer.serialize(v_bool, "v_bool");
    serializer.serialize(v_float, "v_float");
    serializer.serialize(v_string, "v_string");
    serializer.serialize(map_i_i, "map_i_i");
    serializer.serialize(map_b_b, "map_b_b");
    serializer.serialize(map_f_f, "map_f_f");
    serializer.serialize(map_s_s, "map_s_s");
    serializer.serialize(map_t6, "map_t6");
    serializer.serialize(map_t7, "map_t7");
    serializer.serialize(map_t8, "map_t8");
    serializer.serialize(map_t9, "map_t9");
    serializer.serialize(map_t10, "map_t10");
    serializer.serialize(map_t11, "map_t11");
    serializer.serialize(map_t12, "map_t12");
    serializer.serialize(map_t13, "map_t13");
    serializer.serialize(map_t14, "map_t14");
    serializer.serialize(map_t15, "map_t15");
    serializer.serialize(map_t16, "map_t16");
    serializer.serialize(map_t17, "map_t17");
    serializer.serialize(list_list_bool, "list_list_bool");
    serializer.serialize(list_foo_foo, "list_foo_foo");
    serializer.serialize(list_foo_ptr, "list_foo_ptr");
    serializer.serialize(data, std::string("data"));
    serializer.serialize(units, std::string("units"));
    serializer.serialize(map_units_1, std::string("map_units_1"));
    serializer.serialize(map_units_2, std::string("map_units_2"));
    serializer.serialize(map_units_3, std::string("map_units_3"));
    log(json);
    
    auto d_v_int = v_int;
    auto d_v_bool = v_bool;
    auto d_v_float = v_float;
    auto d_v_string = v_string;
    auto d_map_i_i = map_i_i;
    auto d_map_b_b = map_b_b;
    auto d_map_f_f = map_f_f;
    auto d_map_s_s = map_s_s;
    auto d_map_t6 = map_t6;
    auto d_map_t7 = map_t7;
    auto d_map_t8 = map_t8;
    auto d_map_t9 = map_t9;
    auto d_map_t10 = map_t10;
    auto d_map_t11 = map_t11;
    auto d_map_t12 = map_t12;
    auto d_map_t13 = map_t13;
    auto d_map_t14 = map_t14;
    auto d_map_t15 = map_t15;
    auto d_map_t16 = map_t16;
    auto d_map_t17 = map_t17;
    auto d_list_list_bool = list_list_bool;
    auto d_list_foo_foo = list_foo_foo;
    auto d_units = units;
    auto d_map_units_1 = map_units_1;
    auto d_map_units_2 = map_units_2;
    auto d_map_units_3 = map_units_3;

    TestEnum d_enum_value;
    d_v_int.clear();
    d_v_bool.clear();
    d_v_float.clear();
    d_v_string.clear();
    d_map_i_i.clear();
    d_map_b_b.clear();
    d_map_f_f.clear();
    d_map_s_s.clear();
    d_map_t6.clear();
    d_map_t7.clear();
    d_map_t8.clear();
    d_map_t9.clear();
    d_map_t10.clear();
    d_map_t11.clear();
    d_map_t12.clear();
    d_map_t13.clear();
    d_map_t14.clear();
    d_map_t15.clear();
    d_map_t16.clear();
    d_map_t17.clear();
    d_list_list_bool.clear();
    d_list_foo_foo.clear();
    d_units.clear();
    d_map_units_1.clear();
    d_map_units_2.clear();
    d_map_units_3.clear();
    
    DeserializerJson deserializer(json);
    deserializer.deserialize(int_type, "int_type", 0);
    deserializer.deserialize(bool_type, "bool_type", false);
    deserializer.deserialize(float_type, "float_type", 0.f);
    deserializer.deserialize(string_type, "string_type", std::string(""));
    deserializer.deserialize(d_enum_value, "enum_value");
    deserializer.deserialize(foo, "foo");
    deserializer.deserialize(foo_ptr, "foo_ptr");
    deserializer.deserialize(bar, "bar");
    deserializer.deserialize(bar2, "bar2");
    deserializer.deserialize(d_v_int, "v_int");
    deserializer.deserialize(d_v_bool, "v_bool");
    deserializer.deserialize(d_v_float, "v_float");
    deserializer.deserialize(d_v_string, "v_string");
    deserializer.deserialize(d_map_i_i, "map_i_i");
    deserializer.deserialize(d_map_b_b, "map_b_b");
    deserializer.deserialize(d_map_f_f, "map_f_f");
    deserializer.deserialize(d_map_s_s, "map_s_s");
    deserializer.deserialize(d_map_t6, "map_t6");
    deserializer.deserialize(d_map_t7, "map_t7");
    deserializer.deserialize(d_map_t8, "map_t8");
    deserializer.deserialize(d_map_t9, "map_t9");
    deserializer.deserialize(d_map_t10, "map_t10");
    deserializer.deserialize(d_map_t11, "map_t11");
    deserializer.deserialize(d_map_t12, "map_t12");
    deserializer.deserialize(d_map_t13, "map_t13");
    deserializer.deserialize(d_map_t14, "map_t14");
    deserializer.deserialize(d_map_t15, "map_t15");
    deserializer.deserialize(d_map_t16, "map_t16");
    deserializer.deserialize(d_map_t17, "map_t17");
    deserializer.deserialize(d_list_list_bool, "list_list_bool");
    deserializer.deserialize(d_list_foo_foo, "list_foo_foo");
    deserializer.deserialize(data, std::string("data"));
    deserializer.deserialize(d_units, std::string("units"));
    deserializer.deserialize(d_map_units_1, std::string("map_units_1"));
    deserializer.deserialize(d_map_units_2, std::string("map_units_2"));
    deserializer.deserialize(d_map_units_3, std::string("map_units_3"));

    assert(enum_value == d_enum_value);
    assert (v_int == d_v_int);
    assert (v_bool == d_v_bool);
    assert (v_float == d_v_float);
    assert (v_string == d_v_string);
    assert (map_i_i == d_map_i_i);
    assert (map_b_b == d_map_b_b);
    assert (map_f_f == d_map_f_f);
    assert (map_s_s == d_map_s_s);
    assert (map_t6.size() == d_map_t6.size());
    assert (map_t7.size() == d_map_t7.size());
    assert (map_t8.size() == d_map_t8.size());
    assert (map_t9.size() == d_map_t9.size());
    assert (map_t10.size() == d_map_t10.size());
    assert (map_t11.size() == d_map_t11.size());
    assert (map_t12.size() == d_map_t12.size());
    assert (map_t13.size() == d_map_t13.size());
    assert (map_t14.size() == d_map_t14.size());
    assert (map_t15.size() == d_map_t15.size());
    assert (map_t16.size() == d_map_t16.size());
    assert (map_t17 == d_map_t17);
    assert (list_list_bool == d_list_list_bool);
    assert (list_foo_foo.size() == d_list_foo_foo.size());
    assert (d_units == units);
    assert (d_map_units_1 == map_units_1);
    assert (d_map_units_2 == map_units_2);
    assert (d_map_units_3 == map_units_3);
    
    return 0;
}

void test_switch_enum()
{
    TestEnum enum_value = TestEnum::value1;
    switch(enum_value)
    {
        case TestEnum::value1:
            break;
        case TestEnum::value2:
            assert(0);
            break;
    }
    enum_value = TestEnum::value2;
    switch(enum_value)
    {
        case TestEnum::value1:
            assert(0);
            break;
        case TestEnum::value2:
            break;
    }
}


void test_static_asserts()
{
    static_assert(is_attribute<int>::value);
    static_assert(is_attribute<float>::value);
    static_assert(is_attribute<bool>::value);
    static_assert(is_attribute<std::string>::value);
    static_assert(is_enum<TestEnum>::value);
    static_assert(!is_attribute<TestEnum>::value);

    static_assert(is_data<const DataUnit*>::value);
    static_assert(is_data<DataUnit const*>::value);
    static_assert(!is_data<DataUnit*>::value);
    static_assert(!is_data<DataUnit* const>::value);
    static_assert(!is_data<const TestEnum*>::value);

    static_assert(is_serializable<DataUnit>::value);
    static_assert(!is_serializable<TestEnum>::value);
    static_assert(!is_serializable<int>::value);
    static_assert(!is_serializable<std::string>::value);
    static_assert(!is_serializable<intrusive_ptr<DataUnit>>::value);

    static_assert(is_intrusive<intrusive_ptr<DataUnit>>::value);
    static_assert(!is_intrusive<DataUnit>::value);
    static_assert(!is_intrusive<DataUnit*>::value);
    static_assert(!is_intrusive<const DataUnit*>::value);

    static_assert(is_not_serialize_to_attribute<std::vector<int>>::value);
    static_assert(is_not_serialize_to_attribute<std::map<int, DataUnit>>::value);
    static_assert(is_not_serialize_to_attribute<DataUnit>::value);
    static_assert(is_not_serialize_to_attribute<intrusive_ptr<DataUnit>>::value);
    static_assert(!is_not_serialize_to_attribute<int>::value);
    static_assert(!is_not_serialize_to_attribute<const DataUnit*>::value);
    static_assert(!is_not_serialize_to_attribute<TestEnum>::value);

    static_assert(std::is_same<DataUnit, data_type<const DataUnit*>::type>::value);
}

int main() {
    test_static_asserts();

    Factory::shared().registrationCommand<AllTypesChildren>(AllTypesChildren::TYPE);
    Factory::shared().registrationCommand<AllTypes>(AllTypes::TYPE);
    Factory::shared().registrationCommand<DataUnit>(DataUnit::TYPE);
    Factory::shared().registrationCommand<VisualUnit>(VisualUnit::TYPE);
    Factory::shared().registrationCommand<DataStorage>(DataStorage::TYPE);
    Factory::shared().registrationCommand<FooObject>("FooObject");
    Factory::shared().registrationCommand<BarObject>("BarObject");

    const_cast<DataStorage&>(DataStorage().shared()).units["unit1"].name = "unit1";
    const_cast<DataStorage&>(DataStorage().shared())._loaded = true;

//    std::cout << " xml: " << sizeof(pugi::xml_node) << "\n";
//    std::cout << "json: " << sizeof(Json::Value) << "\n";
//    std::cout << "iter: " << sizeof(Json::ValueIterator) << "\n";
    test_all_types_equals_with_old_format_xml();
    test_all_types_equals_with_old_format_json();
    test_xml();
    test_json();
    test_switch_enum();
    run_generated_tests();

    return 0;
}
