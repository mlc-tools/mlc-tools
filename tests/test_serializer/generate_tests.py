

types = {
    'int': '123',
    'bool': 'true',
    'float': '123.5f',
    'std::string': '"434312some_random"',
    # 'TestEnum': 'TestEnum::value2',
    # 'const DataUnit*': 'DataStorage::shared().get<DataUnit>("unit1")',
    # 'AllTypesChildren': 'AllTypesChildren()',
    'intrusive_ptr<AllTypesChildren>': 'make_intrusive<AllTypesChildren>()',
}

comparators = {
    'intrusive_ptr<AllTypesChildren>': '*{0} == *deserialized_{0}'
}

test = '''
inline void test_xml_{index}()
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
inline void test_json_{index}()
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
        tests += test.format(index=index, type1=item1, type2=item2, initialize1=types[item1], initialize2=types[item2],
                             compare_key=compare_key, compare_value=compare_value)
        runner += '\n    test_xml_{index}();'.format(index=index)
        runner += '\n    test_json_{index}();'.format(index=index)
        index += 1

tests = '''/*
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
