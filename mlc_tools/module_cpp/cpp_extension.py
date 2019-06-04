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
        Type* ptr = new Type(std::forward<TArgs>(_Args)...);
        if(ptr)
        {
            holder.reset(ptr);
            ptr->release();
        }
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

#define REGISTRATION_OBJECT(TType)                                      \\
class registration__##TType                                             \\
{                                                                       \\
public:                                                                 \\
    registration__##TType()                                             \\
    {                                                                   \\
        Factory::shared().registrationCommand<TType>( TType::TYPE );    \\
    }                                                                   \\
} ___registration___##TType;

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
        
        {{format=json}}
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
            auto command = shared().build<TType>(type);
            if (command != nullptr)
            command->deserialize_json(json[type]);
            return command;
        }
        template <class TType>
        static intrusive_ptr<TType> clone_object(intrusive_ptr<TType> object)
        {
            auto payload = Factory::serialize_command_to_json<TType>(object);
            auto clone = Factory::create_command_from_json<TType>(payload);
            return clone;
        }
        {{end_format=json}}
        
        {{format=xml}}
        template <class TType>
        static std::string serialize_command_to_xml(intrusive_ptr<TType> command)
        {
            pugi::xml_document doc;
            auto root = doc.append_child(command->get_type().c_str());
            command->serialize_xml(root);
            
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
            auto command = shared().build<TType>(root.name());
            command->deserialize_xml(root);
            return command;
        }

        template <class TType>
        static intrusive_ptr<TType> clone_object(intrusive_ptr<TType> object)
        {
            auto payload = Factory::serialize_command_to_xml<TType>(object);
            auto clone = Factory::create_command_from_xml<TType>(payload);
            return clone;
        }
        {{end_format=xml}}
        
        {{format=both}}
        template <class TType>
        static std::string serialize_command_to_xml(intrusive_ptr<TType> command)
        {
            pugi::xml_document doc;
            auto root = doc.append_child(command->get_type().c_str());
            command->serialize_xml(root);
            
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
            auto command = shared().build<TType>(root.name());
            command->deserialize_xml(root);
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
            auto command = shared().build<TType>(type);
            if (command != nullptr)
            command->deserialize_json(json[type]);
            return command;
        }
        
        template <class TType>
        static intrusive_ptr<TType> clone_object(intrusive_ptr<TType> object)
        {
            auto payload = Factory::serialize_command_to_json<TType>(object);
            auto clone = Factory::create_command_from_json<TType>(payload);
            return clone;
        }
        {{end_format=both}}
    private:
        std::map<std::string, IBuilder*> _builders;
    };
}

#endif // __@{namespace}_Factory_h__
'''


FILES_DICT = [
    ['@{namespace}_extensions.h', FUNCTIONS_HPP],
    ['@{namespace}_extensions.cpp', FUNCTIONS_CPP],
    ['intrusive_ptr.h', INTRUSIVE_HPP],
    ['@{namespace}_Factory.h', FACTORY_HPP],
]
