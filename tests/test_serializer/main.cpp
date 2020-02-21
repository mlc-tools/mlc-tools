#include <iostream>
#include "src/Serializer.h"
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

std::string rand_str()
{
    return "1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}";
}

void test_all_types_equals_with_old_format() {
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

    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("AllTypes");
    Serializer serializer(node);
    objA.serialize(serializer);

    if(Serializer::toStr(doc) != getAllTypesSourcesXML()) {
        std::cout << "XML:\n" << getAllTypesSourcesXML() << "END\n";
        std::cout << "XML:\n" << Serializer::toStr(doc) << "END\n";
        assert(Serializer::toStr(doc) == getAllTypesSourcesXML());
        exit(1);
    }

    Deserializer deserializer(node);
    mg::AllTypes objB;
    objB.deserialize(deserializer);

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
}
int main() {
    test_all_types_equals_with_old_format();

    //    std::cout << " xml: " << sizeof(pugi::xml_node) << "\n";
    //    std::cout << "json: " << sizeof(Json::Value) << "\n";
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    Serializer serializer(node);
    std::vector<int> v = {123, 123, 123, 345};

    // Simple types
    serializer.serialize(123, "int_node", 0);
    serializer.serialize(false, "bool_node", false);
    serializer.serialize(1.f, "float_node", 0.f);
    serializer.serialize(std::string("stream"), "string_node", std::string(""));

    // Object types
    mg::FooObject foo;
    foo.value = 1;
    serializer.serialize(foo, "foo");

    mg::intrusive_ptr<mg::FooObject> foo_ptr = mg::make_intrusive<mg::FooObject>();
    foo_ptr->value = 2;
    serializer.serialize(foo_ptr, "foo_ptr");

    mg::BarObject bar;
    bar.foo_ptr = &foo;
    serializer.serialize(bar, "bar");

    mg::BarObject bar2;
    bar2.foo_ptr = &bar;
    serializer.serialize(bar2, "bar2");

    // vector types
    std::vector<int> v_int = {1, 2, 3};
    std::vector<bool> v_bool = {true, false};
    std::vector<float> v_float = {1.f, 2.f, 5.f};
    std::vector<std::string> v_string = {std::string("123"), std::string("234")};
    serializer.serialize(v_int, "v_int");
    serializer.serialize(v_bool, "v_bool");
    serializer.serialize(v_float, "v_float");
    serializer.serialize(v_string, "v_string");

    // Map<simple, simple>
    std::map<int, int> map_i_i = {std::make_pair(1, 2)};
    std::map<bool, bool> map_b_b = {std::make_pair(true, false)};
    std::map<float, float> map_f_f = {std::make_pair(1.5f, 2.5f)};
    std::map<std::string, std::string> map_s_s = {std::make_pair("key_v", "value_v"), std::make_pair("1", "2")};
    serializer.serialize(map_i_i, "map_i_i");
    serializer.serialize(map_b_b, "map_b_b");
    serializer.serialize(map_f_f, "map_f_f");
    serializer.serialize(map_s_s, "map_s_s");

    serializer.serialize<std::string, int>({std::make_pair("123", 1)}, "map_t0");
    serializer.serialize<float, std::string>({std::make_pair(1.f, "adf")}, "map_t1");

    // Map<simple, Object>
    serializer.serialize<int, mg::FooObject>({std::make_pair(1.f, foo)}, "map_t2");
    // Map<string, Object>
    serializer.serialize<std::string, mg::FooObject>({std::make_pair("asd", foo)}, "map_t3");
    // Map<Object, Object>
    serializer.serialize<mg::FooObject, mg::FooObject>({std::make_pair(foo, foo)}, "map_foo_foo");
    serializer.serialize<mg::BarObject, mg::BarObject>({std::make_pair(bar, bar2)}, "map_bar_bar");
    // Map<Object, simple>
    serializer.serialize<mg::FooObject, int>({std::make_pair(foo, 123)}, "map_foo_s");

    // Map<simple, Object*>
    serializer.serialize(
            std::map<int, mg::intrusive_ptr<mg::FooObject>>{std::make_pair(1, mg::make_intrusive<mg::FooObject>())},
            "map_t4");
    // Map<string, Object*>
    serializer.serialize(std::map<std::string, mg::intrusive_ptr<mg::FooObject>>{std::make_pair("dsfg", nullptr)},
                         "map_t5");
    // Map<Object, Object*>

    std::map<mg::FooObject, mg::intrusive_ptr<mg::FooObject>> map_t6 = {
            std::make_pair(foo, foo_ptr),
    };
    serializer.serialize(map_t6, "map_t6");
    Deserializer deserializer(node);
    std::map<mg::FooObject, mg::intrusive_ptr<mg::FooObject>> map_t6_d;
    deserializer.deserialize(map_t6_d, "map_t6");
    serializer.serialize(map_t6_d, "map_t6_d");
    // Map<Object*, Object*>

    std::map<mg::intrusive_ptr<mg::FooObject>, mg::intrusive_ptr<mg::FooObject>> map_t7 = {
            std::make_pair(foo_ptr, foo_ptr),
    };
    serializer.serialize(map_t7, "map_t7");
    std::map<mg::intrusive_ptr<mg::FooObject>, mg::intrusive_ptr<mg::FooObject>> map_t7_d;
    deserializer.deserialize(map_t7_d, "map_t7");
    serializer.serialize(map_t7_d, "map_t7_d");


    std::vector<std::vector<bool>> list_list_bool = {{false, true}, {true, false, true, false}};
    serializer.serialize(list_list_bool, "list_list_bool");
    std::vector<std::vector<mg::FooObject>> list_foo_foo = {{foo, foo}, {foo, foo, foo, foo}};
    serializer.serialize(list_foo_foo, "list_foo_foo");

    // Const raw pointer:
    foo.name = "data_name";
    const mg::FooObject* data = &foo;
    serializer.serialize(data, std::string("data"));

    Serializer::log(doc);

    return 0;
}
