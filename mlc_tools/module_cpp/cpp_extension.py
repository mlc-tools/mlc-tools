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

#include "pugixml/pugixml.hpp"
#include "jsoncpp/json.h"
#include "@{namespace}_Factory.h"
#include "SerializerXml.h"
#include "SerializerJson.h"

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
    int list_size(const std::vector<T>& vector)
    {
        return static_cast<int>(vector.size());
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
    
    {{format=json}}
    template <class TType>
    std::string serialize_command_to_json(intrusive_ptr<TType> command)
    {
        Json::Value json;
        command->serialize_json(json[command->get_type()]);
        
        Json::StreamWriterBuilder wbuilder;
        wbuilder["indentation"] = "";
        return Json::writeString(wbuilder, json);
    }
    
    template <class TType>
    static intrusive_ptr<TType> create_command_from_json(const std::string& payload)
    {
        Json::Value json;
        Json::Reader reader;
        reader.parse(payload, json);
        
        auto type = json.getMemberNames()[0];
        auto command = Factory::shared().build<TType>(type);
        if (command != nullptr)
        {
            command->deserialize_json(json[type]);
        }
        return command;
    }
    template <class TType>
    static intrusive_ptr<TType> clone_object(intrusive_ptr<TType> object)
    {
        auto payload = serialize_command_to_json<TType>(object);
        auto clone = create_command_from_json<TType>(payload);
        return clone;
    }
    {{end_format=json}}
    
    {{format=xml}}
    template <class TType>
    static std::string serialize_command_to_xml(intrusive_ptr<TType> command)
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
        doc.load(payload.c_str());
        auto root = doc.root().first_child();
        DeserializerXml deserializer(root);
        auto command = Factory::shared().build<TType>(root.name());
        command->deserialize_xml(deserializer);
        return command;
    }

    template <class TType>
    static intrusive_ptr<TType> clone_object(intrusive_ptr<TType> object)
    {
        auto payload = serialize_command_to_xml<TType>(object);
        auto clone = create_command_from_xml<TType>(payload);
        return clone;
    }
    {{end_format=xml}}
    
    {{format=both}}
    template <class TType>
    static std::string serialize_command_to_xml(intrusive_ptr<TType> command)
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
        doc.load(payload.c_str());
        auto root = doc.root().first_child();
        auto command = Factory::shared().build<TType>(root.name());
        DeserializerXml deserializer(root);
        command->deserialize_xml(deserializer);
        return command;
    }
    
    template <class TType>
    static std::string serialize_command_to_json(intrusive_ptr<TType> command)
    {
        Json::Value json;
        command->serialize_json(json[command->get_type()]);
        
        Json::StreamWriterBuilder wbuilder;
        wbuilder["indentation"] = "";
        return Json::writeString(wbuilder, json);
    }
    
    template <class TType>
    static intrusive_ptr<TType> create_command_from_json(const std::string& payload)
    {
        Json::Value json;
        Json::Reader reader;
        reader.parse(payload, json);
        
        auto type = json.getMemberNames()[0];
        auto command = Factory::shared().build<TType>(type);
        if (command != nullptr)
        command->deserialize_json(json[type]);
        return command;
    }
    
    template <class TType>
    static intrusive_ptr<TType> clone_object(intrusive_ptr<TType> object)
    {
        auto payload = serialize_command_to_json<TType>(object);
        auto clone = create_command_from_json<TType>(payload);
        return clone;
    }
    {{end_format=both}}
}

#endif
'''

FUNCTIONS_CPP = '''
#include <cstdlib>
#include <sstream>
#include "@{namespace}_extensions.h"

namespace @{namespace}
{
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

}

'''

INTRUSIVE_HPP = '''#ifndef __intrusive_ptr__
#define __intrusive_ptr__

#include <assert.h>
#include <memory>

namespace @{namespace}
{
    template <class TRef>
    class intrusive_ptr
    {
    public:
        intrusive_ptr(TRef * ptr = nullptr) : _ptr(nullptr)
        {
            reset(ptr);
        }

        intrusive_ptr(const intrusive_ptr& holder) : _ptr(nullptr)
        {
            reset(holder._ptr);
        }

        template <class OtherPtr>
        intrusive_ptr(intrusive_ptr<OtherPtr> holder) : _ptr(nullptr)
        {
            reset(holder.ptr());
        }

        intrusive_ptr(intrusive_ptr&& holder) : _ptr(nullptr)
        {
            _ptr = holder._ptr;
            holder._ptr = nullptr;
        }

        intrusive_ptr& operator = (const intrusive_ptr& r)
        {
            reset(r._ptr);
            return *this;
        }

        template <typename R>
        intrusive_ptr<TRef>& operator = (intrusive_ptr<R> r)
        {
            reset(r.ptr());
            return *this;
        }

        intrusive_ptr<TRef>& operator = (TRef * r)
        {
            reset(r);
            return *this;
        }

        virtual ~intrusive_ptr()
        {
            reset(nullptr);
        }

        TRef* ptr()
        {
            return _ptr;
        }

        const TRef* ptr()const
        {
            return _ptr;
        }

        TRef* operator -> ()
        {
            assert(_ptr);
            return _ptr;
        }
        const TRef* operator -> ()const
        {
            assert(_ptr);
            return _ptr;
        }

        TRef& operator * ()
        {
            assert(_ptr);
            return *_ptr;
        }
        const TRef& operator * ()const
        {
            assert(_ptr);
            return *_ptr;
        }

        operator TRef* ()
        {
            return _ptr;
        }
        operator const TRef* ()const
        {
            return _ptr;
        }

        void reset(TRef * ptr)
        {
            if(ptr != _ptr)
            {
                if(ptr)
                {
                    ptr->retain();
                }
                if(_ptr)
                {
                    _ptr->release();
                }

                _ptr = ptr;
            }
        }

        bool operator == (TRef * pointer)const
        {
            return _ptr == pointer;
        }

        bool operator != (const TRef * pointer)const
        {
            return _ptr != pointer;
        }

        bool operator != (const intrusive_ptr& holder)const
        {
            return _ptr != holder._ptr;
        }

        template <class Other>
        bool operator != (const intrusive_ptr<Other>& holder)const
        {
            return _ptr != holder.ptr();
        }

        bool operator < (const intrusive_ptr& holder)const
        {
            return _ptr < holder._ptr;
        }

    private:
        TRef * _ptr;
    };

    template<class T, class R>
    intrusive_ptr<T> dynamic_pointer_cast_intrusive(intrusive_ptr<R> pointer)
    {
        intrusive_ptr<T> result;
        T* raw = dynamic_cast<T*>(pointer.ptr());
        result.reset(raw);
        return result;
    }

    template<class Type, class...TArgs>
    inline intrusive_ptr<Type> make_intrusive(TArgs&& ... _Args)
    {
        intrusive_ptr<Type> holder;
        holder.reset(new Type(std::forward<TArgs>(_Args)...));
        holder->release();
        return holder;
    }

}

#endif
'''

FACTORY_HPP = '''#ifndef __@{namespace}_Factory_h__
#define __@{namespace}_Factory_h__
#include <string>
#include <map>
#include <iostream>
#include <assert.h>
#include "intrusive_ptr.h"
#include "jsoncpp/json.h"
#include <sstream>
#include "pugixml/pugixml.hpp"

@{registration}
namespace @{namespace}
{
    
    class Factory
    {
        class IBuilder
        {
        public:
            virtual ~IBuilder() {}
            virtual void* build() = 0;
        };
        
        template<class TType>
        class Builder : public IBuilder
        {
        public:
            virtual void* build() override
            {
                return new TType();
            };
        };
        
        ~Factory()
        {
            for(auto& pair : _builders)
            {
                delete pair.second;
            }
            _builders.clear();
        }
    public:
        static Factory& shared()
        {
            static Factory instance;
            return instance;
        }
        
        template <class TType>
        void registrationCommand( const std::string & key )
        {
            if( _builders.find( key ) != _builders.end() )
            {
                std::cout <<std::endl <<"I already have object with key [" <<key <<"]";
            }
            assert( _builders.find( key ) == _builders.end() );
            _builders[key] = new Builder<TType>();
        };
        
        template <class TType>
        intrusive_ptr<TType> build( const std::string & key ) const
        {
            bool isreg = _builders.find( key ) != _builders.end();
            if( !isreg )
            {
                return nullptr;
            }
            auto builder = _builders.at(key);
            intrusive_ptr<TType> result(reinterpret_cast<TType*>(builder->build()));
            result->release();
            return result;
        }
    private:
        std::map<std::string, IBuilder*> _builders;
    };
}

#endif // __@{namespace}_Factory_h__
'''
FACTORY_REGISTRATION = '''
#define REGISTRATION_OBJECT(TType)                                      \\
class registration__##TType                                             \\
{                                                                       \\
public:                                                                 \\
    registration__##TType()                                             \\
    {                                                                   \\
        Factory::shared().registrationCommand<TType>(TType::TYPE);      \\
    }                                                                   \\
} ___registration___##TType;
'''
SERIALIZER_XML_HPP = '''#ifndef __mg_SERIALIZERXML_H__
#define __mg_SERIALIZERXML_H__

#include <string>
#include <map>
#include <vector>
#include "intrusive_ptr.h"
#include "Pimpl.h"
#include "SerializerCommon.h"
#include "DataStorage.h"
#include "@{namespace}_Factory.h"

namespace pugi {
    class xml_node;
    class xml_document;
}

namespace mg{
class SerializerXml
{
public:
    explicit SerializerXml(pugi::xml_node node);
    SerializerXml(const SerializerXml& rhs);
    SerializerXml(SerializerXml&& rhs) noexcept;
    ~SerializerXml();
    SerializerXml& operator=(const SerializerXml& rhs);

    SerializerXml add_child(const std::string& name);
    void add_attribute(const std::string& key, const int& value, int default_value=0);
    void add_attribute(const std::string& key, const bool& value, bool default_value=false);
    void add_attribute(const std::string& key, const float& value, float default_value=0.f);
    void add_attribute(const std::string& key, const std::string& value, const std::string& default_value);

    template <class T>
    typename std::enable_if<is_attribute<T>::value, void>::type
    serialize(const T& value, const std::string& key, const T& default_value) 
    {
        add_attribute(key, value, default_value);
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    serialize(const T* value, const std::string& key) 
    {
        if(value) 
            add_attribute(key, value->name, default_value::value<std::string>());
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    serialize(const mg::intrusive_ptr<T>& value, const std::string& key){
        if(value) 
        {
            SerializerXml child = key.empty() ? *this : add_child(key);
            child.add_attribute("type", value->get_type(), "");
            value->serialize_xml(child);
        }
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    serialize(const T& value, const std::string& key){
        SerializerXml child = key.empty() ? *this : add_child(key);
        value.serialize_xml(child);
    }

    template <class T>
    typename std::enable_if<is_attribute<T>::value, void>::type
    serialize(const std::vector<T>& values, const std::string& key) 
    {
        if(values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for(const T& value : values){
            SerializerXml item = child.add_child("item");
            item.serialize(value, "value", default_value::value<T>());
        }
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    serialize(const std::vector<mg::intrusive_ptr<T>>& values, const std::string& key) 
    {
        if(values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for(const mg::intrusive_ptr<T>& value : values){
            SerializerXml item = child.add_child(value->get_type());
            value->serialize_xml(item);
        }
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    serialize(const std::vector<T>& values, const std::string& key) 
    {
        if(values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for(const T& value : values)
        {
            SerializerXml item = child.add_child("item");
            item.serialize(value, "");
        }
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    serialize(std::vector<const T*>& values, const std::string& key)
    {
        if(values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for(const T* value : values)
        {
            SerializerXml item = child.add_child("item");
            item.add_attribute("value", value->name, default_value::value<std::string>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key) 
    {
        if(values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for(auto& pair : values){
            SerializerXml item = child.add_child("pair");
            item.add_attribute("key", pair.first, default_value::value<Key>());
            item.add_attribute("value", pair.second, default_value::value<Value>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key) 
    {
        if(values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for(auto& pair : values){
            SerializerXml item = child.add_child("pair");
            SerializerXml value = item.add_child("value");
            item.add_attribute("key", pair.first, default_value::value<Key>());
            value.serialize(pair.second, std::string(""));
            // pair.second.serialize_xml(value);
        }
    }

    template <class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key) 
    {
        if(values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for(auto& pair : values){
            SerializerXml item = child.add_child("pair");
            item.add_attribute("value", pair.second, default_value::value<Value>());
            pair.first.serialize_xml(item);
        }
    }

    template <class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key) 
    {
        if(values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for(auto& pair : values){
            SerializerXml item = child.add_child("pair");
            SerializerXml pair_key = item.add_child("key");
            SerializerXml value = item.add_child("value");
            pair.first.serialize_xml(pair_key);
            pair.second.serialize_xml(value);
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, mg::intrusive_ptr<Value>>& values, const std::string& key) 
    {
        if(values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for(auto& pair : values){
            SerializerXml item = child.add_child("pair");
            item.add_attribute("key", pair.first, default_value::value<Key>());
            if(pair.second) 
            {
                SerializerXml value = item.add_child("value");
                value.add_attribute("type", pair.second->get_type(), default_value::value<std::string>());
                pair.second->serialize_xml(value);
            }
        }
    }

    template <class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, mg::intrusive_ptr<Value>>& values, const std::string& key) 
    {
        if(values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for(auto& pair : values)
        {
            SerializerXml item = child.add_child("pair");
            SerializerXml pair_key = item.add_child("key");
            pair.first.serialize_xml(pair_key);
            if(pair.second) 
            {
                SerializerXml value = item.add_child("value");
                value.add_attribute("type", pair.second->get_type(), default_value::value<std::string>());
                pair.second->serialize_xml(value);
            }
        }
    }

    template <class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    serialize(const std::map<mg::intrusive_ptr<Key>, mg::intrusive_ptr<Value>>& values, const std::string& key) 
    {
        if(values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for(auto& pair : values)
        {
            SerializerXml item = child.add_child("pair");
            SerializerXml pair_key = item.add_child("key");
            SerializerXml value = item.add_child("value");
            if(pair.first)
                pair.first->serialize_xml(pair_key);
            if(pair.second)
                pair.second->serialize_xml(value);
        }
    }

private:
    Pimpl<pugi::xml_node, 8> _node;
};

class DeserializerXml
{
public:
    explicit DeserializerXml(pugi::xml_node node);
    DeserializerXml(const DeserializerXml& rhs);
    DeserializerXml(DeserializerXml&& rhs) noexcept;
    ~DeserializerXml();
    DeserializerXml& operator=(const DeserializerXml& rhs);

    DeserializerXml get_child(const std::string& name);
    int get_attribute(const std::string& key, int default_value=0);
    bool get_attribute(const std::string& key, bool default_value=false);
    float get_attribute(const std::string& key, float default_value=0.f);
    std::string get_attribute(const std::string& key, const std::string& default_value);
    std::string get_name();

    DeserializerXml begin();
    DeserializerXml end();
    bool operator != (const DeserializerXml& rhs) const;
    DeserializerXml& operator ++ ();
    DeserializerXml operator ++ (int) noexcept = delete;
    DeserializerXml operator *();

    template <class T>
    typename std::enable_if<is_attribute<T>::value, void>::type
    deserialize(T& value, const std::string& key, const T& default_value) 
    {
        value = get_attribute(key, default_value);
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    deserialize(const T*& value, const std::string& key) 
    {
        value = DataStorage::shared().get<T>(get_attribute(key, default_value::value<std::string>()));
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    deserialize(mg::intrusive_ptr<T>& value, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        value = Factory::shared().build<T>(child.get_attribute("type", std::string()));
        value->deserialize_xml(child);
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    deserialize(T& value, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        value.deserialize_xml(child);
    }

    template <class T>
    typename std::enable_if<is_attribute<T>::value, void>::type
    deserialize(std::vector<T>& values, const std::string& key) 
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for(auto item : child)
        {
            T value;
            item.deserialize(value, "value", default_value::value<T>());
            values.push_back(value);
        }
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    deserialize(std::vector<mg::intrusive_ptr<T>>& values, const std::string& key) 
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for(auto item : child)
        {
            std::string type = item.get_name();
            mg::intrusive_ptr<T> object = Factory::shared().build<T>(type);
            object->deserialize_xml(item);
            values.push_back(object);
        }
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    deserialize(std::vector<T>& values, const std::string& key) 
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for(auto item : child)
        {
            T value;
            item.deserialize(value, default_value::value<std::string>());
            values.push_back(value);
        }
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    deserialize(std::vector<const T*>& values, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for(auto item : child)
        {
            const T* value = DataStorage::shared().get<T>(item.get_attribute("value", default_value::value<std::string>()));
            values.push_back(value);
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& values, const std::string& key) 
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for(DeserializerXml item : child)
        {
            values[item.get_attribute("key", default_value::value<Key>())] =
                    item.get_attribute("value", default_value::value<Value>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& values, const std::string& key) 
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for(DeserializerXml item : child)
        {
            DeserializerXml value = item.get_child("value");
            Value object;
            value.deserialize(object, "");
            values[item.get_attribute("key", default_value::value<Key>())] = object;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& values, const std::string& key) 
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for(DeserializerXml item : child)
        {
            Key object;
            item.deserialize(object, "");
            values[object] = item.get_attribute("value", default_value::value<Value>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& values, const std::string& key) 
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for(auto pair : child)
        {
            DeserializerXml pair_key = pair.get_child("key");
            DeserializerXml value = pair.get_child("value");
            Key key_object;
            Value value_object;
            pair_key.deserialize(key_object, "");
            value.deserialize(value_object, "");
            values[key_object] = value_object;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, mg::intrusive_ptr<Value>>& values, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for(auto item : child)
        {
            Key map_key = item.get_attribute("key", default_value::value<Key>());
            DeserializerXml value = item.get_child("value");
            mg::intrusive_ptr<Value> object = Factory::shared().build<Value>(value.get_attribute("type", std::string()));
            object->deserialize_xml(value);
            values[map_key] = object;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, mg::intrusive_ptr<Value>>& values, const std::string& key) 
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for(DeserializerXml pair : child)
        {
            DeserializerXml pair_key = pair.get_child("key");
            DeserializerXml pair_value = pair.get_child("value");
            Key key_object;
            pair_key.deserialize(key_object, "");
            mg::intrusive_ptr<Value> value_object = Factory::shared().build<Value>(pair_value.get_attribute("type", std::string()));
            value_object->deserialize_xml(pair_value);
            values[key_object] = value_object;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    deserialize(std::map<mg::intrusive_ptr<Key>, mg::intrusive_ptr<Value>>& values, const std::string& key) 
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for(DeserializerXml pair : child)
        {
            DeserializerXml pair_key = pair.get_child("key");
            DeserializerXml pair_value = pair.get_child("value");
            mg::intrusive_ptr<Value> key_object = Factory::shared().build<Value>(pair_key.get_attribute("type", std::string()));
            key_object->deserialize_xml(pair_key);
            mg::intrusive_ptr<Value> value_object = Factory::shared().build<Value>(pair_value.get_attribute("type", std::string()));
            value_object->deserialize_xml(pair_value);
            values[key_object] = value_object;
        }
    }

private:
    Pimpl<pugi::xml_node, 8> _node;
};
}

#endif //__mg_SERIALIZERXML_H__
'''
SERIALIZER_XML_CPP = '''
#include "SerializerXml.h"
#include "pugixml/pugixml.hpp"

namespace mg{
SerializerXml::SerializerXml(pugi::xml_node node)
: _node()
{
    _node = node;
}
SerializerXml::SerializerXml(const SerializerXml& rhs) = default;
SerializerXml::~SerializerXml() = default;
SerializerXml::SerializerXml(SerializerXml&& rhs) noexcept
: _node(std::move(rhs._node))
{
}
SerializerXml& SerializerXml::operator=(const SerializerXml& rhs)
{
    if(this == &rhs)
        return *this;
    *_node = *rhs._node;
    return *this;
}
SerializerXml SerializerXml::add_child(const std::string& name)
{
    return SerializerXml(_node->append_child(name.c_str()));
}
void SerializerXml::add_attribute(const std::string& key, const int& value, int default_value)
{
    if(value != default_value)
        _node->append_attribute(key.c_str()).set_value(value);
}
void SerializerXml::add_attribute(const std::string& key, const bool& value, bool default_value)
{
    if(value != default_value)
        _node->append_attribute(key.c_str()).set_value(value);
}
void SerializerXml::add_attribute(const std::string& key, const float& value, float default_value)
{
    if(value != default_value)
        _node->append_attribute(key.c_str()).set_value(value);
}
void SerializerXml::add_attribute(const std::string& key, const std::string& value, const std::string& default_value)
{
    if(value != default_value)
        _node->append_attribute(key.c_str()).set_value(value.c_str());
}


DeserializerXml::DeserializerXml(pugi::xml_node node)
{
    _node = node;
}
DeserializerXml::DeserializerXml(const DeserializerXml& rhs) = default;
DeserializerXml::DeserializerXml(DeserializerXml&& rhs) noexcept: _node(std::move(rhs._node))
{
}
DeserializerXml::~DeserializerXml() = default;
DeserializerXml& DeserializerXml::operator=(const DeserializerXml& rhs)
{
    if(this == &rhs){
        return *this;
    }
    *_node = *rhs._node;
    return *this;
}
DeserializerXml DeserializerXml::get_child(const std::string& name)
{
    return DeserializerXml(_node->child(name.c_str()));
}
int DeserializerXml::get_attribute(const std::string& key, int default_value)
{
    return _node->attribute(key.c_str()).as_int(default_value);
}
bool DeserializerXml::get_attribute(const std::string& key, bool default_value)
{
    return _node->attribute(key.c_str()).as_bool(default_value);
}
float DeserializerXml::get_attribute(const std::string& key, float default_value)
{
    return _node->attribute(key.c_str()).as_float(default_value);
}
std::string DeserializerXml::get_attribute(const std::string& key, const std::string& default_value)
{
    return _node->attribute(key.c_str()).as_string(default_value.c_str());
}
std::string DeserializerXml::get_name()
{
    return _node->name();
}

DeserializerXml DeserializerXml::begin()
{
    return DeserializerXml(*_node ? *_node->begin() : pugi::xml_node());
}
DeserializerXml DeserializerXml::end()
{
    return DeserializerXml(pugi::xml_node());
}
bool DeserializerXml::operator != (const DeserializerXml& rhs) const
{
    return *_node != *rhs._node;
}
DeserializerXml& DeserializerXml::operator ++ ()
{
    _node = _node->next_sibling();
    return *this;
}
DeserializerXml DeserializerXml::operator *()
{
    return *this;
}
}
'''
SERIALIZER_JSON_HPP = '''
#ifndef __mg_SERIALIZERJSON_H__
#define __mg_SERIALIZERJSON_H__

#include <string>
#include <map>
#include <vector>
#include "Pimpl.h"
#include "intrusive_ptr.h"
#include "SerializerCommon.h"
#include "DataStorage.h"
#include "@{namespace}_Factory.h"

namespace Json
{
    class Value;
    class ValueIterator;
}
namespace mg{
class SerializerJson 
{
public:
    explicit SerializerJson(Json::Value& json);
    SerializerJson(const SerializerJson& rhs);
    SerializerJson(SerializerJson&& rhs) noexcept;
    ~SerializerJson();
    SerializerJson& operator=(const SerializerJson& rhs) = delete;

    static void log(const Json::Value& json);
    static std::string toStr(const Json::Value& json);

    SerializerJson add_child(const std::string& name);
    SerializerJson add_array(const std::string& name);
    SerializerJson add_array_item();
    void add_attribute(const std::string& key, const int& value, int default_value=0);
    void add_attribute(const std::string& key, const bool& value, bool default_value=false);
    void add_attribute(const std::string& key, const float& value, float default_value=0.f);
    void add_attribute(const std::string& key, const std::string& value, const std::string& default_value);
    void add_array_item(const int& value);
    void add_array_item(const bool& value);
    void add_array_item(const float& value);
    void add_array_item(const std::string& value);

    template <class T>
    typename std::enable_if<is_attribute<T>::value, void>::type
    serialize(const T& value, const std::string& key, const T& default_value) {
        add_attribute(key, value, default_value);
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    serialize(const T* value, const std::string& key) {
        if(value) {
            add_attribute(key, value->name, default_value::value<std::string>());
        }
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    serialize(const mg::intrusive_ptr<T>& value, const std::string& key){
        if(value) {
            SerializerJson child = key.empty() ? *this : add_child(key);
            child.add_attribute("type", value->get_type(), "");
            value->serialize(child);
        }
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    serialize(const T& value, const std::string& key){
        SerializerJson child = key.empty() ? *this : add_child(key);
        value.serialize(child);
    }

    template <class T>
    typename std::enable_if<is_attribute<T>::value, void>::type
    serialize(const std::vector<T>& values, const std::string& key) {
        if(values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_array(key);
        for(const T& value : values){
            child.add_array_item(value);
        }
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    serialize(const std::vector<mg::intrusive_ptr<T>>& values, const std::string& key) {
        if(values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_array(key);
        for(const mg::intrusive_ptr<T>& value : values){
            SerializerJson item = child.add_array_item();
            item.add_attribute(std::string("type"), value->get_type(), default_value::value<std::string>());
            value->serialize(item);
        }
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    serialize(const std::vector<T>& values, const std::string& key) {
        if(values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_array(key);
        for(const T& value : values){
            SerializerJson item = child.add_array_item();
            item.serialize(value, "");
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key) {
        if(values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_array(key);
        for(auto& pair : values){
            SerializerJson item = child.add_array_item();
            item.add_attribute("key", pair.first, default_value::value<Key>());
            item.add_attribute("value", pair.second, default_value::value<Value>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key) {
        if(values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_child(key);
        for(auto& pair : values){
            SerializerJson item = child.add_array_item();
            SerializerJson value = item.add_child("value");
            item.add_attribute("key", pair.first, default_value::value<Key>());
            pair.second.serialize(value);
        }
    }

    template <class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key) {
        if(values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_child(key);
        for(auto& pair : values){
            SerializerJson item = child.add_array_item();
            item.add_attribute("value", pair.second, default_value::value<Value>());
            pair.first.serialize(item);
        }
    }

    template <class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key) {
        if(values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_child(key);
        for(auto& pair : values){
            SerializerJson item = child.add_array_item();
            SerializerJson pair_key = item.add_child("key");
            SerializerJson value = item.add_child("value");
            pair.first.serialize(pair_key);
            pair.second.serialize(value);
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, mg::intrusive_ptr<Value>>& values, const std::string& key) {
        if(values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_child(key);
        for(auto& pair : values){
            SerializerJson item = child.add_array_item();
            item.add_attribute("key", pair.first, default_value::value<Key>());
            if(pair.second) {
                SerializerJson value = item.add_child("value");
                value.add_attribute("type", pair.second->get_type(), default_value::value<std::string>());
                pair.second->serialize(value);
            }
        }
    }

    template <class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, mg::intrusive_ptr<Value>>& values, const std::string& key) {
        if(values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_child(key);
        for(auto& pair : values){
            SerializerJson item = child.add_array_item();
            SerializerJson pair_key = item.add_child("key");
            pair.first.serialize(pair_key);
            if(pair.second) {
                SerializerJson value = item.add_child("value");
                value.add_attribute("type", pair.second->get_type(), default_value::value<std::string>());
                pair.second->serialize(value);
            }
        }
    }

    template <class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    serialize(const std::map<mg::intrusive_ptr<Key>, mg::intrusive_ptr<Value>>& values, const std::string& key) {
        if(values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_child(key);
        for(auto& pair : values){
            SerializerJson item = child.add_array_item();
            SerializerJson pair_key = item.add_child("key");
            SerializerJson value = item.add_child("value");
            if(pair.first)
                pair.first->serialize(pair_key);
            if(pair.second)
                pair.second->serialize(value);
        }
    }

private:
    Json::Value& _json;
};

class DeserializerJson
{
    class iterator{
    public:
        explicit iterator(Json::ValueIterator iterator);
        bool operator != (const iterator& rhs) const;
        iterator& operator ++ ();
        iterator operator ++ (int) noexcept = delete;
        DeserializerJson operator *();
    private:
        Pimpl<Json::ValueIterator, 16> _iterator;
    };
public:
    explicit DeserializerJson(Json::Value& json);
    DeserializerJson(const DeserializerJson& rhs);
    DeserializerJson(DeserializerJson&& rhs) noexcept;
    ~DeserializerJson();

    DeserializerJson get_child(const std::string& name);
    int get_attribute(const std::string& key, int default_value=0);
    bool get_attribute(const std::string& key, bool default_value=false);
    float get_attribute(const std::string& key, float default_value=0.f);
    std::string get_attribute(const std::string& key, const std::string& default_value);
    void get_array_item(int& value);
    void get_array_item(bool& value);
    void get_array_item(float& value);
    void get_array_item(std::string& value);

    iterator begin();
    iterator end();

    template <class T>
    typename std::enable_if<is_attribute<T>::value, void>::type
    deserialize(T& value, const std::string& key, const T& default_value) {
        value = get_attribute(key, default_value);
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    deserialize(const T*& value, const std::string& key) {
        value = DataStorage::shared().get<T>(get_attribute(key, default_value::value<std::string>()));
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    deserialize(mg::intrusive_ptr<T>& value, const std::string& key){
        DeserializerJson child = key.empty() ? *this : get_child(key);
        std::string type = child.get_attribute(std::string("type"), default_value::value<std::string>());
        value = Factory::shared().build<T>(child.get_attribute("type", std::string()));
        value->deserialize(child);
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    deserialize(T& value, const std::string& key){
        DeserializerJson child = key.empty() ? *this : get_child(key);
        value.deserialize(child);
    }

    template <class T>
    typename std::enable_if<is_attribute<T>::value, void>::type
    deserialize(std::vector<T>& values, const std::string& key) {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for(DeserializerJson item : child){
            T value;
            item.get_array_item(value);
            values.push_back(value);
        }
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    deserialize(std::vector<mg::intrusive_ptr<T>>& values, const std::string& key) {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for(DeserializerJson item : child){
            auto type = item.get_attribute(std::string("type"), default_value::value<std::string>());
            auto value = Factory::shared().build<T>(child.get_attribute("type", std::string()));
            value->deserialize(item);
            values.push_back(value);
        }
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    deserialize(std::vector<T>& values, const std::string& key) {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for(DeserializerJson item : child){
            T value;
            item.deserialize(value, "");
            values.push_back(value);
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& values, const std::string& key) {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for(DeserializerJson item : child){
            Key key_object;
            Value value;
            key_object = item.get_attribute("key", default_value::value<Key>());
            value = item.get_attribute("value", default_value::value<Value>());
            values[key_object] = value;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& values, const std::string& key) {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for(DeserializerJson item : child){
            DeserializerJson value_json = item.get_child("value");
            Key key_object;
            Value value;
            key_object = item.get_attribute("key", default_value::value<Key>());
            value.deserialize(value_json);
            values[key_object] = value;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& values, const std::string& key) {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for(DeserializerJson item : child){
            Key key_object;
            Value value = get_attribute("value", default_value::value<Value>());
            key_object.deserialize(item);
            values[key_object] = value;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& values, const std::string& key) {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for(DeserializerJson item : child){
            DeserializerJson key_json = item.get_child("key");
            Key key_object;
            key_object.deserialize(key_json);

            DeserializerJson value_json = item.get_child("value");
            Value value;
            value.deserialize(value_json);

            values[key_object] = value;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, mg::intrusive_ptr<Value>>& values, const std::string& key) {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for(DeserializerJson item : child){
            Key key_object;
            key_object = item.get_attribute("key", default_value::value<Key>());

            DeserializerJson value_json = item.get_child("value");
            auto value = Factory::shared().build<Value>(value_json.get_attribute("type", std::string()));
            value->deserialize(value_json);

            values[key_object] = value;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, mg::intrusive_ptr<Value>>& values, const std::string& key) {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for(DeserializerJson item : child){
            DeserializerJson key_json = item.get_child("key");
            Key key_object;
            key_object.deserialize(key_json);

            DeserializerJson value_json = item.get_child("value");
            auto value = Factory::shared().build<Value>(value_json.get_attribute("type", std::string()));
            value->deserialize(value_json);

            values[key_object] = value;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    deserialize(std::map<mg::intrusive_ptr<Key>, mg::intrusive_ptr<Value>>& values, const std::string& key) {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for(DeserializerJson item : child){
            DeserializerJson key_json = item.get_child("key");
            auto key_object = Factory::shared().build<Key>(key_json.get_attribute("type", std::string()));
            key_object->deserialize(key_json);

            DeserializerJson value_json = item.get_child("value");
            auto value = Factory::shared().build<Value>(value_json.get_attribute("type", std::string()));
            value->deserialize(value_json);

            values[key_object] = value;
        }
    }

private:
    Json::Value& _json;
};
}

#endif //__mg_SERIALIZERJSON_H__
'''
SERIALIZER_JSON_CPP = '''
#include "SerializerJson.h"
#include "jsoncpp/json.h"

namespace mg{
SerializerJson::SerializerJson(Json::Value& json)
: _json(json)
{
}
SerializerJson::SerializerJson(const SerializerJson& rhs) = default;
SerializerJson::~SerializerJson() = default;
SerializerJson::SerializerJson(SerializerJson&& rhs) noexcept = default;
SerializerJson SerializerJson::add_child(const std::string& name){
    return SerializerJson(_json[name]);
}
SerializerJson SerializerJson::add_array(const std::string& name){
    return SerializerJson(_json[name]);
}
SerializerJson SerializerJson::add_array_item(){
    return SerializerJson(_json.append(Json::Value()));
}
void SerializerJson::add_attribute(const std::string& key, const int& value, int default_value){
    if(value != default_value)
        _json[key] = value;
}
void SerializerJson::add_attribute(const std::string& key, const bool& value, bool default_value){
    if(value != default_value)
        _json[key] = value;
}
void SerializerJson::add_attribute(const std::string& key, const float& value, float default_value){
    if(value != default_value)
        _json[key] = value;
}
void SerializerJson::add_attribute(const std::string& key, const std::string& value, const std::string& default_value){
    if(value != default_value)
        _json[key] = value;
}
void SerializerJson::add_array_item(const int& value){
    _json.append(value);
}
void SerializerJson::add_array_item(const bool& value){
    _json.append(value);
}
void SerializerJson::add_array_item(const float& value){
    _json.append(value);
}
void SerializerJson::add_array_item(const std::string& value){
    _json.append(value);
}


DeserializerJson::DeserializerJson(Json::Value& json)
:_json(json)
{
    
}
DeserializerJson::DeserializerJson(const DeserializerJson& rhs)
:_json(rhs._json)
{
    
}
DeserializerJson::DeserializerJson(DeserializerJson&& rhs) noexcept = default;
DeserializerJson::~DeserializerJson() = default;
DeserializerJson DeserializerJson::get_child(const std::string& name){
    return DeserializerJson(_json[name]);
}
int DeserializerJson::get_attribute(const std::string& key, int default_value){
    return _json.isMember(key) ? _json[key].asInt() : default_value;
}
bool DeserializerJson::get_attribute(const std::string& key, bool default_value){
    return _json.isMember(key) ? _json[key].asBool() : default_value;
}
float DeserializerJson::get_attribute(const std::string& key, float default_value){
    return _json.isMember(key) ? _json[key].asFloat() : default_value;
}
std::string DeserializerJson::get_attribute(const std::string& key, const std::string& default_value){
    return _json.isMember(key) ? _json[key].asString() : default_value;
}
void DeserializerJson::get_array_item(int& value){
    value = _json.asInt();
}
void DeserializerJson::get_array_item(bool& value){
    value = _json.asBool();
}
void DeserializerJson::get_array_item(float& value){
    value = _json.asFloat();
}
void DeserializerJson::get_array_item(std::string& value){
    value = _json.asString();
}

DeserializerJson::iterator DeserializerJson::begin(){
    return DeserializerJson::iterator(_json.begin());
}

DeserializerJson::iterator DeserializerJson::end(){
    return DeserializerJson::iterator(_json.end());
}

DeserializerJson::iterator::iterator(Json::ValueIterator iterator)
: _iterator(){
    _iterator = iterator;
}
bool DeserializerJson::iterator::operator != (const iterator& rhs) const{
    return *_iterator != *rhs._iterator;
}
DeserializerJson::iterator& DeserializerJson::iterator::operator ++ (){
    ++*_iterator;
    return *this;
}
DeserializerJson DeserializerJson::iterator::operator *(){
    return DeserializerJson(**_iterator);
}
}

'''
SERIALIZER_COMMON = '''
#ifndef __mg_SERIALIZERCOMMON_H__
#define __mg_SERIALIZERCOMMON_H__

#include <type_traits>

namespace mg{
template <class T>
struct is_attribute 
{
    constexpr static bool value = std::is_same<int, T>::value ||
                                  std::is_same<bool, T>::value ||
                                  std::is_same<float, T>::value ||
                                  std::is_same<std::string, T>::value;
    constexpr bool operator()() 
    {
        return value;
    }
};

struct default_value 
{
    template<class T> static typename std::enable_if<std::is_same<int, T>::value, int>::type
    value() { return 0; }

    template<class T> static typename std::enable_if<std::is_same<bool, T>::value, bool>::type
    value() { return false; }

    template<class T> static typename std::enable_if<std::is_same<float, T>::value, float>::type
    value() { return 0.f; }

    template<class T> static typename std::enable_if<std::is_same<std::string, T>::value, std::string>::type
    value() { return std::string(); }
};
}

#endif //SERIALIZER_SERIALIZERCOMMON_H
'''
SERIALIZER_PIMPL = '''
#ifndef __mg_Pimpl_h__
#define __mg_Pimpl_h__

#include <array>

namespace mg{
template <class T, size_t size>
class Pimpl
{
public:
    Pimpl()
    {
        static_assert(size == sizeof(T), "Check size pimpl");
        new (_data.data()) T;
    }
    Pimpl(const Pimpl& rhs)
    {
        static_assert(size == sizeof(T), "Check size pimpl");
        new (_data.data()) T;
        *data() = *rhs.data();
    }
    Pimpl(Pimpl&& rhs) noexcept
    : _data(std::move(rhs._data))
    {
        static_assert(size == sizeof(T), "Check size pimpl");
    }
    ~Pimpl()
    {
        static_assert(size == sizeof(T), "Check size pimpl");
        auto ptr = data();
        ptr->~T();
    }
    Pimpl& operator=(const T& data_)
    {
        static_assert(size == sizeof(T), "Check size pimpl");
        *data() = data_;
        return *this;
    }

    T* operator ->()
    {
        return data();
    }
    const T* operator ->() const
    {
        return data();
    }
    
    T& operator *()
    {
        return *data();
    }
    const T& operator *() const
    {
        return *data();
    }
private:
    T* data()
    {
        return reinterpret_cast<T*>(_data.data());
    }
    const T* data()const
    {
        return reinterpret_cast<const T*>(_data.data());
    }
private:
    std::array<unsigned char, size> _data;
};
}

#endif /* __mg_Pimpl_h__ */
'''


FILES_DICT = [
    ['@{namespace}_extensions.h', FUNCTIONS_HPP],
    ['@{namespace}_extensions.cpp', FUNCTIONS_CPP],
    ['intrusive_ptr.h', INTRUSIVE_HPP],
    ['@{namespace}_Factory.h', FACTORY_HPP],
    ['SerializerXml.h', SERIALIZER_XML_HPP],
    ['SerializerXml.cpp', SERIALIZER_XML_CPP],
    ['SerializerJson.h', SERIALIZER_JSON_HPP],
    ['SerializerJson.cpp', SERIALIZER_JSON_CPP],
    ['Pimpl.h', SERIALIZER_PIMPL],
    ['SerializerCommon.h', SERIALIZER_COMMON],
]
