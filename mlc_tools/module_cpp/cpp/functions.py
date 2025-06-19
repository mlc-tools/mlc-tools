FUNCTIONS_HPP = '''
#ifndef __@{namespace}_functions_h__
#define __@{namespace}_functions_h__

#include <map>
#include <vector>
#include <cmath>
#include <string>
#include <algorithm>
#include "config.h"
#include <assert.h>
#include <cstdarg>

#include "pugixml/pugixml.hpp"
#include "jsoncpp/json.h"
#include "@{namespace}_Factory.h"
#include "SerializerXml.h"
#include "SerializerJson.h"
#include "SerializerBinary.h"

namespace @{namespace}
{

    template <class K, class T, class P>
    bool in_map(const K& element, const std::map<T, P>& map)
    {
        return map.count(element) > 0;
    }

    template <class I, class T>
    bool in_list(I item, const std::vector<T>& list)
    {
        return std::find(list.begin(), list.end(), item) != list.end();
    }

    template <class T, class I>
    void list_push(std::vector<T>& list, const I& t)
    {
        list.push_back(t);
    }

    template <class T, class I>
    void list_insert(std::vector<T>& list, size_t index, const I& t)
    {
        assert(index <= list.size());
        list.insert(list.begin() + index, t);
    }

    template <class T, class I>
    void list_remove(std::vector<T>& list, const I& t)
    {
        auto iter = std::find(list.begin(), list.end(), t);
        if(iter != list.end())
            list.erase(iter);
    }

    template <class T>
    void list_erase(std::vector<T>& list, size_t index)
    {
        assert(index < list.size());
        list.erase(list.begin() + index);
    }

    template <class T>
    void list_truncate(std::vector<T>& list, size_t length)
    {
        assert(length < list.size());
        list.erase(list.begin() + length, list.end());
    }

    template <class T>
    int list_size(const std::vector<T>& vector)
    {
        return static_cast<int>(vector.size());
    }
    
    template <class T>
    int list_index(const std::vector<T>& list, const T& t)
    {
        auto iter = std::find(list.begin(), list.end(), t);
        if(iter != list.end())
            return iter - list.begin();
        return -1;
    }

    template <class T>
    void list_clear(std::vector<T>& vector)
    {
        vector.clear();
    }

    template <class T>
    void list_resize(std::vector<T>& vector, int size)
    {
        vector.resize(size);
    }

    template <class T, class P>
    int map_size(const std::map<T, P>& map)
    {
        return static_cast<int>(map.size());
    }
    template <class T, class P>
    void map_clear(std::map<T, P>& map)
    {
        map.clear();
    }
    template <class T, class P>
    void map_remove(std::map<T, P>& map, const T& key)
    {
        auto iter = map.find(key);
        if(iter != map.end())
        {
            map.erase(iter);
        }
    }

    bool string_empty(const std::string& string);
    int string_size(const std::string& string);

    float random_float();
    int random_int(int min, int max);

    template <class T>
    void mg_swap(T& a, T& b)
    {
        std::swap(a, b);
    }
    
    std::vector<std::string> split(const std::string& string, const char delimiter);
    std::string join(const std::vector<std::string>& values, const char delimiter);

    // Converters
    template <typename T> T strTo(const std::string &value);
    template <typename T> std::string toStr(T value);

    //XML
    template <class T> void set(pugi::xml_attribute& xml, T value);
    template <class T> T get(const pugi::xml_attribute& xml);

    template <class T> void set(pugi::xml_node& xml, const std::string& key, T value)
    {
        auto attribute = xml.append_attribute(key.c_str());
        set<T>(attribute, value);
    }
    template <class T> T get(const pugi::xml_node& xml, const std::string& key)
    {
        auto attribute = xml.attribute(key.c_str());
        if(attribute)
            return get<T>(attribute);
        return 0;
    }

    //JSON
    template <class T> void set(Json::Value& json, T value);
    template <class T> T get(const Json::Value& json);

    template <class T> void set(Json::Value& json, const std::string& key, T value)
    {
        set<T>(json[key], value);
    }
    template <class T> T get(const Json::Value& json, const std::string& key)
    {
        get<T>(json[key]);
    }

    std::string format(const char *fmt, ...);

    {{format=json}}
    template <class TType>
    std::string serialize_command_to_json(const TType* command)
    {
        Json::Value json;
        SerializerJson serializer(json[command->get_type()]);
        command->serialize_json(serializer);

        Json::StreamWriterBuilder wbuilder;
        wbuilder["indentation"] = "";
        return Json::writeString(wbuilder, json);
    }

    template <class TType>
    static intrusive_ptr<TType> create_command_from_json(const std::string& payload)
    {
        Json::Value json;
        Json::Reader reader;
        if(!reader.parse(payload, json))
        {
            return nullptr;
        }
        
        if(json.getMemberNames().size() == 0)
        {
            return nullptr;
        }

        auto type = json.getMemberNames()[0];
        DeserializerJson deserializer(json[type]);
        auto command = Factory::shared().build<TType>(type);
        if(command)
        {
            command->deserialize_json(deserializer);
        }
        return command;
    }
    template <class TType>
    static intrusive_ptr<TType> clone_object(const TType* object)
    {
        auto payload = serialize_command_to_json<TType>(object);
        auto clone = create_command_from_json<TType>(payload);
        return clone;
    }
    {{end_format=json}}

    {{format=xml}}
    template <class TType>
    static std::string serialize_command_to_xml(const TType* command)
    {
        pugi::xml_document doc;
        auto root = doc.append_child(command->get_type().c_str());
        SerializerXml serializer(root);
        command->serialize_xml(serializer);

        std::stringstream stream;
        pugi::xml_writer_stream writer(stream);
#ifdef NDEBUG
        doc.save(writer,
                 "",
                 pugi::format_no_declaration | pugi::format_raw,
                 pugi::xml_encoding::encoding_utf8);
#else
        doc.save(writer,
                 PUGIXML_TEXT(" "),
                 pugi::format_no_declaration | pugi::format_indent,
                 pugi::xml_encoding::encoding_utf8);
#endif
        return stream.str();
    }

    template <class TType>
    static intrusive_ptr<TType> create_command_from_xml(const std::string& payload)
    {
        pugi::xml_document doc;
        doc.load_string(payload.c_str());
        auto root = doc.root().first_child();
        DeserializerXml deserializer(root);
        auto command = Factory::shared().build<TType>(root.name());
        if(command)
        {
            command->deserialize_xml(deserializer);
        }
        return command;
    }

    template <class TType>
    static intrusive_ptr<TType> clone_object(const TType* object)
    {
        auto payload = serialize_command_to_xml<TType>(object);
        auto clone = create_command_from_xml<TType>(payload);
        return clone;
    }
    {{end_format=xml}}

    {{format=binary}}
    template <class TType>
    static std::string serialize_command_to_binary(const TType* command)
    {
        BinaryFormat binary;
        binary.add("type", command->get_type());
        SerializerBinary serializer(binary);
        command->serialize_binary(serializer);
        return binary.get_string_data();
    }

    template <class TType>
    static intrusive_ptr<TType> create_command_from_binary(const std::string& payload)
    {
        BinaryFormat binary;
        binary.set_string_data(payload);
        DeserializerBinary deserializer(binary);
        auto command = Factory::shared().build<TType>(binary.get_string("type", ""));
        if(command)
        {
            command->deserialize_binary(deserializer);
        }
        return command;
    }

    template <class TType>
    static intrusive_ptr<TType> clone_object(const TType* object)
    {
        auto payload = serialize_command_to_binary<TType>(object);
        auto clone = create_command_from_binary<TType>(payload);
        return clone;
    }
    {{end_format=binary}}

    {{format=both}}
    template <class TType>
    static std::string serialize_command_to_xml(const TType* command)
    {
        pugi::xml_document doc;
        auto root = doc.append_child(command->get_type().c_str());
        SerializerXml serializer(root);
        command->serialize_xml(serializer);

        std::stringstream stream;
        pugi::xml_writer_stream writer(stream);
#ifdef NDEBUG
        doc.save(writer,
                 "",
                 pugi::format_no_declaration | pugi::format_raw,
                 pugi::xml_encoding::encoding_utf8);
#else
        doc.save(writer,
                 PUGIXML_TEXT(" "),
                 pugi::format_no_declaration | pugi::format_indent,
                 pugi::xml_encoding::encoding_utf8);
#endif
        return stream.str();
    }

    template <class TType>
    static intrusive_ptr<TType> create_command_from_xml(const std::string& payload)
    {
        pugi::xml_document doc;
        doc.load_string(payload.c_str());
        auto root = doc.root().first_child();
        auto command = Factory::shared().build<TType>(root.name());
        DeserializerXml deserializer(root);
        if(command)
            command->deserialize_xml(deserializer);
        return command;
    }

    template <class TType>
    static std::string serialize_command_to_json(const TType* command)
    {
        Json::Value json;
        SerializerJson serializer(json[command->get_type()]);
        command->serialize_json(serializer);

        Json::StreamWriterBuilder wbuilder;
        wbuilder["indentation"] = "";
        return Json::writeString(wbuilder, json);
    }

    template <class TType>
    static intrusive_ptr<TType> create_command_from_json(const std::string& payload)
    {
        Json::Value json;
        Json::Reader reader;
        if(!reader.parse(payload, json))
        {
            return nullptr;
        }
        
        if(json.getMemberNames().size() == 0)
        {
            return nullptr;
        }

        auto type = json.getMemberNames()[0];
        DeserializerJson deserializer(json[type]);
        auto command = Factory::shared().build<TType>(type);
        if(command)
        {
            command->deserialize_json(deserializer);
        }
        return command;
    }

    template <class TType>
    static std::string serialize_command_to_binary(const TType* command)
    {
        BinaryFormat binary;
        binary.add("type", command->get_type());
        SerializerBinary serializer(binary);
        command->serialize_binary(serializer);
        return binary.get_string_data();
    }

    template <class TType>
    static intrusive_ptr<TType> create_command_from_binary(const std::string& payload)
    {
        BinaryFormat binary;
        binary.set_string_data(payload);
        DeserializerBinary deserializer(binary);
        auto command = Factory::shared().build<TType>(binary.get_string("type", ""));
        if(command)
        {
            command->deserialize_binary(deserializer);
        }
        return command;
    }

    template <class TType>
    static intrusive_ptr<TType> clone_object(const TType* object)
    {
        auto payload = serialize_command_to_binary<TType>(object);
        auto clone = create_command_from_binary<TType>(payload);
        return clone;
    }
    
    {{end_format=both}}
    
    std::string fs_get_string(const std::string& path);
    
    template<typename T> struct Default { static constexpr T value = 0; };
    template<> struct Default<std::string> {static const std::string value;};
}

#endif
'''
FUNCTIONS_CPP = '''
#include <cstdlib>
#include <sstream>
#include <vector>
#include "@{namespace}_extensions.h"
#include <fstream>
#include <iostream>

namespace @{namespace}
{
    const std::string Default<std::string>::value;
    
    float random_float()
    {
        return std::rand() / static_cast<float>(RAND_MAX);
    }

    int random_int(int min, int max)
    {
        auto diff = max - min;
        if(diff > 0)
        {
            return std::rand() % diff + min;
        }
        return min;
    }

    bool string_empty(const std::string& string)
    {
        return string.empty();
    }

    int string_size(const std::string& string)
    {
        return static_cast<int>(string.size());
    }

    std::string boolToStr(bool value)
    {
        return value ? "yes" : "no";
    };

    std::string intToStr(int value)
    {
        std::stringstream ss;
        ss << value;
        return ss.str();
    };

    std::string floatToStr(float value)
    {
        std::stringstream ss;
        ss.precision(5);
        ss << value;
        return ss.str();
    };

    bool strToBool(const std::string& value)
    {
        if (value.empty())
            return false;
        bool result(false);
        result = result || value == "yes";
        result = result || value == "Yes";
        result = result || value == "true";
        result = result || value == "True";
        return result;
    }

    int strToInt(const std::string& value)
    {
        std::stringstream ss(value);
        int result(0);
        ss >> result;
        return result;
    }

    float strToFloat(const std::string& value)
    {
        std::stringstream ss(value);
        float result(0.f);
        ss >> result;
        return result;
    }

    // from string

    template <> std::string strTo(const std::string &value)
    {
        return value;
    }
    template <> float strTo(const std::string &value)
    {
        return strToFloat(value);
    }
    template <> int32_t strTo(const std::string &value)
    {
        return strToInt(value);
    }
    template <> int64_t strTo(const std::string &value)
    {
        return strToInt(value);
    }
    template <> uint32_t strTo(const std::string &value)
    {
        return static_cast<uint32_t>(strToInt(value));
    }
    template <> uint64_t strTo(const std::string &value)
    {
        return static_cast<uint64_t>(strToInt(value));
    }
    template <> bool strTo(const std::string &value)
    {
        return strToBool(value);
    }

    // to string

    template <> std::string toStr(std::string value)
    {
        return value;
    }
    template <> std::string toStr( char const * value )
    {
        return std::string( value ? value : "" );
    }
    template <> std::string toStr(const std::string &value)
    {
        return value;
    }
    template <> std::string toStr(int value)
    {
        return intToStr(value);
    }
    template <> std::string toStr(long value)
    {
        return intToStr(static_cast<int>(value));
    }
    template <> std::string toStr(long long value)
    {
        return intToStr(static_cast<int>(value));
    }
    template <> std::string toStr(unsigned int value)
    {
        return intToStr(static_cast<int>(value));
    }
    template <> std::string toStr( unsigned long value)
    {
        return intToStr(static_cast<int>(value));
    }
    template <> std::string toStr( unsigned long long value)
    {
        return intToStr(static_cast<int>(value));
    }
    template <> std::string toStr(bool value)
    {
        return boolToStr( value );
    }
    template <> std::string toStr( float value )
    {
        return floatToStr( value );
    }

    //XML
    template <> void set(pugi::xml_attribute& xml, int8_t value) { xml.set_value(value); }
    template <> void set(pugi::xml_attribute& xml, int16_t value) { xml.set_value(value); }
    template <> void set(pugi::xml_attribute& xml, int32_t value) { xml.set_value(value); }
    template <> void set(pugi::xml_attribute& xml, int64_t value) { xml.set_value(static_cast<int32_t>(value)); }
    template <> void set(pugi::xml_attribute& xml, uint8_t value) { xml.set_value(value); }
    template <> void set(pugi::xml_attribute& xml, uint16_t value) { xml.set_value(value); }
    template <> void set(pugi::xml_attribute& xml, uint32_t value) { xml.set_value(value); }
    template <> void set(pugi::xml_attribute& xml, uint64_t value) { xml.set_value(static_cast<uint32_t>(value)); }
    template <> void set(pugi::xml_attribute& xml, bool value) { xml.set_value(value); }
    template <> void set(pugi::xml_attribute& xml, float value) { xml.set_value(value); }
    template <> void set(pugi::xml_attribute& xml, std::string value) { xml.set_value(value.c_str()); }

    template <> int8_t get(const pugi::xml_attribute& xml) { return xml.as_int(); }
    template <> int16_t get(const pugi::xml_attribute& xml) { return xml.as_int(); }
    template <> int32_t get(const pugi::xml_attribute& xml) { return xml.as_int(); }
    template <> int64_t get(const pugi::xml_attribute& xml) { return xml.as_int(); }
    template <> uint8_t get(const pugi::xml_attribute& xml) { return xml.as_uint(); }
    template <> uint16_t get(const pugi::xml_attribute& xml) { return xml.as_uint(); }
    template <> uint32_t get(const pugi::xml_attribute& xml) { return xml.as_uint(); }
    template <> uint64_t get(const pugi::xml_attribute& xml) { return xml.as_uint(); }
    template <> bool get(const pugi::xml_attribute& xml) { return xml.as_bool(); }
    template <> float get(const pugi::xml_attribute& xml) { return xml.as_float(); }
    template <> std::string get(const pugi::xml_attribute& xml) { return xml.as_string(); }

    //JSON
    template <> void set( Json::Value& json, int8_t value ) { json = value; }
    template <> void set( Json::Value& json, int16_t value ) { json = value; }
    template <> void set( Json::Value& json, int32_t value ) { json = value; }
    template <> void set( Json::Value& json, int64_t value ) { json = value; }
    template <> void set( Json::Value& json, uint8_t value ) { json = value; }
    template <> void set( Json::Value& json, uint16_t value ) { json = value; }
    template <> void set( Json::Value& json, uint32_t value ) { json = value; }
    template <> void set( Json::Value& json, uint64_t value ) { json = value; }
    template <> void set( Json::Value& json, bool value ) { json = value; }
    template <> void set( Json::Value& json, float value ) { json = value; }
    template <> void set( Json::Value& json, std::string value ) { json = value; }

    template <> int8_t get( const Json::Value& json ) { return json.asInt(); }
    template <> int16_t get( const Json::Value& json ) { return json.asInt(); }
    template <> int32_t get( const Json::Value& json ) { return json.asInt(); }
    template <> int64_t get( const Json::Value& json ) { return json.asInt64(); }
    template <> uint8_t get( const Json::Value& json ) { return json.asUInt(); }
    template <> uint16_t get( const Json::Value& json ) { return json.asUInt(); }
    template <> uint32_t get( const Json::Value& json ) { return json.asUInt(); }
    template <> uint64_t get( const Json::Value& json ) { return json.asUInt64(); }
    template <> bool get( const Json::Value& json ) { return json.asBool(); }
    template <> float get( const Json::Value& json ) { return json.asFloat(); }
    template <> std::string get( const Json::Value& json ) { return json.asString(); }

    std::string format(const char *fmt, ...)
    {
        va_list args;
        va_start(args, fmt);
        std::vector<char> v(1024);
        while (true)
        {
            va_list args2;
            va_copy(args2, args);
            int res = vsnprintf(v.data(), v.size(), fmt, args2);
            if ((res >= 0) && (res < static_cast<int>(v.size())))
            {
                va_end(args);
                va_end(args2);
                return std::string(v.data());
            }
            size_t size;
            if (res < 0)
                size = v.size() * 2;
            else
                size = static_cast<size_t>(res) + 1;
            v.clear();
            v.resize(size);
            va_end(args2);
        }
    }
    
    std::vector<std::string> split(const std::string& string, const char delimiter)
    {
        std::vector<std::string> result;
        auto start = string.begin();
        auto end = string.begin();
        while (end != string.end())
        {
            if (*end == delimiter)
            {
                result.emplace_back(start, end);
                start = end + 1;
            }
            ++end;
        }
        result.emplace_back(start, end);
        return result;
    }
    
    std::string join(const std::vector<std::string>& values, const char delimiter)
    {
        if (values.empty())
        {
            return "";
        }
    
        size_t total_size = 0;
        for (const auto& value : values)
        {
            total_size += value.size();
        }
        total_size += values.size() - 1;
    
        std::string result;
        result.reserve(total_size);
    
        for (size_t i=0; i<values.size()-1; ++i)
        {
            result.append(values[i]);
            result.push_back(delimiter);
        }
        result.append(values.back());
    
        return result;
    }
    
    std::string fs_get_string(const std::string& path)
    {
        std::fstream stream(path, std::ios::in);
        std::string buffer((std::istreambuf_iterator<char>(stream)), std::istreambuf_iterator<char>());
        return buffer;
    }   
}

'''