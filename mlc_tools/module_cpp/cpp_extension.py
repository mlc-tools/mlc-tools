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
    static intrusive_ptr<TType> clone_object(const TType* object)
    {
        auto payload = serialize_command_to_json<TType>(object);
        auto clone = create_command_from_json<TType>(payload);
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
#include "mg_Factory.h"

namespace pugi
{
    class xml_node;
    class xml_document;
}

namespace mg
{
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
    void add_attribute(const std::string& key, const int64_t& value, int64_t default_value=0);
    void add_attribute(const std::string& key, const unsigned int& value, unsigned int default_value=0);
    void add_attribute(const std::string& key, const uint64_t& value, uint64_t default_value=0);
    void add_attribute(const std::string& key, const bool& value, bool default_value=false);
    void add_attribute(const std::string& key, const float& value, float default_value=0.f);
    void add_attribute(const std::string& key, const double& value, double default_value=0.f);
    void add_attribute(const std::string& key, const std::string& value, const std::string& default_value);

    template <class T>
    typename std::enable_if<is_attribute<T>::value, void>::type
    serialize(const T& value, const std::string& key, const T& default_value)
    {
        add_attribute(key, value, default_value);
    }

    template <class T>
    typename std::enable_if<is_enum<T>::value, void>::type
    serialize(const T& value, const std::string& key)
    {
        add_attribute(key.empty() ? std::string("value") : key, value.str(), default_value::value<std::string>());
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    serialize(const T *value, const std::string& key)
    {
        if (value)
        {
            add_attribute(key, value->name, default_value::value<std::string>());
        }
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value && !is_enum<T>::value, void>::type
    serialize(const intrusive_ptr<T>& value, const std::string& key)
    {
        if (value)
        {
            SerializerXml child = key.empty() ? *this : add_child(key);
            child.add_attribute("type", value->get_type(), "");
            value->serialize_xml(child);
        }
    }

    template <class T>
    typename std::enable_if<is_serializable<T>::value, void>::type serialize(const T& value, const std::string& key)
    {
        SerializerXml child = key.empty() ? *this : add_child(key);
        value.serialize_xml(child);
    }

/* Vectors serialization start */
    template <class T>
    typename std::enable_if<is_attribute<T>::value && !std::is_same<T, bool>::value, void>::type
    serialize(const std::vector<T>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for (const T& value : values)
        {
            SerializerXml item = child.add_child("item");
            item.serialize(value, "value", default_value::value<T>());
        }
    }

    template <class T>
    typename std::enable_if<is_attribute<T>::value && std::is_same<T, bool>::value, void>::type
    serialize(const std::vector<T>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for (T value : values)
        {
            SerializerXml item = child.add_child("item");
            item.serialize(value, "value", default_value::value<T>());
        }
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    serialize(const std::vector<intrusive_ptr<T>>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for (const intrusive_ptr<T>& value : values)
        {
            SerializerXml item = child.add_child(value ? value->get_type() : "");
            if(value)
            {
                value->serialize_xml(item);
            }
        }
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    serialize(const std::vector<T>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for (const T& value : values)
        {
            SerializerXml item = child.add_child("item");
            item.serialize(value, "");
        }
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    serialize(const std::vector<const T*>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for (const T* value : values)
        {
            SerializerXml item = child.add_child("item");
            item.serialize(value, "value");
        }
    }
/* Vectors serialization finish */
/* Maps serialization start */
    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerXml item = child.add_child("pair");
            item.add_attribute("key", pair.first, default_value::value<Key>());
            item.add_attribute("value", pair.second, default_value::value<Value>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_enum<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerXml item = child.add_child("pair");
            item.add_attribute("key", pair.first, default_value::value<Key>());
            item.add_attribute("value", pair.second.str(), default_value::value<std::string>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_data<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerXml item = child.add_child("pair");
            item.add_attribute("key", pair.first, default_value::value<Key>());
            item.add_attribute("value", pair.second ? pair.second->name : "", default_value::value<std::string>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_not_serialize_to_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerXml item = child.add_child("pair");
            item.add_attribute("key", pair.first, default_value::value<Key>());
            item.serialize(pair.second, "value");
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_enum<Key>::value && is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerXml item = child.add_child("pair");
            item.add_attribute("key", pair.first.str(), default_value::value<std::string>());
            item.add_attribute("value", pair.second, default_value::value<Value>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_enum<Key>::value && is_enum<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerXml item = child.add_child("pair");
            item.add_attribute("key", pair.first.str(), default_value::value<std::string>());
            item.add_attribute("value", pair.second.str(), default_value::value<std::string>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_enum<Key>::value && is_data<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerXml item = child.add_child("pair");
            item.add_attribute("key", pair.first.str(), default_value::value<std::string>());
            item.add_attribute("value", pair.second ? pair.second->name : "", default_value::value<std::string>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_enum<Key>::value && is_not_serialize_to_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerXml item = child.add_child("pair");
            item.add_attribute("key", pair.first.str(), default_value::value<std::string>());
            item.serialize(pair.second, "value");
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_data<Key>::value && is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerXml item = child.add_child("pair");
            item.add_attribute("key", pair.first ? pair.first->name : "", default_value::value<std::string>());
            item.add_attribute("value", pair.second, default_value::value<Value>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_data<Key>::value && is_enum<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerXml item = child.add_child("pair");
            item.add_attribute("key", pair.first ? pair.first->name : "", default_value::value<std::string>());
            item.add_attribute("value", pair.second.str(), default_value::value<std::string>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_data<Key>::value && is_data<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerXml item = child.add_child("pair");
            item.add_attribute("key", pair.first ? pair.first->name : "", default_value::value<std::string>());
            item.add_attribute("value", pair.second ? pair.second->name : "", default_value::value<std::string>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_data<Key>::value && is_not_serialize_to_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerXml item = child.add_child("pair");
            item.add_attribute("key", pair.first ? pair.first->name : "", default_value::value<std::string>());
            item.serialize(pair.second, "value");
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_not_serialize_to_attribute<Key>::value && is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerXml item = child.add_child("pair");
            item.serialize(pair.first, "key");
            item.add_attribute("value", pair.second, default_value::value<Value>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_not_serialize_to_attribute<Key>::value && is_enum<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerXml item = child.add_child("pair");
            item.serialize(pair.first, "key");
            item.add_attribute("value", pair.second.str(), default_value::value<std::string>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_not_serialize_to_attribute<Key>::value && is_data<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerXml item = child.add_child("pair");
            item.serialize(pair.first, "key");
            item.add_attribute("value", pair.second ? pair.second->name : "", default_value::value<std::string>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_not_serialize_to_attribute<Key>::value && is_not_serialize_to_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerXml item = child.add_child("pair");
            item.serialize(pair.first, "key");
            item.serialize(pair.second, "value");
        }
    }
/* Maps serialization finish */

private:
    Pimpl<pugi::xml_node, sizeof(void*)> _node;

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

    std::string get_name()const;
    int get_attribute(const std::string& key, int default_value=0);
    int64_t get_attribute(const std::string& key, int64_t default_value=0);
    unsigned int get_attribute(const std::string& key, unsigned int default_value=0);
    uint64_t get_attribute(const std::string& key, uint64_t default_value=0);
    bool get_attribute(const std::string& key, bool default_value=false);
    float get_attribute(const std::string& key, float default_value=0.f);
    double get_attribute(const std::string& key, double default_value=0.f);
    std::string get_attribute(const std::string& key, const std::string& default_value);

    DeserializerXml begin();
    DeserializerXml end();

    bool operator!=(const DeserializerXml& rhs) const;
    DeserializerXml& operator++();
    DeserializerXml operator++(int) noexcept = delete;
    DeserializerXml operator*();

    template <class T>
    typename std::enable_if<is_attribute<T>::value, void>::type
    deserialize(T& value, const std::string& key, const T& default_value)
    {
        value = get_attribute(key, default_value);
    }

    template <class T>
    typename std::enable_if<is_enum<T>::value, void>::type
    deserialize(T& value, const std::string& key)
    {
        value = get_attribute(!key.empty() ? key : "value", default_value::value<std::string>());
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    deserialize(T const *&value, const std::string& key)
    {
        value = DataStorage::shared().get<T>(get_attribute(key, default_value::value<std::string>()));
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    deserialize(intrusive_ptr<T>& value, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        auto type = child.get_attribute("type", std::string());
        if(!type.empty())
        {
            value = Factory::shared().build<T>(type);
            if(value)
            {
                value->deserialize_xml(child);
            }
        }
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value && !is_enum<T>::value, void>::type
    deserialize(T& value, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        value.deserialize_xml(child);
    }

/* Vectors deserialization start */
    template <class T>
    typename std::enable_if<is_attribute<T>::value, void>::type
    deserialize(std::vector<T>& values, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for (auto item : child)
        {
            T value;
            item.deserialize(value, "value", default_value::value<T>());
            values.push_back(value);
        }
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    deserialize(std::vector<intrusive_ptr<T>>& values, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for (auto item : child)
        {
            std::string type = item.get_name();
            intrusive_ptr<T> object = Factory::shared().build<T>(type);
            if(object)
            {
                object->deserialize_xml(item);
            }
            values.push_back(object);
        }
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    deserialize(std::vector<const T*>& values, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for (auto item : child)
        {
            const T* value = DataStorage::shared().get<T>(item.get_attribute("value", default_value::value<std::string>()));
            values.push_back(value);
        }
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    deserialize(std::vector<T>& values, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for (auto item : child)
        {
            T value;
            item.deserialize(value, default_value::value<std::string>());
            values.push_back(value);
        }
    }
/* Vectors deserialization finish */
/* Maps deserialization start */
    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for (DeserializerXml item : child)
        {
            Key key_ = item.get_attribute("key", default_value::value<Key>());
            Value value_ = item.get_attribute("value", default_value::value<Value>());
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_enum<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for (DeserializerXml item : child)
        {
            Key key_ = item.get_attribute("key", default_value::value<Key>());
            Value value_; item.deserialize(value_, "value");
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_data<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for (DeserializerXml item : child)
        {
            Key key_ = item.get_attribute("key", default_value::value<Key>());
            Value value_ = DataStorage::shared().get<typename data_type<Value>::type>(item.get_attribute("value", default_value::value<std::string>()));
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_not_serialize_to_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for (DeserializerXml item : child)
        {
            Key key_ = item.get_attribute("key", default_value::value<Key>());
            Value value_; item.deserialize(value_, "value");
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_enum<Key>::value && is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for (DeserializerXml item : child)
        {
            Key key_; item.deserialize(key_, "key");
            Value value_ = item.get_attribute("value", default_value::value<Value>());
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_enum<Key>::value && is_enum<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for (DeserializerXml item : child)
        {
            Key key_; item.deserialize(key_, "key");
            Value value_; item.deserialize(value_, "value");
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_enum<Key>::value && is_data<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for (DeserializerXml item : child)
        {
            Key key_; item.deserialize(key_, "key");
            Value value_ = DataStorage::shared().get<typename data_type<Value>::type>(item.get_attribute("value", default_value::value<std::string>()));
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_enum<Key>::value && is_not_serialize_to_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for (DeserializerXml item : child)
        {
            Key key_; item.deserialize(key_, "key");
            Value value_; item.deserialize(value_, "value");
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_data<Key>::value && is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for (DeserializerXml item : child)
        {
            Key key_ = DataStorage::shared().get<typename data_type<Key>::type>(item.get_attribute("key", default_value::value<std::string>()));
            Value value_ = item.get_attribute("value", default_value::value<Value>());
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_data<Key>::value && is_enum<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for (DeserializerXml item : child)
        {
            Key key_ = DataStorage::shared().get<typename data_type<Key>::type>(item.get_attribute("key", default_value::value<std::string>()));
            Value value_; item.deserialize(value_, "value");
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_data<Key>::value && is_data<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for (DeserializerXml item : child)
        {
            Key key_ = DataStorage::shared().get<typename data_type<Key>::type>(item.get_attribute("key", default_value::value<std::string>()));
            Value value_ = DataStorage::shared().get<typename data_type<Value>::type>(item.get_attribute("value", default_value::value<std::string>()));
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_data<Key>::value && is_not_serialize_to_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for (DeserializerXml item : child)
        {
            Key key_ = DataStorage::shared().get<typename data_type<Key>::type>(item.get_attribute("key", default_value::value<std::string>()));
            Value value_; item.deserialize(value_, "value");
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_not_serialize_to_attribute<Key>::value && is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for (DeserializerXml item : child)
        {
            Key key_; item.deserialize(key_, "key");
            Value value_ = item.get_attribute("value", default_value::value<Value>());
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_not_serialize_to_attribute<Key>::value && is_enum<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for (DeserializerXml item : child)
        {
            Key key_; item.deserialize(key_, "key");
            Value value_; item.deserialize(value_, "value");
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_not_serialize_to_attribute<Key>::value && is_data<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for (DeserializerXml item : child)
        {
            Key key_; item.deserialize(key_, "key");
            Value value_ = DataStorage::shared().get<typename data_type<Value>::type>(item.get_attribute("value", default_value::value<std::string>()));
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_not_serialize_to_attribute<Key>::value && is_not_serialize_to_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for (DeserializerXml item : child)
        {
            Key key_; item.deserialize(key_, "key");
            Value value_; item.deserialize(value_, "value");
            map[key_] = value_;
        }
    }
/* Maps deserialization finish */

private:
    Pimpl<pugi::xml_node, sizeof(void*)> _node;

};

}
#endif
'''
SERIALIZER_XML_CPP = '''#include "SerializerXml.h"
#include "pugixml/pugixml.hpp"


namespace mg
{
SerializerXml::SerializerXml(pugi::xml_node node) : _node()
{
    _node = node;
}

SerializerXml::SerializerXml(const SerializerXml &rhs) = default;


SerializerXml::~SerializerXml() = default;

SerializerXml::SerializerXml(SerializerXml &&rhs) noexcept
: _node(std::move(rhs._node))
{
}

SerializerXml &SerializerXml::operator=(const SerializerXml &rhs)
{
    if (this == &rhs)
    {
        return *this;
    }
    *_node = *rhs._node;
    return *this;
}

SerializerXml SerializerXml::add_child(const std::string &name)
{
    return SerializerXml(_node->append_child(name.c_str()));
}

void SerializerXml::add_attribute(const std::string &key, const int &value, int default_value)
{
    if (value != default_value)
    {
        _node->append_attribute(key.c_str()).set_value(value);
    }
}

void SerializerXml::add_attribute(const std::string &key, const int64_t &value, int64_t default_value)
{
    if (value != default_value)
    {
        _node->append_attribute(key.c_str()).set_value(value);
    }
}

void SerializerXml::add_attribute(const std::string &key, const unsigned int &value, unsigned int default_value)
{
    if (value != default_value)
    {
        _node->append_attribute(key.c_str()).set_value(value);
    }
}

void SerializerXml::add_attribute(const std::string &key, const uint64_t &value, uint64_t default_value)
{
    if (value != default_value)
    {
        _node->append_attribute(key.c_str()).set_value(value);
    }
}

void SerializerXml::add_attribute(const std::string &key, const bool &value, bool default_value)
{
    if (value != default_value)
    {
        _node->append_attribute(key.c_str()).set_value(value);
    }
}

void SerializerXml::add_attribute(const std::string &key, const float &value, float default_value)
{
    if (value != default_value)
    {
        _node->append_attribute(key.c_str()).set_value(value);
    }
}

void SerializerXml::add_attribute(const std::string &key, const double &value, double default_value)
{
    if (value != default_value)
    {
        _node->append_attribute(key.c_str()).set_value(value);
    }
}

void SerializerXml::add_attribute(const std::string &key, const std::string &value, const std::string &default_value)
{
    if (value != default_value)
    {
        _node->append_attribute(key.c_str()).set_value(value.c_str());
    }
}


DeserializerXml::DeserializerXml(pugi::xml_node node)
{
    _node = node;
}

DeserializerXml::DeserializerXml(const DeserializerXml &rhs) = default;

DeserializerXml::DeserializerXml(DeserializerXml &&rhs) noexcept: _node(std::move(rhs._node))
{
}

DeserializerXml::~DeserializerXml() = default;

DeserializerXml &DeserializerXml::operator=(const DeserializerXml &rhs)
{
    if (this == &rhs)
    {
        return *this;
    }
    *_node = *rhs._node;
    return *this;
}

DeserializerXml DeserializerXml::get_child(const std::string &name)
{
    return DeserializerXml(_node->child(name.c_str()));
}

std::string DeserializerXml::get_name()const
{
    return _node->name();
}

int DeserializerXml::get_attribute(const std::string &key, int default_value)
{
    return _node->attribute(key.c_str()).as_int(default_value);
}

int64_t DeserializerXml::get_attribute(const std::string &key, int64_t default_value)
{
    return _node->attribute(key.c_str()).as_llong(default_value);
}

unsigned int DeserializerXml::get_attribute(const std::string &key, unsigned int default_value)
{
    return _node->attribute(key.c_str()).as_uint(default_value);
}

uint64_t DeserializerXml::get_attribute(const std::string &key, uint64_t default_value)
{
    return _node->attribute(key.c_str()).as_ullong(default_value);
}

bool DeserializerXml::get_attribute(const std::string &key, bool default_value)
{
    return _node->attribute(key.c_str()).as_bool(default_value);
}

float DeserializerXml::get_attribute(const std::string &key, float default_value)
{
    return _node->attribute(key.c_str()).as_float(default_value);
}

double DeserializerXml::get_attribute(const std::string &key, double default_value)
{
    return _node->attribute(key.c_str()).as_double(default_value);
}

std::string DeserializerXml::get_attribute(const std::string &key, const std::string &default_value)
{
    return _node->attribute(key.c_str()).as_string(default_value.c_str());
}

DeserializerXml DeserializerXml::begin()
{
    auto begin = _node->begin();
    return DeserializerXml(begin != _node->end() ? *begin : pugi::xml_node());
}

DeserializerXml DeserializerXml::end()
{
    return DeserializerXml(pugi::xml_node());
}

bool DeserializerXml::operator!=(const DeserializerXml &rhs) const
{
    return *_node != *rhs._node;
}

DeserializerXml &DeserializerXml::operator++()
{
    _node = _node->next_sibling();
    return *this;
}

DeserializerXml DeserializerXml::operator*()
{
    return *this;
}
}
'''
SERIALIZER_JSON_HPP = '''#ifndef __mg_SERIALIZERJSON_H__
#define __mg_SERIALIZERJSON_H__

#include <string>
#include <map>
#include <vector>
#include "Pimpl.h"
#include "intrusive_ptr.h"
#include "SerializerCommon.h"
#include "DataStorage.h"
#include "mg_Factory.h"

namespace Json
{
    class Value;
    class ValueIterator;
}

namespace mg
{
class SerializerJson
{

public:
    explicit SerializerJson(Json::Value &json);
    SerializerJson(const SerializerJson &rhs);
    SerializerJson(SerializerJson &&rhs) noexcept;
    ~SerializerJson();
    SerializerJson &operator=(const SerializerJson &rhs) = delete;

    SerializerJson add_child(const std::string &name);
    SerializerJson add_array(const std::string &name);
    SerializerJson add_array_item();

    void add_attribute(const std::string &key, const int &value, int default_value = 0);
    void add_attribute(const std::string &key, const int64_t &value, int64_t default_value = 0);
    void add_attribute(const std::string &key, const unsigned int &value, unsigned int default_value = 0);
    void add_attribute(const std::string &key, const uint64_t &value, uint64_t default_value = 0);
    void add_attribute(const std::string &key, const bool &value, bool default_value = false);
    void add_attribute(const std::string &key, const float &value, float default_value = 0.f);
    void add_attribute(const std::string &key, const double &value, double default_value = 0.f);
    void add_attribute(const std::string &key, const std::string &value, const std::string &default_value);

    void add_array_item(const int &value);
    void add_array_item(const int64_t &value);
    void add_array_item(const unsigned int &value);
    void add_array_item(const uint64_t &value);
    void add_array_item(const bool &value);
    void add_array_item(const float &value);
    void add_array_item(const double &value);
    void add_array_item(const std::string &value);

    template <class T>
    typename std::enable_if<is_enum<T>::value, void>::type
    add_array_item(const T& value)
    {
        add_array_item(value.str());
    }

    template<class T>
    typename std::enable_if<is_attribute<T>::value, void>::type
    serialize(const T &value, const std::string &key, const T &default_value)
    {
        add_attribute(key, value, default_value);
    }

    template<class T>
    typename std::enable_if<is_enum<T>::value, void>::type
    serialize(const T &value, const std::string &key)
    {
        add_attribute(key.empty() ? std::string("value") : key, value.str(), default_value::value<std::string>());
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    serialize(const T *value, const std::string &key)
    {
        if (value)
        {
            add_attribute(key, value->name, default_value::value<std::string>());
        }
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    serialize(const intrusive_ptr<T> &value, const std::string &key)
    {
        if (value)
        {
            SerializerJson child = key.empty() ? *this : add_child(key);
            child.add_attribute("type", value->get_type(), "");
            value->serialize_json(child);
        }
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value && !is_enum<T>::value, void>::type
    serialize(const T &value, const std::string &key)
    {
        SerializerJson child = key.empty() ? *this : add_child(key);
        value.serialize_json(child);
    }
/* Vectors serialization start */
    template<class T>
    typename std::enable_if<(is_attribute<T>::value && !std::is_same<T, bool>::value) || is_enum<T>::value, void>::type
    serialize(const std::vector<T> &values, const std::string &key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_array(key);
        for (const T& value : values)
        {
            child.add_array_item(value);
        }
    }
    template<class T>
    typename std::enable_if<is_attribute<T>::value && std::is_same<T, bool>::value>::type
    serialize(const std::vector<T> &values, const std::string &key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_array(key);
        for (T value : values)
        {
            child.add_array_item(value);
        }
    }
    template<class T>
    typename std::enable_if<is_data<T>::value, void>::type
    serialize(const std::vector<T> &values, const std::string &key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_array(key);
        for (const T &value : values)
        {
            child.add_array_item(value ? value->name : "");
        }
    }

    template<class T>
    typename std::enable_if<is_not_serialize_to_attribute<T>::value, void>::type
    serialize(const std::vector<T> &values, const std::string &key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_array(key);
        for (const T &value : values)
        {
            SerializerJson item = child.add_array_item();
            item.serialize(value, "");
        }
    }
/* Vectors serialization finish */
/* Maps serialization start */
    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_array(key);
        for (auto& pair : values)
        {
            SerializerJson item = child.add_array_item();
            item.add_attribute("key", pair.first, default_value::value<Key>());
            item.add_attribute("value", pair.second, default_value::value<Value>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_enum<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_array(key);
        for (auto& pair : values)
        {
            SerializerJson item = child.add_array_item();
            item.add_attribute("key", pair.first, default_value::value<Key>());
            item.add_attribute("value", pair.second.str(), default_value::value<std::string>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_data<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_array(key);
        for (auto& pair : values)
        {
            SerializerJson item = child.add_array_item();
            item.add_attribute("key", pair.first, default_value::value<Key>());
            item.add_attribute("value", pair.second ? pair.second->name : "", default_value::value<std::string>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_not_serialize_to_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_array(key);
        for (auto& pair : values)
        {
            SerializerJson item = child.add_array_item();
            item.add_attribute("key", pair.first, default_value::value<Key>());
            item.serialize(pair.second, "value");
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_enum<Key>::value && is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_array(key);
        for (auto& pair : values)
        {
            SerializerJson item = child.add_array_item();
            item.add_attribute("key", pair.first.str(), default_value::value<std::string>());
            item.add_attribute("value", pair.second, default_value::value<Value>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_enum<Key>::value && is_enum<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_array(key);
        for (auto& pair : values)
        {
            SerializerJson item = child.add_array_item();
            item.add_attribute("key", pair.first.str(), default_value::value<std::string>());
            item.add_attribute("value", pair.second.str(), default_value::value<std::string>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_enum<Key>::value && is_data<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_array(key);
        for (auto& pair : values)
        {
            SerializerJson item = child.add_array_item();
            item.add_attribute("key", pair.first.str(), default_value::value<std::string>());
            item.add_attribute("value", pair.second ? pair.second->name : "", default_value::value<std::string>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_enum<Key>::value && is_not_serialize_to_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_array(key);
        for (auto& pair : values)
        {
            SerializerJson item = child.add_array_item();
            item.add_attribute("key", pair.first.str(), default_value::value<std::string>());
            item.serialize(pair.second, "value");
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_data<Key>::value && is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_array(key);
        for (auto& pair : values)
        {
            SerializerJson item = child.add_array_item();
            item.add_attribute("key", pair.first ? pair.first->name : "", default_value::value<std::string>());
            item.add_attribute("value", pair.second, default_value::value<Value>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_data<Key>::value && is_enum<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_array(key);
        for (auto& pair : values)
        {
            SerializerJson item = child.add_array_item();
            item.add_attribute("key", pair.first ? pair.first->name : "", default_value::value<std::string>());
            item.add_attribute("value", pair.second.str(), default_value::value<std::string>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_data<Key>::value && is_data<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_array(key);
        for (auto& pair : values)
        {
            SerializerJson item = child.add_array_item();
            item.add_attribute("key", pair.first ? pair.first->name : "", default_value::value<std::string>());
            item.add_attribute("value", pair.second ? pair.second->name : "", default_value::value<std::string>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_data<Key>::value && is_not_serialize_to_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_array(key);
        for (auto& pair : values)
        {
            SerializerJson item = child.add_array_item();
            item.add_attribute("key", pair.first ? pair.first->name : "", default_value::value<std::string>());
            item.serialize(pair.second, "value");
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_not_serialize_to_attribute<Key>::value && is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_array(key);
        for (auto& pair : values)
        {
            SerializerJson item = child.add_array_item();
            item.serialize(pair.first, "key");
            item.add_attribute("value", pair.second, default_value::value<Value>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_not_serialize_to_attribute<Key>::value && is_enum<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_array(key);
        for (auto& pair : values)
        {
            SerializerJson item = child.add_array_item();
            item.serialize(pair.first, "key");
            item.add_attribute("value", pair.second.str(), default_value::value<std::string>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_not_serialize_to_attribute<Key>::value && is_data<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_array(key);
        for (auto& pair : values)
        {
            SerializerJson item = child.add_array_item();
            item.serialize(pair.first, "key");
            item.add_attribute("value", pair.second ? pair.second->name : "", default_value::value<std::string>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_not_serialize_to_attribute<Key>::value && is_not_serialize_to_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_array(key);
        for (auto& pair : values)
        {
            SerializerJson item = child.add_array_item();
            item.serialize(pair.first, "key");
            item.serialize(pair.second, "value");
        }
    }
/* Maps serialization finish */

private:
    Json::Value &_json;
};

class DeserializerJson
{
    class iterator
    {
    public:
        explicit iterator(Json::ValueIterator iterator);
        bool operator!=(const iterator &rhs) const;
        iterator &operator++();
        iterator operator++(int) noexcept = delete;
        DeserializerJson operator*();
    private:
        Pimpl<Json::ValueIterator, sizeof(void*)*2> _iterator;
    };
public:
    explicit DeserializerJson(Json::Value &json);
    DeserializerJson(const DeserializerJson &rhs);
    DeserializerJson(DeserializerJson &&rhs) noexcept;
    ~DeserializerJson();

    DeserializerJson get_child(const std::string &name);

    int get_attribute(const std::string &key, int default_value = 0);
    int64_t get_attribute(const std::string &key, int64_t default_value = 0);
    unsigned int get_attribute(const std::string &key, unsigned int default_value = 0);
    uint64_t get_attribute(const std::string &key, uint64_t default_value = 0);
    bool get_attribute(const std::string &key, bool default_value = false);
    float get_attribute(const std::string &key, float default_value = 0.f);
    double get_attribute(const std::string &key, double default_value = 0.f);
    std::string get_attribute(const std::string &key, const std::string &default_value);

    void get_array_item(int &value);
    void get_array_item(int64_t &value);
    void get_array_item(unsigned int &value);
    void get_array_item(uint64_t &value);
    void get_array_item(bool &value);
    void get_array_item(float &value);
    void get_array_item(double &value);
    void get_array_item(std::string &value);

    iterator begin();
    iterator end();

    template<class T>
    typename std::enable_if<is_attribute<T>::value, void>::type
    deserialize(T &value, const std::string &key, const T &default_value)
    {
        value = get_attribute(key, default_value);
    }

    template<class T>
    typename std::enable_if<is_enum<T>::value, void>::type
    deserialize(T &value, const std::string &key)
    {
        value = get_attribute(!key.empty() ? key : "value", default_value::value<std::string>());
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    deserialize(const T *&value, const std::string &key)
    {
        value = DataStorage::shared().get<T>(get_attribute(key, default_value::value<std::string>()));
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    deserialize(intrusive_ptr<T> &value, const std::string &key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        std::string type = child.get_attribute(std::string("type"), default_value::value<std::string>());
        value = Factory::shared().build<T>(child.get_attribute("type", std::string()));
        if(value)
        {
            value->deserialize_json(child);
        }
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value && !is_enum<T>::value, void>::type
    deserialize(T &value, const std::string &key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        value.deserialize_json(child);
    }

/* Vectors deserialization start */
    template<class T>
    typename std::enable_if<is_attribute<T>::value, void>::type
    deserialize(std::vector<T> &values, const std::string &key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            T value;
            item.get_array_item(value);
            values.push_back(value);
        }
    }

    template<class T>
    typename std::enable_if<is_enum<T>::value, void>::type
    deserialize(std::vector<T> &values, const std::string &key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            std::string value_string;
            item.get_array_item(value_string);
            T value(value_string);
            values.push_back(value);
        }
    }

    template<class T>
    typename std::enable_if<is_data<T>::value, void>::type
    deserialize(std::vector<T> &values, const std::string &key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            std::string value_string;
            item.get_array_item(value_string);
            T value = DataStorage::shared().get<typename data_type<T>::type>(value_string);
            values.push_back(value);
        }
    }

    template<class T>
    typename std::enable_if<is_not_serialize_to_attribute<T>::value, void>::type
    deserialize(std::vector<T> &values, const std::string &key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            T value;
            item.deserialize(value, "");
            values.push_back(value);
        }
    }
/* Vectors deserialization finish */
/* Maps deserialization start */
    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            Key key_ = item.get_attribute("key", default_value::value<Key>());
            Value value_ = item.get_attribute("value", default_value::value<Value>());
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_enum<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            Key key_ = item.get_attribute("key", default_value::value<Key>());
            Value value_; item.deserialize(value_, "value");
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_data<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            Key key_ = item.get_attribute("key", default_value::value<Key>());
            Value value_ = DataStorage::shared().get<typename data_type<Value>::type>(item.get_attribute("value", default_value::value<std::string>()));
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_not_serialize_to_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            Key key_ = item.get_attribute("key", default_value::value<Key>());
            Value value_; item.deserialize(value_, "value");
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_enum<Key>::value && is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            Key key_; item.deserialize(key_, "key");
            Value value_ = item.get_attribute("value", default_value::value<Value>());
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_enum<Key>::value && is_enum<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            Key key_; item.deserialize(key_, "key");
            Value value_; item.deserialize(value_, "value");
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_enum<Key>::value && is_data<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            Key key_; item.deserialize(key_, "key");
            Value value_ = DataStorage::shared().get<typename data_type<Value>::type>(item.get_attribute("value", default_value::value<std::string>()));
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_enum<Key>::value && is_not_serialize_to_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            Key key_; item.deserialize(key_, "key");
            Value value_; item.deserialize(value_, "value");
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_data<Key>::value && is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            Key key_ = DataStorage::shared().get<typename data_type<Key>::type>(item.get_attribute("key", default_value::value<std::string>()));
            Value value_ = item.get_attribute("value", default_value::value<Value>());
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_data<Key>::value && is_enum<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            Key key_ = DataStorage::shared().get<typename data_type<Key>::type>(item.get_attribute("key", default_value::value<std::string>()));
            Value value_; item.deserialize(value_, "value");
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_data<Key>::value && is_data<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            Key key_ = DataStorage::shared().get<typename data_type<Key>::type>(item.get_attribute("key", default_value::value<std::string>()));
            Value value_ = DataStorage::shared().get<typename data_type<Value>::type>(item.get_attribute("value", default_value::value<std::string>()));
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_data<Key>::value && is_not_serialize_to_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            Key key_ = DataStorage::shared().get<typename data_type<Key>::type>(item.get_attribute("key", default_value::value<std::string>()));
            Value value_; item.deserialize(value_, "value");
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_not_serialize_to_attribute<Key>::value && is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            Key key_; item.deserialize(key_, "key");
            Value value_ = item.get_attribute("value", default_value::value<Value>());
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_not_serialize_to_attribute<Key>::value && is_enum<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            Key key_; item.deserialize(key_, "key");
            Value value_; item.deserialize(value_, "value");
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_not_serialize_to_attribute<Key>::value && is_data<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            Key key_; item.deserialize(key_, "key");
            Value value_ = DataStorage::shared().get<typename data_type<Value>::type>(item.get_attribute("value", default_value::value<std::string>()));
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_not_serialize_to_attribute<Key>::value && is_not_serialize_to_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            Key key_; item.deserialize(key_, "key");
            Value value_; item.deserialize(value_, "value");
            map[key_] = value_;
        }
    }
/* Maps deserialization finish */

private:
    Json::Value &_json;

};
}
#endif //__mg_SERIALIZERJSON_H__
'''
SERIALIZER_JSON_CPP = '''#include "SerializerJson.h"
#include "jsoncpp/json.h"


namespace mg
{
SerializerJson::SerializerJson(Json::Value &json) : _json(json)
{
}

SerializerJson::SerializerJson(const SerializerJson &rhs) = default;


SerializerJson::~SerializerJson() = default;

SerializerJson::SerializerJson(SerializerJson &&rhs) noexcept = default;


SerializerJson SerializerJson::add_child(const std::string &name)
{
    return SerializerJson(_json[name]);
}

SerializerJson SerializerJson::add_array(const std::string &name)
{
    return SerializerJson(_json[name]);
}

SerializerJson SerializerJson::add_array_item()
{
    return SerializerJson(_json.append(Json::Value()));
}

void SerializerJson::add_attribute(const std::string &key, const int &value, int default_value)
{
    if (value != default_value)
    {
        _json[key] = value;
    }
}

void SerializerJson::add_attribute(const std::string &key, const int64_t &value, int64_t default_value)
{
    if (value != default_value)
    {
        _json[key] = value;
    }
}

void SerializerJson::add_attribute(const std::string &key, const unsigned int &value, unsigned int default_value)
{
    if (value != default_value)
    {
        _json[key] = value;
    }
}

void SerializerJson::add_attribute(const std::string &key, const uint64_t &value, uint64_t default_value)
{
    if (value != default_value)
    {
        _json[key] = value;
    }
}

void SerializerJson::add_attribute(const std::string &key, const bool &value, bool default_value)
{
    if (value != default_value)
    {
        _json[key] = value;
    }
}

void SerializerJson::add_attribute(const std::string &key, const float &value, float default_value)
{
    if (value != default_value)
    {
        _json[key] = value;
    }
}

void SerializerJson::add_attribute(const std::string &key, const double &value, double default_value)
{
    if (value != default_value)
    {
        _json[key] = value;
    }
}

void SerializerJson::add_attribute(const std::string &key, const std::string &value, const std::string &default_value)
{
    if (value != default_value)
    {
        _json[key] = value;
    }
}

void SerializerJson::add_array_item(const int &value)
{
    _json.append(value);
}

void SerializerJson::add_array_item(const int64_t &value)
{
    _json.append(value);
}

void SerializerJson::add_array_item(const unsigned int &value)
{
    _json.append(value);
}

void SerializerJson::add_array_item(const uint64_t &value)
{
    _json.append(value);
}

void SerializerJson::add_array_item(const bool &value)
{
    _json.append(value);
}

void SerializerJson::add_array_item(const float &value)
{
    _json.append(value);
}

void SerializerJson::add_array_item(const double &value)
{
    _json.append(value);
}

void SerializerJson::add_array_item(const std::string &value)
{
    _json.append(value);
}


DeserializerJson::DeserializerJson(Json::Value &json) : _json(json)
{

}

DeserializerJson::DeserializerJson(const DeserializerJson &rhs) : _json(rhs._json)
{

}

DeserializerJson::DeserializerJson(DeserializerJson &&rhs) noexcept = default;

DeserializerJson::~DeserializerJson() = default;

DeserializerJson DeserializerJson::get_child(const std::string &name)
{
    return DeserializerJson(_json[name]);
}

int DeserializerJson::get_attribute(const std::string &key, int default_value)
{
    return _json.isMember(key) ? _json[key].asInt() : default_value;
}

int64_t DeserializerJson::get_attribute(const std::string &key, int64_t default_value)
{
    return _json.isMember(key) ? _json[key].asInt64() : default_value;
}

unsigned int DeserializerJson::get_attribute(const std::string &key, unsigned int default_value)
{
    return _json.isMember(key) ? _json[key].asUInt() : default_value;
}

uint64_t DeserializerJson::get_attribute(const std::string &key, uint64_t default_value)
{
    return _json.isMember(key) ? _json[key].asUInt64() : default_value;
}

bool DeserializerJson::get_attribute(const std::string &key, bool default_value)
{
    return _json.isMember(key) ? _json[key].asBool() : default_value;
}

float DeserializerJson::get_attribute(const std::string &key, float default_value)
{
    return _json.isMember(key) ? _json[key].asFloat() : default_value;
}

double DeserializerJson::get_attribute(const std::string &key, double default_value)
{
    return _json.isMember(key) ? _json[key].asFloat() : default_value;
}

std::string DeserializerJson::get_attribute(const std::string &key, const std::string &default_value)
{
    return _json.isMember(key) ? _json[key].asString() : default_value;
}

void DeserializerJson::get_array_item(int &value)
{
    value = _json.asInt();
}

void DeserializerJson::get_array_item(int64_t &value)
{
    value = _json.asInt64();
}

void DeserializerJson::get_array_item(bool &value)
{
    value = _json.asBool();
}

void DeserializerJson::get_array_item(float &value)
{
    value = _json.asFloat();
}

void DeserializerJson::get_array_item(double &value)
{
    value = _json.asDouble();
}

void DeserializerJson::get_array_item(std::string &value)
{
    value = _json.asString();
}

DeserializerJson::iterator DeserializerJson::begin()
{
    return DeserializerJson::iterator(_json.begin());
}

DeserializerJson::iterator DeserializerJson::end()
{
    return DeserializerJson::iterator(_json.end());
}

DeserializerJson::iterator::iterator(Json::ValueIterator iterator) : _iterator()
{
    _iterator = iterator;
}

bool DeserializerJson::iterator::operator!=(const iterator &rhs) const
{
    return *_iterator != *rhs._iterator;
}

DeserializerJson::iterator &DeserializerJson::iterator::operator++()
{
    ++*_iterator;
    return *this;
}

DeserializerJson DeserializerJson::iterator::operator*()
{
    return DeserializerJson(**_iterator);
}
}
'''
SERIALIZER_COMMON = '''#ifndef __mg_SERIALIZERCOMMON_H__
#define __mg_SERIALIZERCOMMON_H__

#include <type_traits>
#include "BaseEnum.h"
#include "intrusive_ptr.h"

namespace mg
{
class SerializerXml;
class DeserializerXml;
class SerializerJson;
class DeserializerJson;

template<class T>
struct is_attribute
{
    constexpr static bool value = (std::is_same<int, T>::value ||
                                   std::is_same<unsigned int, T>::value ||
                                   std::is_same<int64_t, T>::value ||
                                   std::is_same<uint64_t, T>::value ||
                                   std::is_same<bool, T>::value ||
                                   std::is_same<float, T>::value ||
                                   std::is_same<double, T>::value ||
                                   std::is_same<std::string, T>::value) &&
                                  !std::is_base_of<BaseEnum, T>::value;

    constexpr bool operator()() {
        return value;
    }
};

template<class T>
struct is_enum
{
    constexpr static bool value = std::is_base_of<BaseEnum, T>::value;

    constexpr bool operator()() {
        return value;
    }
};

template<typename, typename T>
struct has_serialize {
    static_assert( std::integral_constant<T, false>::value, "Second template parameter needs to be of function type.");
};
template<typename C, typename Ret, typename... Args>
struct has_serialize<C, Ret(Args...)> {
private:
    template<typename T>
    static constexpr auto check_xml(T*) -> typename std::is_same< decltype( std::declval<T>().serialize_xml( std::declval<Args>()... ) ),Ret>::type;
    template<typename>
    static constexpr std::false_type check_xml(...);
    typedef decltype(check_xml<C>(0)) type_xml;

    template<typename T>
    static constexpr auto check_json(T*) -> typename std::is_same< decltype( std::declval<T>().serialize_json( std::declval<Args>()... ) ),Ret>::type;
    template<typename>
    static constexpr std::false_type check_json(...);
    typedef decltype(check_json<C>(0)) type_json;
public:
    static constexpr bool value_xml = type_xml::value;
    static constexpr bool value_json = type_json::value;
};
template <class T>
struct is_serializable{
    constexpr static bool value =
            has_serialize<T, void(SerializerXml&)>::value_xml ||
            has_serialize<T, void(SerializerJson&)>::value_json;
    constexpr bool operator()() {
        return value;
    }
};

template<class T> struct is_data : std::false_type {};
template<class T> struct is_data<const T*> {
    constexpr static bool value = !is_enum<T>::value && !is_attribute<T>::value && is_serializable<T>::value;
};
template <class T> struct data_type {};
template <class T> struct data_type<const T*>{
    typedef T type;
};


template<class T> struct is_intrusive : std::false_type {};
template<class T> struct is_intrusive<intrusive_ptr<T>> {
    constexpr static bool value = is_serializable<T>::value;
};

template<class T> struct is_not_serialize_to_attribute {
    constexpr static bool value =
            !is_enum<T>::value &&
            !is_attribute<T>::value &&
            !is_data<T>::value;
};

struct default_value
{
    template<class T>
    static typename std::enable_if<std::is_same<int, T>::value, int>::type
    value() { return 0; }

    template<class T>
    static typename std::enable_if<std::is_same<unsigned int, T>::value, unsigned int>::type
    value() { return 0; }

    template<class T>
    static typename std::enable_if<std::is_same<int64_t, T>::value, int64_t>::type
    value() { return 0ull; }

    template<class T>
    static typename std::enable_if<std::is_same<uint64_t, T>::value, uint64_t>::type
    value() { return 0ll; }

    template<class T>
    static typename std::enable_if<std::is_same<bool, T>::value, bool>::type
    value() { return false; }

    template<class T>
    static typename std::enable_if<std::is_same<float, T>::value, float>::type
    value() { return 0.f; }

    template<class T>
    static typename std::enable_if<std::is_same<double, T>::value, double>::type
    value() { return 0.0; }

    template<class T>
    static typename std::enable_if<std::is_same<std::string, T>::value, std::string>::type
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

BASE_ENUM_HPP='''#ifndef __mg_BaseEnum_h__
#define __mg_BaseEnum_h__

#include <string>

namespace mg
{
    class BaseEnum
    {
    public:
        constexpr BaseEnum(int value_ = 0): value(value_) {}
        constexpr BaseEnum(const BaseEnum& rhs): value(rhs.value) {}
        constexpr operator int() const { return value; }
    protected:
        int value;
    };
}

#endif
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
    ['BaseEnum.h', BASE_ENUM_HPP],
]
