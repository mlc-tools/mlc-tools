#include <iostream>
#include "src/serialize/SerializerXml.h"
#include "src/serialize/SerializerJson.h"
#include "third/pugixml/pugixml.hpp"
#include "src/FooObject.h"
#include "src/intrusive_ptr.h"
#include "src/AllTypes.h"
#include "src/AllTypesChildren.h"
#include "src/TestEnum.h"
#include <vector>
#include <map>
#include "third/jsoncpp/json.h"
#include "src/mg_extensions.h"
#include "third/jsoncpp/json.h"

std::string getAllTypesSourcesXML() {
    return "<AllTypes int_value0=\"1234\" int_value1=\"6346363\" float_value0=\"100.000000\" float_value1=\"1000.000000\" str_value0=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" str_value1=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\">\n"
           " <int_list>\n"
           "  <item />\n"
           "  <item value=\"13\" />\n"
           "  <item value=\"26\" />\n"
           "  <item value=\"39\" />\n"
           "  <item value=\"52\" />\n"
           "  <item value=\"65\" />\n"
           "  <item value=\"78\" />\n"
           "  <item value=\"91\" />\n"
           "  <item value=\"104\" />\n"
           "  <item value=\"117\" />\n"
           " </int_list>\n"
           " <float_list>\n"
           "  <item />\n"
           "  <item value=\"7.500000\" />\n"
           "  <item value=\"15.000000\" />\n"
           "  <item value=\"22.500000\" />\n"
           "  <item value=\"30.000000\" />\n"
           "  <item value=\"37.500000\" />\n"
           "  <item value=\"45.000000\" />\n"
           "  <item value=\"52.500000\" />\n"
           "  <item value=\"60.000000\" />\n"
           "  <item value=\"67.500000\" />\n"
           " </float_list>\n"
           " <bool_list>\n"
           "  <item />\n"
           "  <item value=\"true\" />\n"
           "  <item />\n"
           "  <item value=\"true\" />\n"
           "  <item />\n"
           "  <item value=\"true\" />\n"
           "  <item />\n"
           "  <item value=\"true\" />\n"
           "  <item />\n"
           "  <item value=\"true\" />\n"
           " </bool_list>\n"
           " <string_list>\n"
           "  <item value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <item value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <item value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <item value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <item value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <item value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <item value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <item value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <item value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <item value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           " </string_list>\n"
           " <int_string_map>\n"
           "  <pair value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <pair key=\"1\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <pair key=\"2\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <pair key=\"3\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <pair key=\"4\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <pair key=\"5\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <pair key=\"6\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <pair key=\"7\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <pair key=\"8\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <pair key=\"9\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           " </int_string_map>\n"
           " <float_string_map>\n"
           "  <pair value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <pair key=\"1.000000\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <pair key=\"2.000000\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <pair key=\"3.000000\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <pair key=\"4.000000\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <pair key=\"5.000000\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <pair key=\"6.000000\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <pair key=\"7.000000\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <pair key=\"8.000000\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <pair key=\"9.000000\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           " </float_string_map>\n"
           " <bool_string_map>\n"
           "  <pair value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <pair key=\"true\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           " </bool_string_map>\n"
           " <string_string_map>\n"
           "  <pair key=\"0\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <pair key=\"1\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <pair key=\"2\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <pair key=\"3\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <pair key=\"4\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <pair key=\"5\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <pair key=\"6\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <pair key=\"7\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <pair key=\"8\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           "  <pair key=\"9\" value=\"1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}\" />\n"
           " </string_string_map>\n"
           " <string_int_map>\n"
           "  <pair key=\"0\" />\n"
           "  <pair key=\"1\" value=\"1\" />\n"
           "  <pair key=\"2\" value=\"2\" />\n"
           "  <pair key=\"3\" value=\"3\" />\n"
           "  <pair key=\"4\" value=\"4\" />\n"
           "  <pair key=\"5\" value=\"5\" />\n"
           "  <pair key=\"6\" value=\"6\" />\n"
           "  <pair key=\"7\" value=\"7\" />\n"
           "  <pair key=\"8\" value=\"8\" />\n"
           "  <pair key=\"9\" value=\"9\" />\n"
           " </string_int_map>\n"
           " <string_float_map>\n"
           "  <pair key=\"0\" />\n"
           "  <pair key=\"1\" value=\"1.000000\" />\n"
           "  <pair key=\"2\" value=\"2.000000\" />\n"
           "  <pair key=\"3\" value=\"3.000000\" />\n"
           "  <pair key=\"4\" value=\"4.000000\" />\n"
           "  <pair key=\"5\" value=\"5.000000\" />\n"
           "  <pair key=\"6\" value=\"6.000000\" />\n"
           "  <pair key=\"7\" value=\"7.000000\" />\n"
           "  <pair key=\"8\" value=\"8.000000\" />\n"
           "  <pair key=\"9\" value=\"9.000000\" />\n"
           " </string_float_map>\n"
           " <string_bool_map>\n"
           "  <pair key=\"0\" />\n"
           "  <pair key=\"1\" value=\"true\" />\n"
           " </string_bool_map>\n"
           " <object value=\"487998\" />\n"
           " <object_ptr type=\"AllTypesChildren\" value=\"243525235\" />\n"
           " <object_list>\n"
           "  <item value=\"132123123\" />\n"
           "  <item value=\"132123123\" />\n"
           "  <item value=\"132123123\" />\n"
           "  <item value=\"132123123\" />\n"
           "  <item value=\"132123123\" />\n"
           "  <item value=\"132123123\" />\n"
           "  <item value=\"132123123\" />\n"
           "  <item value=\"132123123\" />\n"
           "  <item value=\"132123123\" />\n"
           "  <item value=\"132123123\" />\n"
           " </object_list>\n"
           " <object_ptr_list>\n"
           "  <AllTypesChildren value=\"234234\" />\n"
           "  <AllTypesChildren value=\"234234\" />\n"
           "  <AllTypesChildren value=\"234234\" />\n"
           "  <AllTypesChildren value=\"234234\" />\n"
           "  <AllTypesChildren value=\"234234\" />\n"
           "  <AllTypesChildren value=\"234234\" />\n"
           "  <AllTypesChildren value=\"234234\" />\n"
           "  <AllTypesChildren value=\"234234\" />\n"
           "  <AllTypesChildren value=\"234234\" />\n"
           "  <AllTypesChildren value=\"234234\" />\n"
           " </object_ptr_list>\n"
           " <object_map>\n"
           "  <pair key=\"0\">\n"
           "   <value value=\"547987\" />\n"
           "  </pair>\n"
           "  <pair key=\"1\">\n"
           "   <value value=\"547987\" />\n"
           "  </pair>\n"
           "  <pair key=\"2\">\n"
           "   <value value=\"547987\" />\n"
           "  </pair>\n"
           "  <pair key=\"3\">\n"
           "   <value value=\"547987\" />\n"
           "  </pair>\n"
           "  <pair key=\"4\">\n"
           "   <value value=\"547987\" />\n"
           "  </pair>\n"
           "  <pair key=\"5\">\n"
           "   <value value=\"547987\" />\n"
           "  </pair>\n"
           "  <pair key=\"6\">\n"
           "   <value value=\"547987\" />\n"
           "  </pair>\n"
           "  <pair key=\"7\">\n"
           "   <value value=\"547987\" />\n"
           "  </pair>\n"
           "  <pair key=\"8\">\n"
           "   <value value=\"547987\" />\n"
           "  </pair>\n"
           "  <pair key=\"9\">\n"
           "   <value value=\"547987\" />\n"
           "  </pair>\n"
           " </object_map>\n"
           " <object_ptr_map>\n"
           "  <pair key=\"0\">\n"
           "   <value type=\"AllTypesChildren\" value=\"6879\" />\n"
           "  </pair>\n"
           "  <pair key=\"1\">\n"
           "   <value type=\"AllTypesChildren\" value=\"6879\" />\n"
           "  </pair>\n"
           "  <pair key=\"2\">\n"
           "   <value type=\"AllTypesChildren\" value=\"6879\" />\n"
           "  </pair>\n"
           "  <pair key=\"3\">\n"
           "   <value type=\"AllTypesChildren\" value=\"6879\" />\n"
           "  </pair>\n"
           "  <pair key=\"4\">\n"
           "   <value type=\"AllTypesChildren\" value=\"6879\" />\n"
           "  </pair>\n"
           "  <pair key=\"5\">\n"
           "   <value type=\"AllTypesChildren\" value=\"6879\" />\n"
           "  </pair>\n"
           "  <pair key=\"6\">\n"
           "   <value type=\"AllTypesChildren\" value=\"6879\" />\n"
           "  </pair>\n"
           "  <pair key=\"7\">\n"
           "   <value type=\"AllTypesChildren\" value=\"6879\" />\n"
           "  </pair>\n"
           "  <pair key=\"8\">\n"
           "   <value type=\"AllTypesChildren\" value=\"6879\" />\n"
           "  </pair>\n"
           "  <pair key=\"9\">\n"
           "   <value type=\"AllTypesChildren\" value=\"6879\" />\n"
           "  </pair>\n"
           " </object_ptr_map>\n"
           "</AllTypes>\n";
}

std::string getAllTypesSourcesJSON() {
    return
#include "src/json.h"
}

std::string rand_str()
{
    return "1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}";
}

mg::AllTypes build_object(){
    mg::AllTypes objA;
    
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
        objA.string_string_map[mg::toStr(i)] = rand_str();
    for (int i = 0; i < count; ++i)
        objA.string_int_map[mg::toStr(i)] = i;
    for (int i = 0; i < count; ++i)
        objA.string_float_map[mg::toStr(i)] = static_cast<float>(i);
    for (int i = 0; i < 2; ++i)
        objA.string_bool_map[mg::toStr(i)] = static_cast<bool>(i);
    
    objA.object.value = 487998;
    
    objA.object_ptr = mg::make_intrusive<mg::AllTypesChildren>();
    objA.object_ptr->value = 243525235;
    
    for (int i = 0; i < count; ++i)
    {
        mg::AllTypesChildren object;
        object.value = 132123123;
        objA.object_list.push_back(object);
    }
    for (int i = 0; i < count; ++i)
    {
        auto object_ptr = mg::make_intrusive<mg::AllTypesChildren>();
        object_ptr->value = 234234;
        objA.object_ptr_list.push_back(object_ptr);
    }
    for (int i = 0; i < count; ++i)
    {
        mg::AllTypesChildren object;
        object.value = 547987;
        objA.object_map[mg::toStr(i)] = object;
    }
    for (int i = 0; i < count; ++i)
    {
        auto object_ptr = mg::make_intrusive<mg::AllTypesChildren>();
        object_ptr->value = 6879;
        objA.object_ptr_map[mg::toStr(i)] = object_ptr;
    }
    
    //TODO: map<Enum, ...>
    //    objA.enum_list.push_back(mg::TestEnum::value1);
    //    objA.enum_list.push_back(mg::TestEnum::value2);
    //    objA.enum_map[mg::TestEnum::value1] = 1;
    //    objA.enum_map[mg::TestEnum::value2] = 2;
    return objA;
}

void compare_objects(const mg::AllTypes& objA, const mg::AllTypes& objB){
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
    objA.serialize(serializer);
    
    if(SerializerXml::toStr(doc) != getAllTypesSourcesXML()) {
        std::cout << "XML:\n" << getAllTypesSourcesXML() << "END\n";
        std::cout << "XML:\n" << SerializerXml::toStr(doc) << "END\n";
        assert(SerializerXml::toStr(doc) == getAllTypesSourcesXML());
        exit(1);
    }
    
    DeserializerXml deserializer(node);
    mg::AllTypes objB;
    objB.deserialize(deserializer);
    
    compare_objects(objA, objB);
}

void test_all_types_equals_with_old_format_json() {
    auto objA = build_object();
    
    Json::Value json;
    SerializerJson serializer(json);
    objA.serialize(serializer);
    
    Json::Value jsonSource;
    Json::Reader reader;
    reader.parse(getAllTypesSourcesJSON(), jsonSource);
    
    SerializerJson::log(json);
    SerializerJson::log(jsonSource);
    
    
//    DeserializerJson deserializer(node);
//    mg::AllTypes objB;
//    objB.deserialize(deserializer);
    
//    compare_objects(objA, objB);
}

int test_xml() {
    mg::FooObject foo;
    foo.value = 1;
    
    mg::intrusive_ptr<mg::FooObject> foo_ptr = mg::make_intrusive<mg::FooObject>();
    foo_ptr->value = 2;
    
    mg::BarObject bar;
    bar.foo_ptr = &foo;
    
    mg::BarObject bar2;
    bar2.foo_ptr = &bar;
    foo.name = "data_name";
    const mg::FooObject* data = &foo;
    
    int int_type = 123;
    bool bool_type = true;
    float float_type = 25.f;
    std::string string_type = "gdhsih";
    std::vector<int> v_int = {1, 2, 3};
    std::vector<bool> v_bool = {true, false};
    std::vector<float> v_float = {1.f, 2.f, 5.f};
    std::vector<std::string> v_string = {std::string("123"), std::string("234")};
    std::vector<std::vector<bool>> list_list_bool = {{false, true}, {true, false, true, false}};
    std::vector<std::vector<mg::FooObject>> list_foo_foo = {{foo, foo}, {foo, foo, foo, foo}};
    std::map<int, int> map_i_i = {std::make_pair(1, 2)};
    std::map<bool, bool> map_b_b = {std::make_pair(true, false)};
    std::map<float, float> map_f_f = {std::make_pair(1.5f, 2.5f)};
    std::map<std::string, std::string> map_s_s = {std::make_pair("key_v", "value_v"), std::make_pair("1", "2")};
    std::map<mg::FooObject, mg::intrusive_ptr<mg::FooObject>> map_t6 = {std::make_pair(foo, foo_ptr)};
    std::map<mg::intrusive_ptr<mg::FooObject>, mg::intrusive_ptr<mg::FooObject>> map_t7 = {std::make_pair(foo_ptr, foo_ptr)};
    std::map<std::string, int> map_t8 = {std::make_pair("123", 1)};
    std::map<float, std::string> map_t9 = {std::make_pair(1.f, "adf")};
    std::map<int, mg::FooObject> map_t10 = {std::make_pair(1.f, foo)};
    std::map<std::string, mg::FooObject> map_t11 = {std::make_pair("asd", foo)};
    std::map<mg::FooObject, mg::FooObject> map_t12 = {std::make_pair(foo, foo)};
    std::map<mg::BarObject, mg::BarObject> map_t13 = {std::make_pair(bar, bar2)};
    std::map<mg::FooObject, int> map_t14 = {std::make_pair(foo, 123)};
    std::map<int, mg::intrusive_ptr<mg::FooObject>> map_t15 = {std::make_pair(1, mg::make_intrusive<mg::FooObject>())};
    std::map<std::string, mg::intrusive_ptr<mg::FooObject>> map_t16 = {std::make_pair("dsfg", nullptr)};
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");
    
    SerializerXml serializer(node);
    serializer.serialize(int_type, "int_type", 0);
    serializer.serialize(bool_type, "bool_type", false);
    serializer.serialize(float_type, "float_type", 0.f);
    serializer.serialize(string_type, "string_type", std::string(""));
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
    serializer.serialize(list_list_bool, "list_list_bool");
    serializer.serialize(list_foo_foo, "list_foo_foo");
    serializer.serialize(data, std::string("data"));
    SerializerXml::log(doc);
    
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
    auto d_list_list_bool = list_list_bool;
    auto d_list_foo_foo = list_foo_foo;
    
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
    d_list_list_bool.clear();
    d_list_foo_foo.clear();
    
    DeserializerXml deserializer(node);
    deserializer.deserialize(int_type, "int_type", 0);
    deserializer.deserialize(bool_type, "bool_type", false);
    deserializer.deserialize(float_type, "float_type", 0.f);
    deserializer.deserialize(string_type, "string_type", std::string(""));
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
    deserializer.deserialize(d_list_list_bool, "list_list_bool");
    deserializer.deserialize(d_list_foo_foo, "list_foo_foo");
    deserializer.deserialize(data, std::string("data"));
    
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
    assert (list_list_bool == d_list_list_bool);
    assert (list_foo_foo.size() == d_list_foo_foo.size());
    
    return 0;
}

int test_json() {
    mg::FooObject foo;
    foo.value = 1;
    
    mg::intrusive_ptr<mg::FooObject> foo_ptr = mg::make_intrusive<mg::FooObject>();
    foo_ptr->value = 2;
    
    mg::BarObject bar;
    bar.foo_ptr = &foo;
    
    mg::BarObject bar2;
    bar2.foo_ptr = &bar;
    foo.name = "data_name";
    const mg::FooObject* data = &foo;
    
    int int_type = 123;
    bool bool_type = true;
    float float_type = 25.f;
    std::string string_type = "gdhsih";
    std::vector<int> v_int = {1, 2, 3};
    std::vector<bool> v_bool = {true, false};
    std::vector<float> v_float = {1.f, 2.f, 5.f};
    std::vector<std::string> v_string = {std::string("123"), std::string("234")};
    std::vector<std::vector<bool>> list_list_bool = {{false, true}, {true, false, true, false}};
    std::vector<mg::intrusive_ptr<mg::FooObject>> list_foo_ptr = {foo_ptr, foo_ptr};
    std::vector<std::vector<mg::FooObject>> list_foo_foo = {{foo, foo}, {foo, foo, foo, foo}};
    std::map<int, int> map_i_i = {std::make_pair(1, 2)};
    std::map<bool, bool> map_b_b = {std::make_pair(true, false)};
    std::map<float, float> map_f_f = {std::make_pair(1.5f, 2.5f)};
    std::map<std::string, std::string> map_s_s = {std::make_pair("key_v", "value_v"), std::make_pair("1", "2")};
    std::map<mg::FooObject, mg::intrusive_ptr<mg::FooObject>> map_t6 = {std::make_pair(foo, foo_ptr)};
    std::map<mg::intrusive_ptr<mg::FooObject>, mg::intrusive_ptr<mg::FooObject>> map_t7 = {std::make_pair(foo_ptr, foo_ptr)};
    std::map<std::string, int> map_t8 = {std::make_pair("123", 1)};
    std::map<float, std::string> map_t9 = {std::make_pair(1.f, "adf")};
    std::map<int, mg::FooObject> map_t10 = {std::make_pair(1.f, foo)};
    std::map<std::string, mg::FooObject> map_t11 = {std::make_pair("asd", foo)};
    std::map<mg::FooObject, mg::FooObject> map_t12 = {std::make_pair(foo, foo)};
    std::map<mg::BarObject, mg::BarObject> map_t13 = {std::make_pair(bar, bar2)};
    std::map<mg::FooObject, int> map_t14 = {std::make_pair(foo, 123)};
    std::map<int, mg::intrusive_ptr<mg::FooObject>> map_t15 = {std::make_pair(1, mg::make_intrusive<mg::FooObject>())};
    std::map<std::string, mg::intrusive_ptr<mg::FooObject>> map_t16 = {std::make_pair("dsfg", nullptr)};
    
    Json::Value json;
    
    SerializerJson serializer(json);
    serializer.serialize(int_type, "int_type", 0);
    serializer.serialize(bool_type, "bool_type", false);
    serializer.serialize(float_type, "float_type", 0.f);
    serializer.serialize(string_type, "string_type", std::string(""));
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
    serializer.serialize(list_list_bool, "list_list_bool");
    serializer.serialize(list_foo_foo, "list_foo_foo");
    serializer.serialize(list_foo_ptr, "list_foo_ptr");
    serializer.serialize(data, std::string("data"));
    SerializerJson::log(json);
    
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
    auto d_list_list_bool = list_list_bool;
    auto d_list_foo_foo = list_foo_foo;
    
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
    d_list_list_bool.clear();
    d_list_foo_foo.clear();
    
//    DeserializerJson deserializer(json);
//    deserializer.deserialize(int_type, "int_type", 0);
//    deserializer.deserialize(bool_type, "bool_type", false);
//    deserializer.deserialize(float_type, "float_type", 0.f);
//    deserializer.deserialize(string_type, "string_type", std::string(""));
//    deserializer.deserialize(foo, "foo");
//    deserializer.deserialize(foo_ptr, "foo_ptr");
//    deserializer.deserialize(bar, "bar");
//    deserializer.deserialize(bar2, "bar2");
//    deserializer.deserialize(d_v_int, "v_int");
//    deserializer.deserialize(d_v_bool, "v_bool");
//    deserializer.deserialize(d_v_float, "v_float");
//    deserializer.deserialize(d_v_string, "v_string");
//    deserializer.deserialize(d_map_i_i, "map_i_i");
//    deserializer.deserialize(d_map_b_b, "map_b_b");
//    deserializer.deserialize(d_map_f_f, "map_f_f");
//    deserializer.deserialize(d_map_s_s, "map_s_s");
//    deserializer.deserialize(d_map_t6, "map_t6");
//    deserializer.deserialize(d_map_t7, "map_t7");
//    deserializer.deserialize(d_map_t8, "map_t8");
//    deserializer.deserialize(d_map_t9, "map_t9");
//    deserializer.deserialize(d_map_t10, "map_t10");
//    deserializer.deserialize(d_map_t11, "map_t11");
//    deserializer.deserialize(d_map_t12, "map_t12");
//    deserializer.deserialize(d_map_t13, "map_t13");
//    deserializer.deserialize(d_map_t14, "map_t14");
//    deserializer.deserialize(d_map_t15, "map_t15");
//    deserializer.deserialize(d_map_t16, "map_t16");
//    deserializer.deserialize(d_list_list_bool, "list_list_bool");
//    deserializer.deserialize(d_list_foo_foo, "list_foo_foo");
//    deserializer.deserialize(data, std::string("data"));
    
//    assert (v_int == d_v_int);
//    assert (v_bool == d_v_bool);
//    assert (v_float == d_v_float);
//    assert (v_string == d_v_string);
//    assert (map_i_i == d_map_i_i);
//    assert (map_b_b == d_map_b_b);
//    assert (map_f_f == d_map_f_f);
//    assert (map_s_s == d_map_s_s);
//    assert (map_t6.size() == d_map_t6.size());
//    assert (map_t7.size() == d_map_t7.size());
//    assert (map_t8.size() == d_map_t8.size());
//    assert (map_t9.size() == d_map_t9.size());
//    assert (map_t10.size() == d_map_t10.size());
//    assert (map_t11.size() == d_map_t11.size());
//    assert (map_t12.size() == d_map_t12.size());
//    assert (map_t13.size() == d_map_t13.size());
//    assert (map_t14.size() == d_map_t14.size());
//    assert (map_t15.size() == d_map_t15.size());
//    assert (map_t16.size() == d_map_t16.size());
//    assert (list_list_bool == d_list_list_bool);
//    assert (list_foo_foo.size() == d_list_foo_foo.size());
    
    return 0;
}

int main() {
//    std::cout << " xml: " << sizeof(pugi::xml_node) << "\n";
//    std::cout << "json: " << sizeof(Json::Value) << "\n";
//    test_all_types_equals_with_old_format_xml();
    test_all_types_equals_with_old_format_json();
//    test_xml();
//    test_json();

    return 0;
}
