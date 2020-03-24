/*
    This is generated file by generate.py script
*/
#ifndef __TESTS_H__
#define __TESTS_H__

#include "DataStorage.h"
#include "data/DataUnit.h"
#include "AllTypesChildren.h"
#include "src/serialize/SerializerXml.h"
#include "src/serialize/SerializerJson.h"
#include "intrusive_ptr.h"

using namespace mg;

inline std::string toStr(const pugi::xml_document &document)
{
    std::stringstream stream;
    pugi::xml_writer_stream writer(stream);
    document.save(writer, " ", pugi::format_no_declaration | pugi::format_indent, pugi::xml_encoding::encoding_auto);

    return stream.str();
}
inline void log(const pugi::xml_document &document)
{
    std::cout << "XML:" << std::endl << toStr(document) << std::endl;
}
inline std::string toStr(const Json::Value &json)
{
    Json::StreamWriterBuilder wbuilder;
    wbuilder["indentation"] = " ";
    return Json::writeString(wbuilder, json);
}
inline void log(const Json::Value &json)
{
    std::cout << "JSON:" << std::endl << toStr(json) << std::endl;
}


inline void test_0_xml()
{
    std::map<int, int> object1;
    std::map<int, int> object2;
    
    auto key = 123;
    auto value = 123;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<int|int>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_1_json()
{
    std::map<int, int> object1;
    std::map<int, int> object2;
    
    auto key = 123;
    auto value = 123;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<int|int>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_2_xml()
{
    std::map<int, bool> object1;
    std::map<int, bool> object2;
    
    auto key = 123;
    auto value = true;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<int|bool>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_3_json()
{
    std::map<int, bool> object1;
    std::map<int, bool> object2;
    
    auto key = 123;
    auto value = true;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<int|bool>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_4_xml()
{
    std::map<int, float> object1;
    std::map<int, float> object2;
    
    auto key = 123;
    auto value = 123.5f;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<int|float>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_5_json()
{
    std::map<int, float> object1;
    std::map<int, float> object2;
    
    auto key = 123;
    auto value = 123.5f;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<int|float>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_6_xml()
{
    std::map<int, std::string> object1;
    std::map<int, std::string> object2;
    
    auto key = 123;
    auto value = "434312some_random";
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<int|std::string>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_7_json()
{
    std::map<int, std::string> object1;
    std::map<int, std::string> object2;
    
    auto key = 123;
    auto value = "434312some_random";
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<int|std::string>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_8_xml()
{
    std::map<int, TestEnum> object1;
    std::map<int, TestEnum> object2;
    
    auto key = 123;
    auto value = TestEnum::value2;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<int|TestEnum>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_9_json()
{
    std::map<int, TestEnum> object1;
    std::map<int, TestEnum> object2;
    
    auto key = 123;
    auto value = TestEnum::value2;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<int|TestEnum>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_10_xml()
{
    std::map<int, const DataUnit*> object1;
    std::map<int, const DataUnit*> object2;
    
    auto key = 123;
    auto value = DataStorage::shared().get<DataUnit>("unit1");
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<int|const DataUnit*>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_11_json()
{
    std::map<int, const DataUnit*> object1;
    std::map<int, const DataUnit*> object2;
    
    auto key = 123;
    auto value = DataStorage::shared().get<DataUnit>("unit1");
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<int|const DataUnit*>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_12_xml()
{
    std::map<int, AllTypesChildren> object1;
    std::map<int, AllTypesChildren> object2;
    
    auto key = 123;
    auto value = AllTypesChildren();
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<int|AllTypesChildren>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_13_json()
{
    std::map<int, AllTypesChildren> object1;
    std::map<int, AllTypesChildren> object2;
    
    auto key = 123;
    auto value = AllTypesChildren();
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<int|AllTypesChildren>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_14_xml()
{
    std::map<int, intrusive_ptr<AllTypesChildren>> object1;
    std::map<int, intrusive_ptr<AllTypesChildren>> object2;
    
    auto key = 123;
    auto value = make_intrusive<AllTypesChildren>();
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<int|intrusive_ptr<AllTypesChildren>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(*value == *deserialized_value);
}

inline void test_15_json()
{
    std::map<int, intrusive_ptr<AllTypesChildren>> object1;
    std::map<int, intrusive_ptr<AllTypesChildren>> object2;
    
    auto key = 123;
    auto value = make_intrusive<AllTypesChildren>();
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<int|intrusive_ptr<AllTypesChildren>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(*value == *deserialized_value);
}

inline void test_16_xml()
{
    std::map<int, std::vector<int>> object1;
    std::map<int, std::vector<int>> object2;
    
    auto key = 123;
    auto value = std::vector<int>{1, 2, 3, 4};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<int|std::vector<int>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_17_json()
{
    std::map<int, std::vector<int>> object1;
    std::map<int, std::vector<int>> object2;
    
    auto key = 123;
    auto value = std::vector<int>{1, 2, 3, 4};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<int|std::vector<int>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_18_xml()
{
    std::map<int, std::vector<std::vector<bool>>> object1;
    std::map<int, std::vector<std::vector<bool>>> object2;
    
    auto key = 123;
    auto value = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<int|std::vector<std::vector<bool>>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_19_json()
{
    std::map<int, std::vector<std::vector<bool>>> object1;
    std::map<int, std::vector<std::vector<bool>>> object2;
    
    auto key = 123;
    auto value = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<int|std::vector<std::vector<bool>>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_20_xml()
{
    std::map<int, std::map<int, int>> object1;
    std::map<int, std::map<int, int>> object2;
    
    auto key = 123;
    auto value = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<int|std::map<int, int>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_21_json()
{
    std::map<int, std::map<int, int>> object1;
    std::map<int, std::map<int, int>> object2;
    
    auto key = 123;
    auto value = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<int|std::map<int, int>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_22_xml()
{
    std::map<bool, int> object1;
    std::map<bool, int> object2;
    
    auto key = true;
    auto value = 123;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<bool|int>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_23_json()
{
    std::map<bool, int> object1;
    std::map<bool, int> object2;
    
    auto key = true;
    auto value = 123;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<bool|int>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_24_xml()
{
    std::map<bool, bool> object1;
    std::map<bool, bool> object2;
    
    auto key = true;
    auto value = true;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<bool|bool>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_25_json()
{
    std::map<bool, bool> object1;
    std::map<bool, bool> object2;
    
    auto key = true;
    auto value = true;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<bool|bool>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_26_xml()
{
    std::map<bool, float> object1;
    std::map<bool, float> object2;
    
    auto key = true;
    auto value = 123.5f;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<bool|float>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_27_json()
{
    std::map<bool, float> object1;
    std::map<bool, float> object2;
    
    auto key = true;
    auto value = 123.5f;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<bool|float>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_28_xml()
{
    std::map<bool, std::string> object1;
    std::map<bool, std::string> object2;
    
    auto key = true;
    auto value = "434312some_random";
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<bool|std::string>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_29_json()
{
    std::map<bool, std::string> object1;
    std::map<bool, std::string> object2;
    
    auto key = true;
    auto value = "434312some_random";
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<bool|std::string>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_30_xml()
{
    std::map<bool, TestEnum> object1;
    std::map<bool, TestEnum> object2;
    
    auto key = true;
    auto value = TestEnum::value2;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<bool|TestEnum>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_31_json()
{
    std::map<bool, TestEnum> object1;
    std::map<bool, TestEnum> object2;
    
    auto key = true;
    auto value = TestEnum::value2;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<bool|TestEnum>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_32_xml()
{
    std::map<bool, const DataUnit*> object1;
    std::map<bool, const DataUnit*> object2;
    
    auto key = true;
    auto value = DataStorage::shared().get<DataUnit>("unit1");
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<bool|const DataUnit*>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_33_json()
{
    std::map<bool, const DataUnit*> object1;
    std::map<bool, const DataUnit*> object2;
    
    auto key = true;
    auto value = DataStorage::shared().get<DataUnit>("unit1");
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<bool|const DataUnit*>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_34_xml()
{
    std::map<bool, AllTypesChildren> object1;
    std::map<bool, AllTypesChildren> object2;
    
    auto key = true;
    auto value = AllTypesChildren();
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<bool|AllTypesChildren>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_35_json()
{
    std::map<bool, AllTypesChildren> object1;
    std::map<bool, AllTypesChildren> object2;
    
    auto key = true;
    auto value = AllTypesChildren();
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<bool|AllTypesChildren>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_36_xml()
{
    std::map<bool, intrusive_ptr<AllTypesChildren>> object1;
    std::map<bool, intrusive_ptr<AllTypesChildren>> object2;
    
    auto key = true;
    auto value = make_intrusive<AllTypesChildren>();
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<bool|intrusive_ptr<AllTypesChildren>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(*value == *deserialized_value);
}

inline void test_37_json()
{
    std::map<bool, intrusive_ptr<AllTypesChildren>> object1;
    std::map<bool, intrusive_ptr<AllTypesChildren>> object2;
    
    auto key = true;
    auto value = make_intrusive<AllTypesChildren>();
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<bool|intrusive_ptr<AllTypesChildren>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(*value == *deserialized_value);
}

inline void test_38_xml()
{
    std::map<bool, std::vector<int>> object1;
    std::map<bool, std::vector<int>> object2;
    
    auto key = true;
    auto value = std::vector<int>{1, 2, 3, 4};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<bool|std::vector<int>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_39_json()
{
    std::map<bool, std::vector<int>> object1;
    std::map<bool, std::vector<int>> object2;
    
    auto key = true;
    auto value = std::vector<int>{1, 2, 3, 4};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<bool|std::vector<int>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_40_xml()
{
    std::map<bool, std::vector<std::vector<bool>>> object1;
    std::map<bool, std::vector<std::vector<bool>>> object2;
    
    auto key = true;
    auto value = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<bool|std::vector<std::vector<bool>>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_41_json()
{
    std::map<bool, std::vector<std::vector<bool>>> object1;
    std::map<bool, std::vector<std::vector<bool>>> object2;
    
    auto key = true;
    auto value = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<bool|std::vector<std::vector<bool>>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_42_xml()
{
    std::map<bool, std::map<int, int>> object1;
    std::map<bool, std::map<int, int>> object2;
    
    auto key = true;
    auto value = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<bool|std::map<int, int>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_43_json()
{
    std::map<bool, std::map<int, int>> object1;
    std::map<bool, std::map<int, int>> object2;
    
    auto key = true;
    auto value = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<bool|std::map<int, int>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_44_xml()
{
    std::map<float, int> object1;
    std::map<float, int> object2;
    
    auto key = 123.5f;
    auto value = 123;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<float|int>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_45_json()
{
    std::map<float, int> object1;
    std::map<float, int> object2;
    
    auto key = 123.5f;
    auto value = 123;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<float|int>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_46_xml()
{
    std::map<float, bool> object1;
    std::map<float, bool> object2;
    
    auto key = 123.5f;
    auto value = true;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<float|bool>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_47_json()
{
    std::map<float, bool> object1;
    std::map<float, bool> object2;
    
    auto key = 123.5f;
    auto value = true;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<float|bool>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_48_xml()
{
    std::map<float, float> object1;
    std::map<float, float> object2;
    
    auto key = 123.5f;
    auto value = 123.5f;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<float|float>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_49_json()
{
    std::map<float, float> object1;
    std::map<float, float> object2;
    
    auto key = 123.5f;
    auto value = 123.5f;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<float|float>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_50_xml()
{
    std::map<float, std::string> object1;
    std::map<float, std::string> object2;
    
    auto key = 123.5f;
    auto value = "434312some_random";
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<float|std::string>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_51_json()
{
    std::map<float, std::string> object1;
    std::map<float, std::string> object2;
    
    auto key = 123.5f;
    auto value = "434312some_random";
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<float|std::string>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_52_xml()
{
    std::map<float, TestEnum> object1;
    std::map<float, TestEnum> object2;
    
    auto key = 123.5f;
    auto value = TestEnum::value2;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<float|TestEnum>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_53_json()
{
    std::map<float, TestEnum> object1;
    std::map<float, TestEnum> object2;
    
    auto key = 123.5f;
    auto value = TestEnum::value2;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<float|TestEnum>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_54_xml()
{
    std::map<float, const DataUnit*> object1;
    std::map<float, const DataUnit*> object2;
    
    auto key = 123.5f;
    auto value = DataStorage::shared().get<DataUnit>("unit1");
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<float|const DataUnit*>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_55_json()
{
    std::map<float, const DataUnit*> object1;
    std::map<float, const DataUnit*> object2;
    
    auto key = 123.5f;
    auto value = DataStorage::shared().get<DataUnit>("unit1");
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<float|const DataUnit*>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_56_xml()
{
    std::map<float, AllTypesChildren> object1;
    std::map<float, AllTypesChildren> object2;
    
    auto key = 123.5f;
    auto value = AllTypesChildren();
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<float|AllTypesChildren>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_57_json()
{
    std::map<float, AllTypesChildren> object1;
    std::map<float, AllTypesChildren> object2;
    
    auto key = 123.5f;
    auto value = AllTypesChildren();
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<float|AllTypesChildren>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_58_xml()
{
    std::map<float, intrusive_ptr<AllTypesChildren>> object1;
    std::map<float, intrusive_ptr<AllTypesChildren>> object2;
    
    auto key = 123.5f;
    auto value = make_intrusive<AllTypesChildren>();
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<float|intrusive_ptr<AllTypesChildren>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(*value == *deserialized_value);
}

inline void test_59_json()
{
    std::map<float, intrusive_ptr<AllTypesChildren>> object1;
    std::map<float, intrusive_ptr<AllTypesChildren>> object2;
    
    auto key = 123.5f;
    auto value = make_intrusive<AllTypesChildren>();
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<float|intrusive_ptr<AllTypesChildren>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(*value == *deserialized_value);
}

inline void test_60_xml()
{
    std::map<float, std::vector<int>> object1;
    std::map<float, std::vector<int>> object2;
    
    auto key = 123.5f;
    auto value = std::vector<int>{1, 2, 3, 4};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<float|std::vector<int>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_61_json()
{
    std::map<float, std::vector<int>> object1;
    std::map<float, std::vector<int>> object2;
    
    auto key = 123.5f;
    auto value = std::vector<int>{1, 2, 3, 4};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<float|std::vector<int>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_62_xml()
{
    std::map<float, std::vector<std::vector<bool>>> object1;
    std::map<float, std::vector<std::vector<bool>>> object2;
    
    auto key = 123.5f;
    auto value = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<float|std::vector<std::vector<bool>>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_63_json()
{
    std::map<float, std::vector<std::vector<bool>>> object1;
    std::map<float, std::vector<std::vector<bool>>> object2;
    
    auto key = 123.5f;
    auto value = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<float|std::vector<std::vector<bool>>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_64_xml()
{
    std::map<float, std::map<int, int>> object1;
    std::map<float, std::map<int, int>> object2;
    
    auto key = 123.5f;
    auto value = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<float|std::map<int, int>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_65_json()
{
    std::map<float, std::map<int, int>> object1;
    std::map<float, std::map<int, int>> object2;
    
    auto key = 123.5f;
    auto value = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<float|std::map<int, int>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_66_xml()
{
    std::map<std::string, int> object1;
    std::map<std::string, int> object2;
    
    auto key = "434312some_random";
    auto value = 123;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::string|int>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_67_json()
{
    std::map<std::string, int> object1;
    std::map<std::string, int> object2;
    
    auto key = "434312some_random";
    auto value = 123;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::string|int>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_68_xml()
{
    std::map<std::string, bool> object1;
    std::map<std::string, bool> object2;
    
    auto key = "434312some_random";
    auto value = true;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::string|bool>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_69_json()
{
    std::map<std::string, bool> object1;
    std::map<std::string, bool> object2;
    
    auto key = "434312some_random";
    auto value = true;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::string|bool>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_70_xml()
{
    std::map<std::string, float> object1;
    std::map<std::string, float> object2;
    
    auto key = "434312some_random";
    auto value = 123.5f;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::string|float>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_71_json()
{
    std::map<std::string, float> object1;
    std::map<std::string, float> object2;
    
    auto key = "434312some_random";
    auto value = 123.5f;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::string|float>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_72_xml()
{
    std::map<std::string, std::string> object1;
    std::map<std::string, std::string> object2;
    
    auto key = "434312some_random";
    auto value = "434312some_random";
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::string|std::string>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_73_json()
{
    std::map<std::string, std::string> object1;
    std::map<std::string, std::string> object2;
    
    auto key = "434312some_random";
    auto value = "434312some_random";
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::string|std::string>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_74_xml()
{
    std::map<std::string, TestEnum> object1;
    std::map<std::string, TestEnum> object2;
    
    auto key = "434312some_random";
    auto value = TestEnum::value2;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::string|TestEnum>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_75_json()
{
    std::map<std::string, TestEnum> object1;
    std::map<std::string, TestEnum> object2;
    
    auto key = "434312some_random";
    auto value = TestEnum::value2;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::string|TestEnum>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_76_xml()
{
    std::map<std::string, const DataUnit*> object1;
    std::map<std::string, const DataUnit*> object2;
    
    auto key = "434312some_random";
    auto value = DataStorage::shared().get<DataUnit>("unit1");
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::string|const DataUnit*>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_77_json()
{
    std::map<std::string, const DataUnit*> object1;
    std::map<std::string, const DataUnit*> object2;
    
    auto key = "434312some_random";
    auto value = DataStorage::shared().get<DataUnit>("unit1");
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::string|const DataUnit*>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_78_xml()
{
    std::map<std::string, AllTypesChildren> object1;
    std::map<std::string, AllTypesChildren> object2;
    
    auto key = "434312some_random";
    auto value = AllTypesChildren();
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::string|AllTypesChildren>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_79_json()
{
    std::map<std::string, AllTypesChildren> object1;
    std::map<std::string, AllTypesChildren> object2;
    
    auto key = "434312some_random";
    auto value = AllTypesChildren();
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::string|AllTypesChildren>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_80_xml()
{
    std::map<std::string, intrusive_ptr<AllTypesChildren>> object1;
    std::map<std::string, intrusive_ptr<AllTypesChildren>> object2;
    
    auto key = "434312some_random";
    auto value = make_intrusive<AllTypesChildren>();
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::string|intrusive_ptr<AllTypesChildren>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(*value == *deserialized_value);
}

inline void test_81_json()
{
    std::map<std::string, intrusive_ptr<AllTypesChildren>> object1;
    std::map<std::string, intrusive_ptr<AllTypesChildren>> object2;
    
    auto key = "434312some_random";
    auto value = make_intrusive<AllTypesChildren>();
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::string|intrusive_ptr<AllTypesChildren>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(*value == *deserialized_value);
}

inline void test_82_xml()
{
    std::map<std::string, std::vector<int>> object1;
    std::map<std::string, std::vector<int>> object2;
    
    auto key = "434312some_random";
    auto value = std::vector<int>{1, 2, 3, 4};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::string|std::vector<int>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_83_json()
{
    std::map<std::string, std::vector<int>> object1;
    std::map<std::string, std::vector<int>> object2;
    
    auto key = "434312some_random";
    auto value = std::vector<int>{1, 2, 3, 4};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::string|std::vector<int>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_84_xml()
{
    std::map<std::string, std::vector<std::vector<bool>>> object1;
    std::map<std::string, std::vector<std::vector<bool>>> object2;
    
    auto key = "434312some_random";
    auto value = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::string|std::vector<std::vector<bool>>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_85_json()
{
    std::map<std::string, std::vector<std::vector<bool>>> object1;
    std::map<std::string, std::vector<std::vector<bool>>> object2;
    
    auto key = "434312some_random";
    auto value = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::string|std::vector<std::vector<bool>>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_86_xml()
{
    std::map<std::string, std::map<int, int>> object1;
    std::map<std::string, std::map<int, int>> object2;
    
    auto key = "434312some_random";
    auto value = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::string|std::map<int, int>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_87_json()
{
    std::map<std::string, std::map<int, int>> object1;
    std::map<std::string, std::map<int, int>> object2;
    
    auto key = "434312some_random";
    auto value = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::string|std::map<int, int>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_88_xml()
{
    std::map<TestEnum, int> object1;
    std::map<TestEnum, int> object2;
    
    auto key = TestEnum::value2;
    auto value = 123;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<TestEnum|int>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_89_json()
{
    std::map<TestEnum, int> object1;
    std::map<TestEnum, int> object2;
    
    auto key = TestEnum::value2;
    auto value = 123;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<TestEnum|int>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_90_xml()
{
    std::map<TestEnum, bool> object1;
    std::map<TestEnum, bool> object2;
    
    auto key = TestEnum::value2;
    auto value = true;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<TestEnum|bool>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_91_json()
{
    std::map<TestEnum, bool> object1;
    std::map<TestEnum, bool> object2;
    
    auto key = TestEnum::value2;
    auto value = true;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<TestEnum|bool>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_92_xml()
{
    std::map<TestEnum, float> object1;
    std::map<TestEnum, float> object2;
    
    auto key = TestEnum::value2;
    auto value = 123.5f;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<TestEnum|float>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_93_json()
{
    std::map<TestEnum, float> object1;
    std::map<TestEnum, float> object2;
    
    auto key = TestEnum::value2;
    auto value = 123.5f;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<TestEnum|float>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_94_xml()
{
    std::map<TestEnum, std::string> object1;
    std::map<TestEnum, std::string> object2;
    
    auto key = TestEnum::value2;
    auto value = "434312some_random";
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<TestEnum|std::string>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_95_json()
{
    std::map<TestEnum, std::string> object1;
    std::map<TestEnum, std::string> object2;
    
    auto key = TestEnum::value2;
    auto value = "434312some_random";
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<TestEnum|std::string>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_96_xml()
{
    std::map<TestEnum, TestEnum> object1;
    std::map<TestEnum, TestEnum> object2;
    
    auto key = TestEnum::value2;
    auto value = TestEnum::value2;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<TestEnum|TestEnum>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_97_json()
{
    std::map<TestEnum, TestEnum> object1;
    std::map<TestEnum, TestEnum> object2;
    
    auto key = TestEnum::value2;
    auto value = TestEnum::value2;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<TestEnum|TestEnum>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_98_xml()
{
    std::map<TestEnum, const DataUnit*> object1;
    std::map<TestEnum, const DataUnit*> object2;
    
    auto key = TestEnum::value2;
    auto value = DataStorage::shared().get<DataUnit>("unit1");
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<TestEnum|const DataUnit*>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_99_json()
{
    std::map<TestEnum, const DataUnit*> object1;
    std::map<TestEnum, const DataUnit*> object2;
    
    auto key = TestEnum::value2;
    auto value = DataStorage::shared().get<DataUnit>("unit1");
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<TestEnum|const DataUnit*>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_100_xml()
{
    std::map<TestEnum, AllTypesChildren> object1;
    std::map<TestEnum, AllTypesChildren> object2;
    
    auto key = TestEnum::value2;
    auto value = AllTypesChildren();
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<TestEnum|AllTypesChildren>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_101_json()
{
    std::map<TestEnum, AllTypesChildren> object1;
    std::map<TestEnum, AllTypesChildren> object2;
    
    auto key = TestEnum::value2;
    auto value = AllTypesChildren();
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<TestEnum|AllTypesChildren>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_102_xml()
{
    std::map<TestEnum, intrusive_ptr<AllTypesChildren>> object1;
    std::map<TestEnum, intrusive_ptr<AllTypesChildren>> object2;
    
    auto key = TestEnum::value2;
    auto value = make_intrusive<AllTypesChildren>();
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<TestEnum|intrusive_ptr<AllTypesChildren>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(*value == *deserialized_value);
}

inline void test_103_json()
{
    std::map<TestEnum, intrusive_ptr<AllTypesChildren>> object1;
    std::map<TestEnum, intrusive_ptr<AllTypesChildren>> object2;
    
    auto key = TestEnum::value2;
    auto value = make_intrusive<AllTypesChildren>();
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<TestEnum|intrusive_ptr<AllTypesChildren>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(*value == *deserialized_value);
}

inline void test_104_xml()
{
    std::map<TestEnum, std::vector<int>> object1;
    std::map<TestEnum, std::vector<int>> object2;
    
    auto key = TestEnum::value2;
    auto value = std::vector<int>{1, 2, 3, 4};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<TestEnum|std::vector<int>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_105_json()
{
    std::map<TestEnum, std::vector<int>> object1;
    std::map<TestEnum, std::vector<int>> object2;
    
    auto key = TestEnum::value2;
    auto value = std::vector<int>{1, 2, 3, 4};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<TestEnum|std::vector<int>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_106_xml()
{
    std::map<TestEnum, std::vector<std::vector<bool>>> object1;
    std::map<TestEnum, std::vector<std::vector<bool>>> object2;
    
    auto key = TestEnum::value2;
    auto value = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<TestEnum|std::vector<std::vector<bool>>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_107_json()
{
    std::map<TestEnum, std::vector<std::vector<bool>>> object1;
    std::map<TestEnum, std::vector<std::vector<bool>>> object2;
    
    auto key = TestEnum::value2;
    auto value = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<TestEnum|std::vector<std::vector<bool>>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_108_xml()
{
    std::map<TestEnum, std::map<int, int>> object1;
    std::map<TestEnum, std::map<int, int>> object2;
    
    auto key = TestEnum::value2;
    auto value = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<TestEnum|std::map<int, int>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_109_json()
{
    std::map<TestEnum, std::map<int, int>> object1;
    std::map<TestEnum, std::map<int, int>> object2;
    
    auto key = TestEnum::value2;
    auto value = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<TestEnum|std::map<int, int>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_110_xml()
{
    std::map<const DataUnit*, int> object1;
    std::map<const DataUnit*, int> object2;
    
    auto key = DataStorage::shared().get<DataUnit>("unit1");
    auto value = 123;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<const DataUnit*|int>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_111_json()
{
    std::map<const DataUnit*, int> object1;
    std::map<const DataUnit*, int> object2;
    
    auto key = DataStorage::shared().get<DataUnit>("unit1");
    auto value = 123;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<const DataUnit*|int>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_112_xml()
{
    std::map<const DataUnit*, bool> object1;
    std::map<const DataUnit*, bool> object2;
    
    auto key = DataStorage::shared().get<DataUnit>("unit1");
    auto value = true;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<const DataUnit*|bool>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_113_json()
{
    std::map<const DataUnit*, bool> object1;
    std::map<const DataUnit*, bool> object2;
    
    auto key = DataStorage::shared().get<DataUnit>("unit1");
    auto value = true;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<const DataUnit*|bool>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_114_xml()
{
    std::map<const DataUnit*, float> object1;
    std::map<const DataUnit*, float> object2;
    
    auto key = DataStorage::shared().get<DataUnit>("unit1");
    auto value = 123.5f;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<const DataUnit*|float>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_115_json()
{
    std::map<const DataUnit*, float> object1;
    std::map<const DataUnit*, float> object2;
    
    auto key = DataStorage::shared().get<DataUnit>("unit1");
    auto value = 123.5f;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<const DataUnit*|float>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_116_xml()
{
    std::map<const DataUnit*, std::string> object1;
    std::map<const DataUnit*, std::string> object2;
    
    auto key = DataStorage::shared().get<DataUnit>("unit1");
    auto value = "434312some_random";
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<const DataUnit*|std::string>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_117_json()
{
    std::map<const DataUnit*, std::string> object1;
    std::map<const DataUnit*, std::string> object2;
    
    auto key = DataStorage::shared().get<DataUnit>("unit1");
    auto value = "434312some_random";
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<const DataUnit*|std::string>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_118_xml()
{
    std::map<const DataUnit*, TestEnum> object1;
    std::map<const DataUnit*, TestEnum> object2;
    
    auto key = DataStorage::shared().get<DataUnit>("unit1");
    auto value = TestEnum::value2;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<const DataUnit*|TestEnum>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_119_json()
{
    std::map<const DataUnit*, TestEnum> object1;
    std::map<const DataUnit*, TestEnum> object2;
    
    auto key = DataStorage::shared().get<DataUnit>("unit1");
    auto value = TestEnum::value2;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<const DataUnit*|TestEnum>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_120_xml()
{
    std::map<const DataUnit*, const DataUnit*> object1;
    std::map<const DataUnit*, const DataUnit*> object2;
    
    auto key = DataStorage::shared().get<DataUnit>("unit1");
    auto value = DataStorage::shared().get<DataUnit>("unit1");
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<const DataUnit*|const DataUnit*>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_121_json()
{
    std::map<const DataUnit*, const DataUnit*> object1;
    std::map<const DataUnit*, const DataUnit*> object2;
    
    auto key = DataStorage::shared().get<DataUnit>("unit1");
    auto value = DataStorage::shared().get<DataUnit>("unit1");
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<const DataUnit*|const DataUnit*>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_122_xml()
{
    std::map<const DataUnit*, AllTypesChildren> object1;
    std::map<const DataUnit*, AllTypesChildren> object2;
    
    auto key = DataStorage::shared().get<DataUnit>("unit1");
    auto value = AllTypesChildren();
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<const DataUnit*|AllTypesChildren>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_123_json()
{
    std::map<const DataUnit*, AllTypesChildren> object1;
    std::map<const DataUnit*, AllTypesChildren> object2;
    
    auto key = DataStorage::shared().get<DataUnit>("unit1");
    auto value = AllTypesChildren();
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<const DataUnit*|AllTypesChildren>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_124_xml()
{
    std::map<const DataUnit*, intrusive_ptr<AllTypesChildren>> object1;
    std::map<const DataUnit*, intrusive_ptr<AllTypesChildren>> object2;
    
    auto key = DataStorage::shared().get<DataUnit>("unit1");
    auto value = make_intrusive<AllTypesChildren>();
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<const DataUnit*|intrusive_ptr<AllTypesChildren>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(*value == *deserialized_value);
}

inline void test_125_json()
{
    std::map<const DataUnit*, intrusive_ptr<AllTypesChildren>> object1;
    std::map<const DataUnit*, intrusive_ptr<AllTypesChildren>> object2;
    
    auto key = DataStorage::shared().get<DataUnit>("unit1");
    auto value = make_intrusive<AllTypesChildren>();
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<const DataUnit*|intrusive_ptr<AllTypesChildren>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(*value == *deserialized_value);
}

inline void test_126_xml()
{
    std::map<const DataUnit*, std::vector<int>> object1;
    std::map<const DataUnit*, std::vector<int>> object2;
    
    auto key = DataStorage::shared().get<DataUnit>("unit1");
    auto value = std::vector<int>{1, 2, 3, 4};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<const DataUnit*|std::vector<int>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_127_json()
{
    std::map<const DataUnit*, std::vector<int>> object1;
    std::map<const DataUnit*, std::vector<int>> object2;
    
    auto key = DataStorage::shared().get<DataUnit>("unit1");
    auto value = std::vector<int>{1, 2, 3, 4};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<const DataUnit*|std::vector<int>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_128_xml()
{
    std::map<const DataUnit*, std::vector<std::vector<bool>>> object1;
    std::map<const DataUnit*, std::vector<std::vector<bool>>> object2;
    
    auto key = DataStorage::shared().get<DataUnit>("unit1");
    auto value = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<const DataUnit*|std::vector<std::vector<bool>>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_129_json()
{
    std::map<const DataUnit*, std::vector<std::vector<bool>>> object1;
    std::map<const DataUnit*, std::vector<std::vector<bool>>> object2;
    
    auto key = DataStorage::shared().get<DataUnit>("unit1");
    auto value = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<const DataUnit*|std::vector<std::vector<bool>>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_130_xml()
{
    std::map<const DataUnit*, std::map<int, int>> object1;
    std::map<const DataUnit*, std::map<int, int>> object2;
    
    auto key = DataStorage::shared().get<DataUnit>("unit1");
    auto value = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<const DataUnit*|std::map<int, int>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_131_json()
{
    std::map<const DataUnit*, std::map<int, int>> object1;
    std::map<const DataUnit*, std::map<int, int>> object2;
    
    auto key = DataStorage::shared().get<DataUnit>("unit1");
    auto value = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<const DataUnit*|std::map<int, int>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_132_xml()
{
    std::map<AllTypesChildren, int> object1;
    std::map<AllTypesChildren, int> object2;
    
    auto key = AllTypesChildren();
    auto value = 123;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<AllTypesChildren|int>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_133_json()
{
    std::map<AllTypesChildren, int> object1;
    std::map<AllTypesChildren, int> object2;
    
    auto key = AllTypesChildren();
    auto value = 123;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<AllTypesChildren|int>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_134_xml()
{
    std::map<AllTypesChildren, bool> object1;
    std::map<AllTypesChildren, bool> object2;
    
    auto key = AllTypesChildren();
    auto value = true;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<AllTypesChildren|bool>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_135_json()
{
    std::map<AllTypesChildren, bool> object1;
    std::map<AllTypesChildren, bool> object2;
    
    auto key = AllTypesChildren();
    auto value = true;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<AllTypesChildren|bool>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_136_xml()
{
    std::map<AllTypesChildren, float> object1;
    std::map<AllTypesChildren, float> object2;
    
    auto key = AllTypesChildren();
    auto value = 123.5f;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<AllTypesChildren|float>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_137_json()
{
    std::map<AllTypesChildren, float> object1;
    std::map<AllTypesChildren, float> object2;
    
    auto key = AllTypesChildren();
    auto value = 123.5f;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<AllTypesChildren|float>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_138_xml()
{
    std::map<AllTypesChildren, std::string> object1;
    std::map<AllTypesChildren, std::string> object2;
    
    auto key = AllTypesChildren();
    auto value = "434312some_random";
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<AllTypesChildren|std::string>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_139_json()
{
    std::map<AllTypesChildren, std::string> object1;
    std::map<AllTypesChildren, std::string> object2;
    
    auto key = AllTypesChildren();
    auto value = "434312some_random";
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<AllTypesChildren|std::string>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_140_xml()
{
    std::map<AllTypesChildren, TestEnum> object1;
    std::map<AllTypesChildren, TestEnum> object2;
    
    auto key = AllTypesChildren();
    auto value = TestEnum::value2;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<AllTypesChildren|TestEnum>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_141_json()
{
    std::map<AllTypesChildren, TestEnum> object1;
    std::map<AllTypesChildren, TestEnum> object2;
    
    auto key = AllTypesChildren();
    auto value = TestEnum::value2;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<AllTypesChildren|TestEnum>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_142_xml()
{
    std::map<AllTypesChildren, const DataUnit*> object1;
    std::map<AllTypesChildren, const DataUnit*> object2;
    
    auto key = AllTypesChildren();
    auto value = DataStorage::shared().get<DataUnit>("unit1");
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<AllTypesChildren|const DataUnit*>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_143_json()
{
    std::map<AllTypesChildren, const DataUnit*> object1;
    std::map<AllTypesChildren, const DataUnit*> object2;
    
    auto key = AllTypesChildren();
    auto value = DataStorage::shared().get<DataUnit>("unit1");
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<AllTypesChildren|const DataUnit*>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_144_xml()
{
    std::map<AllTypesChildren, AllTypesChildren> object1;
    std::map<AllTypesChildren, AllTypesChildren> object2;
    
    auto key = AllTypesChildren();
    auto value = AllTypesChildren();
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<AllTypesChildren|AllTypesChildren>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_145_json()
{
    std::map<AllTypesChildren, AllTypesChildren> object1;
    std::map<AllTypesChildren, AllTypesChildren> object2;
    
    auto key = AllTypesChildren();
    auto value = AllTypesChildren();
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<AllTypesChildren|AllTypesChildren>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_146_xml()
{
    std::map<AllTypesChildren, intrusive_ptr<AllTypesChildren>> object1;
    std::map<AllTypesChildren, intrusive_ptr<AllTypesChildren>> object2;
    
    auto key = AllTypesChildren();
    auto value = make_intrusive<AllTypesChildren>();
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<AllTypesChildren|intrusive_ptr<AllTypesChildren>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(*value == *deserialized_value);
}

inline void test_147_json()
{
    std::map<AllTypesChildren, intrusive_ptr<AllTypesChildren>> object1;
    std::map<AllTypesChildren, intrusive_ptr<AllTypesChildren>> object2;
    
    auto key = AllTypesChildren();
    auto value = make_intrusive<AllTypesChildren>();
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<AllTypesChildren|intrusive_ptr<AllTypesChildren>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(*value == *deserialized_value);
}

inline void test_148_xml()
{
    std::map<AllTypesChildren, std::vector<int>> object1;
    std::map<AllTypesChildren, std::vector<int>> object2;
    
    auto key = AllTypesChildren();
    auto value = std::vector<int>{1, 2, 3, 4};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<AllTypesChildren|std::vector<int>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_149_json()
{
    std::map<AllTypesChildren, std::vector<int>> object1;
    std::map<AllTypesChildren, std::vector<int>> object2;
    
    auto key = AllTypesChildren();
    auto value = std::vector<int>{1, 2, 3, 4};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<AllTypesChildren|std::vector<int>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_150_xml()
{
    std::map<AllTypesChildren, std::vector<std::vector<bool>>> object1;
    std::map<AllTypesChildren, std::vector<std::vector<bool>>> object2;
    
    auto key = AllTypesChildren();
    auto value = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<AllTypesChildren|std::vector<std::vector<bool>>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_151_json()
{
    std::map<AllTypesChildren, std::vector<std::vector<bool>>> object1;
    std::map<AllTypesChildren, std::vector<std::vector<bool>>> object2;
    
    auto key = AllTypesChildren();
    auto value = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<AllTypesChildren|std::vector<std::vector<bool>>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_152_xml()
{
    std::map<AllTypesChildren, std::map<int, int>> object1;
    std::map<AllTypesChildren, std::map<int, int>> object2;
    
    auto key = AllTypesChildren();
    auto value = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<AllTypesChildren|std::map<int, int>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_153_json()
{
    std::map<AllTypesChildren, std::map<int, int>> object1;
    std::map<AllTypesChildren, std::map<int, int>> object2;
    
    auto key = AllTypesChildren();
    auto value = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<AllTypesChildren|std::map<int, int>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_154_xml()
{
    std::map<intrusive_ptr<AllTypesChildren>, int> object1;
    std::map<intrusive_ptr<AllTypesChildren>, int> object2;
    
    auto key = make_intrusive<AllTypesChildren>();
    auto value = 123;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<intrusive_ptr<AllTypesChildren>|int>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(value == deserialized_value);
}

inline void test_155_json()
{
    std::map<intrusive_ptr<AllTypesChildren>, int> object1;
    std::map<intrusive_ptr<AllTypesChildren>, int> object2;
    
    auto key = make_intrusive<AllTypesChildren>();
    auto value = 123;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<intrusive_ptr<AllTypesChildren>|int>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(value == deserialized_value);
}

inline void test_156_xml()
{
    std::map<intrusive_ptr<AllTypesChildren>, bool> object1;
    std::map<intrusive_ptr<AllTypesChildren>, bool> object2;
    
    auto key = make_intrusive<AllTypesChildren>();
    auto value = true;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<intrusive_ptr<AllTypesChildren>|bool>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(value == deserialized_value);
}

inline void test_157_json()
{
    std::map<intrusive_ptr<AllTypesChildren>, bool> object1;
    std::map<intrusive_ptr<AllTypesChildren>, bool> object2;
    
    auto key = make_intrusive<AllTypesChildren>();
    auto value = true;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<intrusive_ptr<AllTypesChildren>|bool>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(value == deserialized_value);
}

inline void test_158_xml()
{
    std::map<intrusive_ptr<AllTypesChildren>, float> object1;
    std::map<intrusive_ptr<AllTypesChildren>, float> object2;
    
    auto key = make_intrusive<AllTypesChildren>();
    auto value = 123.5f;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<intrusive_ptr<AllTypesChildren>|float>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(value == deserialized_value);
}

inline void test_159_json()
{
    std::map<intrusive_ptr<AllTypesChildren>, float> object1;
    std::map<intrusive_ptr<AllTypesChildren>, float> object2;
    
    auto key = make_intrusive<AllTypesChildren>();
    auto value = 123.5f;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<intrusive_ptr<AllTypesChildren>|float>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(value == deserialized_value);
}

inline void test_160_xml()
{
    std::map<intrusive_ptr<AllTypesChildren>, std::string> object1;
    std::map<intrusive_ptr<AllTypesChildren>, std::string> object2;
    
    auto key = make_intrusive<AllTypesChildren>();
    auto value = "434312some_random";
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<intrusive_ptr<AllTypesChildren>|std::string>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(value == deserialized_value);
}

inline void test_161_json()
{
    std::map<intrusive_ptr<AllTypesChildren>, std::string> object1;
    std::map<intrusive_ptr<AllTypesChildren>, std::string> object2;
    
    auto key = make_intrusive<AllTypesChildren>();
    auto value = "434312some_random";
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<intrusive_ptr<AllTypesChildren>|std::string>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(value == deserialized_value);
}

inline void test_162_xml()
{
    std::map<intrusive_ptr<AllTypesChildren>, TestEnum> object1;
    std::map<intrusive_ptr<AllTypesChildren>, TestEnum> object2;
    
    auto key = make_intrusive<AllTypesChildren>();
    auto value = TestEnum::value2;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<intrusive_ptr<AllTypesChildren>|TestEnum>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(value == deserialized_value);
}

inline void test_163_json()
{
    std::map<intrusive_ptr<AllTypesChildren>, TestEnum> object1;
    std::map<intrusive_ptr<AllTypesChildren>, TestEnum> object2;
    
    auto key = make_intrusive<AllTypesChildren>();
    auto value = TestEnum::value2;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<intrusive_ptr<AllTypesChildren>|TestEnum>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(value == deserialized_value);
}

inline void test_164_xml()
{
    std::map<intrusive_ptr<AllTypesChildren>, const DataUnit*> object1;
    std::map<intrusive_ptr<AllTypesChildren>, const DataUnit*> object2;
    
    auto key = make_intrusive<AllTypesChildren>();
    auto value = DataStorage::shared().get<DataUnit>("unit1");
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<intrusive_ptr<AllTypesChildren>|const DataUnit*>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(value == deserialized_value);
}

inline void test_165_json()
{
    std::map<intrusive_ptr<AllTypesChildren>, const DataUnit*> object1;
    std::map<intrusive_ptr<AllTypesChildren>, const DataUnit*> object2;
    
    auto key = make_intrusive<AllTypesChildren>();
    auto value = DataStorage::shared().get<DataUnit>("unit1");
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<intrusive_ptr<AllTypesChildren>|const DataUnit*>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(value == deserialized_value);
}

inline void test_166_xml()
{
    std::map<intrusive_ptr<AllTypesChildren>, AllTypesChildren> object1;
    std::map<intrusive_ptr<AllTypesChildren>, AllTypesChildren> object2;
    
    auto key = make_intrusive<AllTypesChildren>();
    auto value = AllTypesChildren();
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<intrusive_ptr<AllTypesChildren>|AllTypesChildren>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(value == deserialized_value);
}

inline void test_167_json()
{
    std::map<intrusive_ptr<AllTypesChildren>, AllTypesChildren> object1;
    std::map<intrusive_ptr<AllTypesChildren>, AllTypesChildren> object2;
    
    auto key = make_intrusive<AllTypesChildren>();
    auto value = AllTypesChildren();
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<intrusive_ptr<AllTypesChildren>|AllTypesChildren>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(value == deserialized_value);
}

inline void test_168_xml()
{
    std::map<intrusive_ptr<AllTypesChildren>, intrusive_ptr<AllTypesChildren>> object1;
    std::map<intrusive_ptr<AllTypesChildren>, intrusive_ptr<AllTypesChildren>> object2;
    
    auto key = make_intrusive<AllTypesChildren>();
    auto value = make_intrusive<AllTypesChildren>();
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<intrusive_ptr<AllTypesChildren>|intrusive_ptr<AllTypesChildren>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(*value == *deserialized_value);
}

inline void test_169_json()
{
    std::map<intrusive_ptr<AllTypesChildren>, intrusive_ptr<AllTypesChildren>> object1;
    std::map<intrusive_ptr<AllTypesChildren>, intrusive_ptr<AllTypesChildren>> object2;
    
    auto key = make_intrusive<AllTypesChildren>();
    auto value = make_intrusive<AllTypesChildren>();
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<intrusive_ptr<AllTypesChildren>|intrusive_ptr<AllTypesChildren>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(*value == *deserialized_value);
}

inline void test_170_xml()
{
    std::map<intrusive_ptr<AllTypesChildren>, std::vector<int>> object1;
    std::map<intrusive_ptr<AllTypesChildren>, std::vector<int>> object2;
    
    auto key = make_intrusive<AllTypesChildren>();
    auto value = std::vector<int>{1, 2, 3, 4};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<intrusive_ptr<AllTypesChildren>|std::vector<int>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(value == deserialized_value);
}

inline void test_171_json()
{
    std::map<intrusive_ptr<AllTypesChildren>, std::vector<int>> object1;
    std::map<intrusive_ptr<AllTypesChildren>, std::vector<int>> object2;
    
    auto key = make_intrusive<AllTypesChildren>();
    auto value = std::vector<int>{1, 2, 3, 4};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<intrusive_ptr<AllTypesChildren>|std::vector<int>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(value == deserialized_value);
}

inline void test_172_xml()
{
    std::map<intrusive_ptr<AllTypesChildren>, std::vector<std::vector<bool>>> object1;
    std::map<intrusive_ptr<AllTypesChildren>, std::vector<std::vector<bool>>> object2;
    
    auto key = make_intrusive<AllTypesChildren>();
    auto value = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<intrusive_ptr<AllTypesChildren>|std::vector<std::vector<bool>>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(value == deserialized_value);
}

inline void test_173_json()
{
    std::map<intrusive_ptr<AllTypesChildren>, std::vector<std::vector<bool>>> object1;
    std::map<intrusive_ptr<AllTypesChildren>, std::vector<std::vector<bool>>> object2;
    
    auto key = make_intrusive<AllTypesChildren>();
    auto value = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<intrusive_ptr<AllTypesChildren>|std::vector<std::vector<bool>>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(value == deserialized_value);
}

inline void test_174_xml()
{
    std::map<intrusive_ptr<AllTypesChildren>, std::map<int, int>> object1;
    std::map<intrusive_ptr<AllTypesChildren>, std::map<int, int>> object2;
    
    auto key = make_intrusive<AllTypesChildren>();
    auto value = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<intrusive_ptr<AllTypesChildren>|std::map<int, int>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(value == deserialized_value);
}

inline void test_175_json()
{
    std::map<intrusive_ptr<AllTypesChildren>, std::map<int, int>> object1;
    std::map<intrusive_ptr<AllTypesChildren>, std::map<int, int>> object2;
    
    auto key = make_intrusive<AllTypesChildren>();
    auto value = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<intrusive_ptr<AllTypesChildren>|std::map<int, int>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(value == deserialized_value);
}

inline void test_176_xml()
{
    std::map<std::vector<int>, int> object1;
    std::map<std::vector<int>, int> object2;
    
    auto key = std::vector<int>{1, 2, 3, 4};
    auto value = 123;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<int>|int>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_177_json()
{
    std::map<std::vector<int>, int> object1;
    std::map<std::vector<int>, int> object2;
    
    auto key = std::vector<int>{1, 2, 3, 4};
    auto value = 123;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<int>|int>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_178_xml()
{
    std::map<std::vector<int>, bool> object1;
    std::map<std::vector<int>, bool> object2;
    
    auto key = std::vector<int>{1, 2, 3, 4};
    auto value = true;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<int>|bool>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_179_json()
{
    std::map<std::vector<int>, bool> object1;
    std::map<std::vector<int>, bool> object2;
    
    auto key = std::vector<int>{1, 2, 3, 4};
    auto value = true;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<int>|bool>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_180_xml()
{
    std::map<std::vector<int>, float> object1;
    std::map<std::vector<int>, float> object2;
    
    auto key = std::vector<int>{1, 2, 3, 4};
    auto value = 123.5f;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<int>|float>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_181_json()
{
    std::map<std::vector<int>, float> object1;
    std::map<std::vector<int>, float> object2;
    
    auto key = std::vector<int>{1, 2, 3, 4};
    auto value = 123.5f;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<int>|float>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_182_xml()
{
    std::map<std::vector<int>, std::string> object1;
    std::map<std::vector<int>, std::string> object2;
    
    auto key = std::vector<int>{1, 2, 3, 4};
    auto value = "434312some_random";
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<int>|std::string>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_183_json()
{
    std::map<std::vector<int>, std::string> object1;
    std::map<std::vector<int>, std::string> object2;
    
    auto key = std::vector<int>{1, 2, 3, 4};
    auto value = "434312some_random";
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<int>|std::string>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_184_xml()
{
    std::map<std::vector<int>, TestEnum> object1;
    std::map<std::vector<int>, TestEnum> object2;
    
    auto key = std::vector<int>{1, 2, 3, 4};
    auto value = TestEnum::value2;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<int>|TestEnum>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_185_json()
{
    std::map<std::vector<int>, TestEnum> object1;
    std::map<std::vector<int>, TestEnum> object2;
    
    auto key = std::vector<int>{1, 2, 3, 4};
    auto value = TestEnum::value2;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<int>|TestEnum>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_186_xml()
{
    std::map<std::vector<int>, const DataUnit*> object1;
    std::map<std::vector<int>, const DataUnit*> object2;
    
    auto key = std::vector<int>{1, 2, 3, 4};
    auto value = DataStorage::shared().get<DataUnit>("unit1");
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<int>|const DataUnit*>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_187_json()
{
    std::map<std::vector<int>, const DataUnit*> object1;
    std::map<std::vector<int>, const DataUnit*> object2;
    
    auto key = std::vector<int>{1, 2, 3, 4};
    auto value = DataStorage::shared().get<DataUnit>("unit1");
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<int>|const DataUnit*>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_188_xml()
{
    std::map<std::vector<int>, AllTypesChildren> object1;
    std::map<std::vector<int>, AllTypesChildren> object2;
    
    auto key = std::vector<int>{1, 2, 3, 4};
    auto value = AllTypesChildren();
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<int>|AllTypesChildren>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_189_json()
{
    std::map<std::vector<int>, AllTypesChildren> object1;
    std::map<std::vector<int>, AllTypesChildren> object2;
    
    auto key = std::vector<int>{1, 2, 3, 4};
    auto value = AllTypesChildren();
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<int>|AllTypesChildren>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_190_xml()
{
    std::map<std::vector<int>, intrusive_ptr<AllTypesChildren>> object1;
    std::map<std::vector<int>, intrusive_ptr<AllTypesChildren>> object2;
    
    auto key = std::vector<int>{1, 2, 3, 4};
    auto value = make_intrusive<AllTypesChildren>();
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<int>|intrusive_ptr<AllTypesChildren>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(*value == *deserialized_value);
}

inline void test_191_json()
{
    std::map<std::vector<int>, intrusive_ptr<AllTypesChildren>> object1;
    std::map<std::vector<int>, intrusive_ptr<AllTypesChildren>> object2;
    
    auto key = std::vector<int>{1, 2, 3, 4};
    auto value = make_intrusive<AllTypesChildren>();
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<int>|intrusive_ptr<AllTypesChildren>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(*value == *deserialized_value);
}

inline void test_192_xml()
{
    std::map<std::vector<int>, std::vector<int>> object1;
    std::map<std::vector<int>, std::vector<int>> object2;
    
    auto key = std::vector<int>{1, 2, 3, 4};
    auto value = std::vector<int>{1, 2, 3, 4};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<int>|std::vector<int>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_193_json()
{
    std::map<std::vector<int>, std::vector<int>> object1;
    std::map<std::vector<int>, std::vector<int>> object2;
    
    auto key = std::vector<int>{1, 2, 3, 4};
    auto value = std::vector<int>{1, 2, 3, 4};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<int>|std::vector<int>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_194_xml()
{
    std::map<std::vector<int>, std::vector<std::vector<bool>>> object1;
    std::map<std::vector<int>, std::vector<std::vector<bool>>> object2;
    
    auto key = std::vector<int>{1, 2, 3, 4};
    auto value = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<int>|std::vector<std::vector<bool>>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_195_json()
{
    std::map<std::vector<int>, std::vector<std::vector<bool>>> object1;
    std::map<std::vector<int>, std::vector<std::vector<bool>>> object2;
    
    auto key = std::vector<int>{1, 2, 3, 4};
    auto value = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<int>|std::vector<std::vector<bool>>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_196_xml()
{
    std::map<std::vector<int>, std::map<int, int>> object1;
    std::map<std::vector<int>, std::map<int, int>> object2;
    
    auto key = std::vector<int>{1, 2, 3, 4};
    auto value = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<int>|std::map<int, int>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_197_json()
{
    std::map<std::vector<int>, std::map<int, int>> object1;
    std::map<std::vector<int>, std::map<int, int>> object2;
    
    auto key = std::vector<int>{1, 2, 3, 4};
    auto value = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<int>|std::map<int, int>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_198_xml()
{
    std::map<std::vector<std::vector<bool>>, int> object1;
    std::map<std::vector<std::vector<bool>>, int> object2;
    
    auto key = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    auto value = 123;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<std::vector<bool>>|int>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_199_json()
{
    std::map<std::vector<std::vector<bool>>, int> object1;
    std::map<std::vector<std::vector<bool>>, int> object2;
    
    auto key = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    auto value = 123;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<std::vector<bool>>|int>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_200_xml()
{
    std::map<std::vector<std::vector<bool>>, bool> object1;
    std::map<std::vector<std::vector<bool>>, bool> object2;
    
    auto key = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    auto value = true;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<std::vector<bool>>|bool>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_201_json()
{
    std::map<std::vector<std::vector<bool>>, bool> object1;
    std::map<std::vector<std::vector<bool>>, bool> object2;
    
    auto key = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    auto value = true;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<std::vector<bool>>|bool>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_202_xml()
{
    std::map<std::vector<std::vector<bool>>, float> object1;
    std::map<std::vector<std::vector<bool>>, float> object2;
    
    auto key = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    auto value = 123.5f;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<std::vector<bool>>|float>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_203_json()
{
    std::map<std::vector<std::vector<bool>>, float> object1;
    std::map<std::vector<std::vector<bool>>, float> object2;
    
    auto key = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    auto value = 123.5f;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<std::vector<bool>>|float>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_204_xml()
{
    std::map<std::vector<std::vector<bool>>, std::string> object1;
    std::map<std::vector<std::vector<bool>>, std::string> object2;
    
    auto key = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    auto value = "434312some_random";
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<std::vector<bool>>|std::string>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_205_json()
{
    std::map<std::vector<std::vector<bool>>, std::string> object1;
    std::map<std::vector<std::vector<bool>>, std::string> object2;
    
    auto key = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    auto value = "434312some_random";
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<std::vector<bool>>|std::string>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_206_xml()
{
    std::map<std::vector<std::vector<bool>>, TestEnum> object1;
    std::map<std::vector<std::vector<bool>>, TestEnum> object2;
    
    auto key = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    auto value = TestEnum::value2;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<std::vector<bool>>|TestEnum>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_207_json()
{
    std::map<std::vector<std::vector<bool>>, TestEnum> object1;
    std::map<std::vector<std::vector<bool>>, TestEnum> object2;
    
    auto key = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    auto value = TestEnum::value2;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<std::vector<bool>>|TestEnum>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_208_xml()
{
    std::map<std::vector<std::vector<bool>>, const DataUnit*> object1;
    std::map<std::vector<std::vector<bool>>, const DataUnit*> object2;
    
    auto key = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    auto value = DataStorage::shared().get<DataUnit>("unit1");
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<std::vector<bool>>|const DataUnit*>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_209_json()
{
    std::map<std::vector<std::vector<bool>>, const DataUnit*> object1;
    std::map<std::vector<std::vector<bool>>, const DataUnit*> object2;
    
    auto key = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    auto value = DataStorage::shared().get<DataUnit>("unit1");
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<std::vector<bool>>|const DataUnit*>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_210_xml()
{
    std::map<std::vector<std::vector<bool>>, AllTypesChildren> object1;
    std::map<std::vector<std::vector<bool>>, AllTypesChildren> object2;
    
    auto key = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    auto value = AllTypesChildren();
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<std::vector<bool>>|AllTypesChildren>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_211_json()
{
    std::map<std::vector<std::vector<bool>>, AllTypesChildren> object1;
    std::map<std::vector<std::vector<bool>>, AllTypesChildren> object2;
    
    auto key = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    auto value = AllTypesChildren();
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<std::vector<bool>>|AllTypesChildren>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_212_xml()
{
    std::map<std::vector<std::vector<bool>>, intrusive_ptr<AllTypesChildren>> object1;
    std::map<std::vector<std::vector<bool>>, intrusive_ptr<AllTypesChildren>> object2;
    
    auto key = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    auto value = make_intrusive<AllTypesChildren>();
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<std::vector<bool>>|intrusive_ptr<AllTypesChildren>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(*value == *deserialized_value);
}

inline void test_213_json()
{
    std::map<std::vector<std::vector<bool>>, intrusive_ptr<AllTypesChildren>> object1;
    std::map<std::vector<std::vector<bool>>, intrusive_ptr<AllTypesChildren>> object2;
    
    auto key = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    auto value = make_intrusive<AllTypesChildren>();
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<std::vector<bool>>|intrusive_ptr<AllTypesChildren>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(*value == *deserialized_value);
}

inline void test_214_xml()
{
    std::map<std::vector<std::vector<bool>>, std::vector<int>> object1;
    std::map<std::vector<std::vector<bool>>, std::vector<int>> object2;
    
    auto key = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    auto value = std::vector<int>{1, 2, 3, 4};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<std::vector<bool>>|std::vector<int>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_215_json()
{
    std::map<std::vector<std::vector<bool>>, std::vector<int>> object1;
    std::map<std::vector<std::vector<bool>>, std::vector<int>> object2;
    
    auto key = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    auto value = std::vector<int>{1, 2, 3, 4};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<std::vector<bool>>|std::vector<int>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_216_xml()
{
    std::map<std::vector<std::vector<bool>>, std::vector<std::vector<bool>>> object1;
    std::map<std::vector<std::vector<bool>>, std::vector<std::vector<bool>>> object2;
    
    auto key = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    auto value = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<std::vector<bool>>|std::vector<std::vector<bool>>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_217_json()
{
    std::map<std::vector<std::vector<bool>>, std::vector<std::vector<bool>>> object1;
    std::map<std::vector<std::vector<bool>>, std::vector<std::vector<bool>>> object2;
    
    auto key = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    auto value = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<std::vector<bool>>|std::vector<std::vector<bool>>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_218_xml()
{
    std::map<std::vector<std::vector<bool>>, std::map<int, int>> object1;
    std::map<std::vector<std::vector<bool>>, std::map<int, int>> object2;
    
    auto key = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    auto value = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<std::vector<bool>>|std::map<int, int>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_219_json()
{
    std::map<std::vector<std::vector<bool>>, std::map<int, int>> object1;
    std::map<std::vector<std::vector<bool>>, std::map<int, int>> object2;
    
    auto key = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    auto value = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::vector<std::vector<bool>>|std::map<int, int>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_220_xml()
{
    std::map<std::map<int, int>, int> object1;
    std::map<std::map<int, int>, int> object2;
    
    auto key = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    auto value = 123;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::map<int, int>|int>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_221_json()
{
    std::map<std::map<int, int>, int> object1;
    std::map<std::map<int, int>, int> object2;
    
    auto key = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    auto value = 123;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::map<int, int>|int>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_222_xml()
{
    std::map<std::map<int, int>, bool> object1;
    std::map<std::map<int, int>, bool> object2;
    
    auto key = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    auto value = true;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::map<int, int>|bool>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_223_json()
{
    std::map<std::map<int, int>, bool> object1;
    std::map<std::map<int, int>, bool> object2;
    
    auto key = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    auto value = true;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::map<int, int>|bool>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_224_xml()
{
    std::map<std::map<int, int>, float> object1;
    std::map<std::map<int, int>, float> object2;
    
    auto key = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    auto value = 123.5f;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::map<int, int>|float>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_225_json()
{
    std::map<std::map<int, int>, float> object1;
    std::map<std::map<int, int>, float> object2;
    
    auto key = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    auto value = 123.5f;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::map<int, int>|float>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_226_xml()
{
    std::map<std::map<int, int>, std::string> object1;
    std::map<std::map<int, int>, std::string> object2;
    
    auto key = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    auto value = "434312some_random";
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::map<int, int>|std::string>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_227_json()
{
    std::map<std::map<int, int>, std::string> object1;
    std::map<std::map<int, int>, std::string> object2;
    
    auto key = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    auto value = "434312some_random";
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::map<int, int>|std::string>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_228_xml()
{
    std::map<std::map<int, int>, TestEnum> object1;
    std::map<std::map<int, int>, TestEnum> object2;
    
    auto key = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    auto value = TestEnum::value2;
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::map<int, int>|TestEnum>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_229_json()
{
    std::map<std::map<int, int>, TestEnum> object1;
    std::map<std::map<int, int>, TestEnum> object2;
    
    auto key = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    auto value = TestEnum::value2;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::map<int, int>|TestEnum>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_230_xml()
{
    std::map<std::map<int, int>, const DataUnit*> object1;
    std::map<std::map<int, int>, const DataUnit*> object2;
    
    auto key = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    auto value = DataStorage::shared().get<DataUnit>("unit1");
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::map<int, int>|const DataUnit*>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_231_json()
{
    std::map<std::map<int, int>, const DataUnit*> object1;
    std::map<std::map<int, int>, const DataUnit*> object2;
    
    auto key = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    auto value = DataStorage::shared().get<DataUnit>("unit1");
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::map<int, int>|const DataUnit*>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_232_xml()
{
    std::map<std::map<int, int>, AllTypesChildren> object1;
    std::map<std::map<int, int>, AllTypesChildren> object2;
    
    auto key = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    auto value = AllTypesChildren();
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::map<int, int>|AllTypesChildren>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_233_json()
{
    std::map<std::map<int, int>, AllTypesChildren> object1;
    std::map<std::map<int, int>, AllTypesChildren> object2;
    
    auto key = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    auto value = AllTypesChildren();
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::map<int, int>|AllTypesChildren>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_234_xml()
{
    std::map<std::map<int, int>, intrusive_ptr<AllTypesChildren>> object1;
    std::map<std::map<int, int>, intrusive_ptr<AllTypesChildren>> object2;
    
    auto key = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    auto value = make_intrusive<AllTypesChildren>();
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::map<int, int>|intrusive_ptr<AllTypesChildren>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(*value == *deserialized_value);
}

inline void test_235_json()
{
    std::map<std::map<int, int>, intrusive_ptr<AllTypesChildren>> object1;
    std::map<std::map<int, int>, intrusive_ptr<AllTypesChildren>> object2;
    
    auto key = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    auto value = make_intrusive<AllTypesChildren>();
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::map<int, int>|intrusive_ptr<AllTypesChildren>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(*value == *deserialized_value);
}

inline void test_236_xml()
{
    std::map<std::map<int, int>, std::vector<int>> object1;
    std::map<std::map<int, int>, std::vector<int>> object2;
    
    auto key = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    auto value = std::vector<int>{1, 2, 3, 4};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::map<int, int>|std::vector<int>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_237_json()
{
    std::map<std::map<int, int>, std::vector<int>> object1;
    std::map<std::map<int, int>, std::vector<int>> object2;
    
    auto key = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    auto value = std::vector<int>{1, 2, 3, 4};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::map<int, int>|std::vector<int>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_238_xml()
{
    std::map<std::map<int, int>, std::vector<std::vector<bool>>> object1;
    std::map<std::map<int, int>, std::vector<std::vector<bool>>> object2;
    
    auto key = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    auto value = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::map<int, int>|std::vector<std::vector<bool>>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_239_json()
{
    std::map<std::map<int, int>, std::vector<std::vector<bool>>> object1;
    std::map<std::map<int, int>, std::vector<std::vector<bool>>> object2;
    
    auto key = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    auto value = std::vector<std::vector<bool>>{{true, false}, {false, true}};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::map<int, int>|std::vector<std::vector<bool>>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_240_xml()
{
    std::map<std::map<int, int>, std::map<int, int>> object1;
    std::map<std::map<int, int>, std::map<int, int>> object2;
    
    auto key = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    auto value = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    object1[key] = value;
    
    pugi::xml_document doc;
    pugi::xml_node node = doc.root().append_child("root");

    SerializerXml serializer(node);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::map<int, int>|std::map<int, int>>\":" << std::endl; 
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_241_json()
{
    std::map<std::map<int, int>, std::map<int, int>> object1;
    std::map<std::map<int, int>, std::map<int, int>> object2;
    
    auto key = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    auto value = std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)};
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    std::cout << std::endl << ",\"map<std::map<int, int>|std::map<int, int>>\":" << std::endl; 
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}


inline void run_generated_tests()
{
    test_0_xml();
    test_2_xml();
    test_4_xml();
    test_6_xml();
    test_8_xml();
    test_10_xml();
    test_12_xml();
    test_14_xml();
    test_16_xml();
    test_18_xml();
    test_20_xml();
    test_22_xml();
    test_24_xml();
    test_26_xml();
    test_28_xml();
    test_30_xml();
    test_32_xml();
    test_34_xml();
    test_36_xml();
    test_38_xml();
    test_40_xml();
    test_42_xml();
    test_44_xml();
    test_46_xml();
    test_48_xml();
    test_50_xml();
    test_52_xml();
    test_54_xml();
    test_56_xml();
    test_58_xml();
    test_60_xml();
    test_62_xml();
    test_64_xml();
    test_66_xml();
    test_68_xml();
    test_70_xml();
    test_72_xml();
    test_74_xml();
    test_76_xml();
    test_78_xml();
    test_80_xml();
    test_82_xml();
    test_84_xml();
    test_86_xml();
    test_88_xml();
    test_90_xml();
    test_92_xml();
    test_94_xml();
    test_96_xml();
    test_98_xml();
    test_100_xml();
    test_102_xml();
    test_104_xml();
    test_106_xml();
    test_108_xml();
    test_110_xml();
    test_112_xml();
    test_114_xml();
    test_116_xml();
    test_118_xml();
    test_120_xml();
    test_122_xml();
    test_124_xml();
    test_126_xml();
    test_128_xml();
    test_130_xml();
    test_132_xml();
    test_134_xml();
    test_136_xml();
    test_138_xml();
    test_140_xml();
    test_142_xml();
    test_144_xml();
    test_146_xml();
    test_148_xml();
    test_150_xml();
    test_152_xml();
    test_154_xml();
    test_156_xml();
    test_158_xml();
    test_160_xml();
    test_162_xml();
    test_164_xml();
    test_166_xml();
    test_168_xml();
    test_170_xml();
    test_172_xml();
    test_174_xml();
    test_176_xml();
    test_178_xml();
    test_180_xml();
    test_182_xml();
    test_184_xml();
    test_186_xml();
    test_188_xml();
    test_190_xml();
    test_192_xml();
    test_194_xml();
    test_196_xml();
    test_198_xml();
    test_200_xml();
    test_202_xml();
    test_204_xml();
    test_206_xml();
    test_208_xml();
    test_210_xml();
    test_212_xml();
    test_214_xml();
    test_216_xml();
    test_218_xml();
    test_220_xml();
    test_222_xml();
    test_224_xml();
    test_226_xml();
    test_228_xml();
    test_230_xml();
    test_232_xml();
    test_234_xml();
    test_236_xml();
    test_238_xml();
    test_240_xml();
}

#endif
