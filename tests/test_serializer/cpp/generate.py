

types = {
    'int': '123',
    'bool': 'true',
    'float': '123.5f',
    'std::string': '"434312some_random"',
    'TestEnum': 'TestEnum::value2',
    'const DataUnit*': 'DataStorage::shared().get<DataUnit>("unit1")',
    'AllTypesChildren': 'AllTypesChildren()',
    'intrusive_ptr<AllTypesChildren>': 'make_intrusive<AllTypesChildren>()',
    'std::vector<int>': 'std::vector<int>{1, 2, 3, 4}',
    'std::vector<std::vector<bool>>': 'std::vector<std::vector<bool>>{{true, false}, {false, true}}',
    'std::map<int, int>': 'std::map<int, int>{std::make_pair(1, 2), std::make_pair(2, 3)}',
}

comparators = {
    'intrusive_ptr<AllTypesChildren>': '*{0} == *deserialized_{0}'
}

test = '''
inline void test_{index1}_xml()
{{
    std::map<{type1}, {type2}> object1;
    std::map<{type1}, {type2}> object2;
    
    auto key = {initialize1};
    auto value = {initialize2};
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
    assert({compare_key});
    assert({compare_value});
}}

inline void test_{index2}_json()
{{
    std::map<{type1}, {type2}> object1;
    std::map<{type1}, {type2}> object2;
    
    auto key = {initialize1};
    auto value = {initialize2};
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
    assert({compare_key});
    assert({compare_value});
}}
'''

tests = ''
runner = ''
keys = types.keys()
index = 0
for item1 in keys:
    for item2 in keys:
        compare_key = comparators[item1].format('key') if item1 in comparators else 'key == deserialized_key'
        compare_value = comparators[item2].format('value') if item2 in comparators else 'value == deserialized_value'
        tests += test.format(index1=index, index2=index+1,
                             type1=item1, type2=item2,
                             initialize1=types[item1], initialize2=types[item2],
                             compare_key=compare_key, compare_value=compare_value)
        runner += '\n    test_{index}_xml();'.format(index=index)
        runner += '\n    test_{index}_json();'.format(index=index+1)
        index += 2

tests = '''/*
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
{{
    std::stringstream stream;
    pugi::xml_writer_stream writer(stream);
    document.save(writer, " ", pugi::format_no_declaration | pugi::format_indent, pugi::xml_encoding::encoding_auto);

    return stream.str();
}}
inline void log(const pugi::xml_document &document)
{{
    std::cout << "XML:" << std::endl << toStr(document) << std::endl;
}}
inline std::string toStr(const Json::Value &json)
{{
    Json::StreamWriterBuilder wbuilder;
    wbuilder["indentation"] = " ";
    return Json::writeString(wbuilder, json);
}}
inline void log(const Json::Value &json)
{{
    std::cout << "JSON:" << std::endl << toStr(json) << std::endl;
}}

{tests}

inline void run_generated_tests()
{{{runner}
}}

#endif
'''.format(tests=tests, runner=runner)
open('tests.h', 'w').write(tests)

# Generate Serialize methods

types = [
    'is_attribute',
    'is_enum',
    'is_data',
    'is_not_serialize_to_attribute',
    # 'is_intrusive',
    # 'is_container',
]

# XML

xml_key_serialize = {
    'is_attribute': 'item.add_attribute("key", pair.first, default_value::value<Key>());',
    'is_enum': 'item.add_attribute("key", pair.first.str(), default_value::value<std::string>());',
    'is_data': 'item.add_attribute("key", pair.first->name, default_value::value<std::string>());',
    'is_not_serialize_to_attribute': 'item.serialize(pair.first, "key");',
}
xml_value_serialize = {
    'is_attribute': 'item.add_attribute("value", pair.second, default_value::value<Value>());',
    'is_enum': 'item.add_attribute("value", pair.second.str(), default_value::value<std::string>());',
    'is_data': 'item.add_attribute("value", pair.second->name, default_value::value<std::string>());',
    'is_not_serialize_to_attribute': 'item.serialize(pair.second, "value");',
}
xml_key_deserialize = {
    'is_attribute': 'Key key_ = item.get_attribute("key", default_value::value<Key>());',
    'is_enum': 'Key key_; item.deserialize(key_, "key");',
    'is_data': 'Key key_ = DataStorage::shared().get<typename data_type<Key>::type>(item.get_attribute("key", default_value::value<std::string>()));',
    'is_not_serialize_to_attribute': 'Key key_; item.deserialize(key_, "key");',
}
xml_value_deserialize = {
    'is_attribute': 'Value value_ = item.get_attribute("value", default_value::value<Value>());',
    'is_enum': 'Value value_; item.deserialize(value_, "value");',
    'is_data': 'Value value_ = DataStorage::shared().get<typename data_type<Value>::type>(item.get_attribute("value", default_value::value<std::string>()));',
    'is_not_serialize_to_attribute': 'Value value_; item.deserialize(value_, "value");',
}

# JSON

json_key_serialize = {
    'is_attribute': 'item.add_attribute("key", pair.first, default_value::value<Key>());',
    'is_enum': 'item.add_attribute("key", pair.first.str(), default_value::value<std::string>());',
    'is_data': 'item.add_attribute("key", pair.first->name, default_value::value<std::string>());',
    'is_not_serialize_to_attribute': 'SerializerJson pair_key = item.add_child("key"); pair_key.serialize(pair.first);',
}
json_value_serialize = {
    'is_attribute': 'item.add_attribute("value", pair.second, default_value::value<Value>());',
    'is_enum': 'item.add_attribute("value", pair.second.str(), default_value::value<std::string>());',
    'is_data': 'item.add_attribute("value", pair.second->name, default_value::value<std::string>());',
    'is_not_serialize_to_attribute': 'SerializerJson pair_value = item.add_child("value"); pair_value.serialize(pair.second);',
}
json_key_deserialize = {
    'is_attribute': 'Key key_ = item.get_attribute("key", default_value::value<Key>());',
    'is_enum': 'Key key_(item.get_attribute("key", default_value::value<Key>());',
    'is_data': 'Key key_ = DataStorage::shared().get<typename data_type<Key>::type>(item.get_attribute("key", default_value::value<std::string>()));',
    'is_not_serialize_to_attribute': 'Key key_; item.deserialize(key_, "key");',
}
json_value_deserialize = {
    'is_attribute': 'Value value_ = item.get_attribute("value", default_value::value<Value>());',
    'is_enum': 'Value value_(item.get_attribute("value", default_value::value<Value>());',
    'is_data': 'Value value_ = DataStorage::shared().get<typename data_type<Value>::type>(item.get_attribute("value", default_value::value<std::string>()));',
    'is_not_serialize_to_attribute': 'Value value_; item.deserialize(value_, "value");',
}

xml_map_serialize = ''
xml_map_deserialize = ''
json_map_serialize = ''
json_map_deserialize = ''
for type1 in types:
    for type2 in types:

        key = xml_key_serialize[type1]
        value = xml_value_serialize[type2]
        body_xml_serialize = '''
    template <class Key, class Value>
    typename std::enable_if<{type1}<Key>::value && {type2}<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {{
        if (values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {{
            SerializerXml item = child.add_child("pair");
            {key}
            {value}            
        }}
    }}\n'''.format(type1=type1, type2=type2, key=key, value=value)

        key = xml_key_deserialize[type1]
        value = xml_value_deserialize[type2]
        body_xml_deserialize = '''
    template <class Key, class Value>
    typename std::enable_if<{type1}<Key>::value && {type2}<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {{
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for (DeserializerXml item : child)
        {{
            {key}
            {value}
            map[key_] = value_;            
        }}
    }}\n'''.format(type1=type1, type2=type2, key=key, value=value)
        xml_map_serialize += body_xml_serialize
        xml_map_deserialize += body_xml_deserialize

        key = xml_key_serialize[type1]
        value = xml_value_serialize[type2]
        body_json_serialize = '''
    template <class Key, class Value>
    typename std::enable_if<{type1}<Key>::value && {type2}<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {{
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_array(key);
        for (auto& pair : values)
        {{
            SerializerJson item = child.add_array_item();
            {key}
            {value}            
        }}
    }}\n'''.format(type1=type1, type2=type2, key=key, value=value)

        key = xml_key_deserialize[type1]
        value = xml_value_deserialize[type2]
        body_json_deserialize = '''
    template <class Key, class Value>
    typename std::enable_if<{type1}<Key>::value && {type2}<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {{
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {{
            {key}
            {value}
            map[key_] = value_;            
        }}
    }}\n'''.format(type1=type1, type2=type2, key=key, value=value)

        json_map_serialize += body_json_serialize
        json_map_deserialize += body_json_deserialize


def replace(source, new_content, block):
    start = source.find('/* {} start */'.format(block))
    start = source.find('\n', start)
    finish = source.find('/* {} finish */'.format(block))
    source = source[:start] + new_content + source[finish:]
    return source


content = open('src/serialize/SerializerXml.h').read()
content = replace(content, xml_map_serialize, 'Maps serialization')
content = replace(content, xml_map_deserialize, 'Maps deserialization')
open('src/serialize/SerializerXml.h', 'w').write(content)

content = open('src/serialize/SerializerJson.h').read()
content = replace(content, json_map_serialize, 'Maps serialization')
content = replace(content, json_map_deserialize, 'Maps deserialization')
open('src/serialize/SerializerJson.h', 'w').write(content)

# Save serializers to mlc_tools
content = open('../../../mlc_tools/module_cpp/cpp_extension.py').read()

data = open('src/serialize/SerializerXml.h').read()
start = content.find("'''", content.find('SERIALIZER_XML_HPP')) + 3
finish = content.find("'''", start)
content = content[:start] + data + content[finish:]

data = open('src/serialize/SerializerXml.cpp').read()
start = content.find("'''", content.find('SERIALIZER_XML_CPP')) + 3
finish = content.find("'''", start)
content = content[:start] + data + content[finish:]

data = open('src/serialize/SerializerJson.h').read()
start = content.find("'''", content.find('SERIALIZER_JSON_HPP')) + 3
finish = content.find("'''", start)
content = content[:start] + data + content[finish:]

data = open('src/serialize/SerializerJson.cpp').read()
start = content.find("'''", content.find('SERIALIZER_JSON_CPP')) + 3
finish = content.find("'''", start)
content = content[:start] + data + content[finish:]

data = open('src/serialize/SerializerCommon.h').read()
start = content.find("'''", content.find('SERIALIZER_COMMON')) + 3
finish = content.find("'''", start)
content = content[:start] + data + content[finish:]

open('../../../mlc_tools/module_cpp/cpp_extension.py', 'w').write(content)
