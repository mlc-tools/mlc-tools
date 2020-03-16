/*
    This is generated file by generate_tests.py script
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


inline void test_xml_0()
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
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}
inline void test_json_0()
{
    std::map<int, int> object1;
    std::map<int, int> object2;
    
    auto key = 123;
    auto value = 123;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_xml_1()
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
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}
inline void test_json_1()
{
    std::map<int, bool> object1;
    std::map<int, bool> object2;
    
    auto key = 123;
    auto value = true;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_xml_2()
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
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}
inline void test_json_2()
{
    std::map<int, float> object1;
    std::map<int, float> object2;
    
    auto key = 123;
    auto value = 123.5f;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_xml_3()
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
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}
inline void test_json_3()
{
    std::map<int, std::string> object1;
    std::map<int, std::string> object2;
    
    auto key = 123;
    auto value = "434312some_random";
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_xml_4()
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
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(*value == *deserialized_value);
}
inline void test_json_4()
{
    std::map<int, intrusive_ptr<AllTypesChildren>> object1;
    std::map<int, intrusive_ptr<AllTypesChildren>> object2;
    
    auto key = 123;
    auto value = make_intrusive<AllTypesChildren>();
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(*value == *deserialized_value);
}

inline void test_xml_5()
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
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}
inline void test_json_5()
{
    std::map<bool, int> object1;
    std::map<bool, int> object2;
    
    auto key = true;
    auto value = 123;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_xml_6()
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
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}
inline void test_json_6()
{
    std::map<bool, bool> object1;
    std::map<bool, bool> object2;
    
    auto key = true;
    auto value = true;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_xml_7()
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
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}
inline void test_json_7()
{
    std::map<bool, float> object1;
    std::map<bool, float> object2;
    
    auto key = true;
    auto value = 123.5f;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_xml_8()
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
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}
inline void test_json_8()
{
    std::map<bool, std::string> object1;
    std::map<bool, std::string> object2;
    
    auto key = true;
    auto value = "434312some_random";
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_xml_9()
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
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(*value == *deserialized_value);
}
inline void test_json_9()
{
    std::map<bool, intrusive_ptr<AllTypesChildren>> object1;
    std::map<bool, intrusive_ptr<AllTypesChildren>> object2;
    
    auto key = true;
    auto value = make_intrusive<AllTypesChildren>();
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(*value == *deserialized_value);
}

inline void test_xml_10()
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
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}
inline void test_json_10()
{
    std::map<float, int> object1;
    std::map<float, int> object2;
    
    auto key = 123.5f;
    auto value = 123;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_xml_11()
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
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}
inline void test_json_11()
{
    std::map<float, bool> object1;
    std::map<float, bool> object2;
    
    auto key = 123.5f;
    auto value = true;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_xml_12()
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
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}
inline void test_json_12()
{
    std::map<float, float> object1;
    std::map<float, float> object2;
    
    auto key = 123.5f;
    auto value = 123.5f;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_xml_13()
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
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}
inline void test_json_13()
{
    std::map<float, std::string> object1;
    std::map<float, std::string> object2;
    
    auto key = 123.5f;
    auto value = "434312some_random";
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_xml_14()
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
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(*value == *deserialized_value);
}
inline void test_json_14()
{
    std::map<float, intrusive_ptr<AllTypesChildren>> object1;
    std::map<float, intrusive_ptr<AllTypesChildren>> object2;
    
    auto key = 123.5f;
    auto value = make_intrusive<AllTypesChildren>();
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(*value == *deserialized_value);
}

inline void test_xml_15()
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
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}
inline void test_json_15()
{
    std::map<std::string, int> object1;
    std::map<std::string, int> object2;
    
    auto key = "434312some_random";
    auto value = 123;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_xml_16()
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
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}
inline void test_json_16()
{
    std::map<std::string, bool> object1;
    std::map<std::string, bool> object2;
    
    auto key = "434312some_random";
    auto value = true;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_xml_17()
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
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}
inline void test_json_17()
{
    std::map<std::string, float> object1;
    std::map<std::string, float> object2;
    
    auto key = "434312some_random";
    auto value = 123.5f;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_xml_18()
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
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}
inline void test_json_18()
{
    std::map<std::string, std::string> object1;
    std::map<std::string, std::string> object2;
    
    auto key = "434312some_random";
    auto value = "434312some_random";
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(value == deserialized_value);
}

inline void test_xml_19()
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
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(*value == *deserialized_value);
}
inline void test_json_19()
{
    std::map<std::string, intrusive_ptr<AllTypesChildren>> object1;
    std::map<std::string, intrusive_ptr<AllTypesChildren>> object2;
    
    auto key = "434312some_random";
    auto value = make_intrusive<AllTypesChildren>();
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(key == deserialized_key);
    assert(*value == *deserialized_value);
}

inline void test_xml_20()
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
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(value == deserialized_value);
}
inline void test_json_20()
{
    std::map<intrusive_ptr<AllTypesChildren>, int> object1;
    std::map<intrusive_ptr<AllTypesChildren>, int> object2;
    
    auto key = make_intrusive<AllTypesChildren>();
    auto value = 123;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(value == deserialized_value);
}

inline void test_xml_21()
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
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(value == deserialized_value);
}
inline void test_json_21()
{
    std::map<intrusive_ptr<AllTypesChildren>, bool> object1;
    std::map<intrusive_ptr<AllTypesChildren>, bool> object2;
    
    auto key = make_intrusive<AllTypesChildren>();
    auto value = true;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(value == deserialized_value);
}

inline void test_xml_22()
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
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(value == deserialized_value);
}
inline void test_json_22()
{
    std::map<intrusive_ptr<AllTypesChildren>, float> object1;
    std::map<intrusive_ptr<AllTypesChildren>, float> object2;
    
    auto key = make_intrusive<AllTypesChildren>();
    auto value = 123.5f;
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(value == deserialized_value);
}

inline void test_xml_23()
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
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(value == deserialized_value);
}
inline void test_json_23()
{
    std::map<intrusive_ptr<AllTypesChildren>, std::string> object1;
    std::map<intrusive_ptr<AllTypesChildren>, std::string> object2;
    
    auto key = make_intrusive<AllTypesChildren>();
    auto value = "434312some_random";
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(value == deserialized_value);
}

inline void test_xml_24()
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
    log(doc);

    DeserializerXml deserializer(node);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(*value == *deserialized_value);
}
inline void test_json_24()
{
    std::map<intrusive_ptr<AllTypesChildren>, intrusive_ptr<AllTypesChildren>> object1;
    std::map<intrusive_ptr<AllTypesChildren>, intrusive_ptr<AllTypesChildren>> object2;
    
    auto key = make_intrusive<AllTypesChildren>();
    auto value = make_intrusive<AllTypesChildren>();
    object1[key] = value;
    
    Json::Value json;

    SerializerJson serializer(json);
    serializer.serialize(object1, "object");
    log(json);

    DeserializerJson deserializer(json);
    deserializer.deserialize(object2, "object");
    
    assert(object1.size() == object2.size() && object2.size() == 1);
    
    auto& deserialized_key = object2.begin()->first; 
    auto& deserialized_value = object2.begin()->second; 
    assert(*key == *deserialized_key);
    assert(*value == *deserialized_value);
}


inline void run_generated_tests()
{
    test_xml_0();
    test_json_0();
    test_xml_1();
    test_json_1();
    test_xml_2();
    test_json_2();
    test_xml_3();
    test_json_3();
    test_xml_4();
    test_json_4();
    test_xml_5();
    test_json_5();
    test_xml_6();
    test_json_6();
    test_xml_7();
    test_json_7();
    test_xml_8();
    test_json_8();
    test_xml_9();
    test_json_9();
    test_xml_10();
    test_json_10();
    test_xml_11();
    test_json_11();
    test_xml_12();
    test_json_12();
    test_xml_13();
    test_json_13();
    test_xml_14();
    test_json_14();
    test_xml_15();
    test_json_15();
    test_xml_16();
    test_json_16();
    test_xml_17();
    test_json_17();
    test_xml_18();
    test_json_18();
    test_xml_19();
    test_json_19();
    test_xml_20();
    test_json_20();
    test_xml_21();
    test_json_21();
    test_xml_22();
    test_json_22();
    test_xml_23();
    test_json_23();
    test_xml_24();
    test_json_24();
}

#endif
