functions_hpp = '''
#ifndef __@{namespace}_functions_h__
#define __@{namespace}_functions_h__

#include <map>
#include <vector>
#include <cmath>
#include <string>
#include <algorithm>
#include "config.h"

#if MG_SERIALIZE_FORMAT == MG_XML
#   include "pugixml/pugixml.hpp"
#elif MG_SERIALIZE_FORMAT == MG_JSON
#   include "jsoncpp/json.h"
#endif

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
    void list_remove(std::vector<T>& list, const I& t)
    {
        auto iter = std::find(list.begin(), list.end(), t);
        if(iter != list.end())
            list.erase(iter);
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

    template <class T, class P>
    int map_size(const std::map<T, P>& map)
    {
        return static_cast<int>(map.size());
    }

    bool string_empty(const std::string& string);
    int string_size(const std::string& string);

    float random_float();
    int random_int(int min, int max);

    // Converters
    template <typename T> T strTo(const std::string &value);
    template <typename T> std::string toStr(T value);

#if MG_SERIALIZE_FORMAT == MG_XML

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

#elif MG_SERIALIZE_FORMAT == MG_JSON

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

#endif

}

#endif
'''
functions_cpp = '''
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

#if MG_SERIALIZE_FORMAT == MG_XML

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

#elif MG_SERIALIZE_FORMAT == MG_JSON

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

#endif
}

'''

intrusive_hpp = '''#ifndef __intrusive_ptr__
#define __intrusive_ptr__

#include <assert.h>
#include <memory>

namespace @{namespace}
{
    class SerializedObject;

    void __intrusive_ptr__retain(SerializedObject* ptr);
    void __intrusive_ptr__release(SerializedObject* ptr);

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
                    __intrusive_ptr__retain(ptr);
                if(_ptr)
                    __intrusive_ptr__release(_ptr);

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
intrusive_cpp = '''#include "intrusive_ptr.h"
#include "SerializedObject.h"

namespace @{namespace}
{
    void __intrusive_ptr__retain( SerializedObject* ptr )
    {
        ptr->retain();
    }

    void __intrusive_ptr__release( SerializedObject* ptr )
    {
        ptr->release();
    }
}
'''

factory_hpp = '''#ifndef __@{namespace}_Factory_h__
#define __@{namespace}_Factory_h__
#include <string>
#include <map>
#include <iostream>
#include <assert.h>
#include "intrusive_ptr.h"
#include "SerializedObject.h"
#include "config.h"

#if MG_SERIALIZE_FORMAT == MG_JSON
#   include "jsoncpp/json.h"
#else
#   include <sstream>
#endif

#define REGISTRATION_OBJECT(TType) class registrator__##TType { \
public: registrator__##TType() { Factory::shared().registrationCommand<TType>( TType::TYPE ); } } \
___registrator___##TType;

namespace @{namespace}
{

    template <class TRef>
    class TFactory
    {
        class IObject : public TRef
        {
        public:
            virtual intrusive_ptr<TRef> build() = 0;
        };

        template<class TType>
        class Object : public IObject
        {
        public:
            virtual intrusive_ptr<TRef> build()
            {
                return dynamic_pointer_cast_intrusive<TRef>( make_intrusive<TType>() );
            };
        };
    public:
        static TFactory& shared()
        {
            static TFactory instance;
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
            auto ptr = make_intrusive<Object<TType>>();
            _builders[key] = ptr;
        };

        intrusive_ptr<TRef> build( const std::string & key )
        {
            bool isreg = _builders.find( key ) != _builders.end();
            if( !isreg )
                return nullptr;
            return isreg ? _builders[key]->build() : nullptr;
        }

        template <class TType>
        intrusive_ptr<TType> build( const std::string & key )
        {
            intrusive_ptr<TRef> ptr = build( key );
            intrusive_ptr<TType> result = dynamic_pointer_cast_intrusive<TType>( ptr );
            return result;
        };

    #if MG_SERIALIZE_FORMAT == MG_JSON
        static std::string serialize_command(intrusive_ptr<TRef> command)
        {
            Json::Value json;
            command->serialize(json[command->get_type()]);

            Json::StreamWriterBuilder wbuilder;
            wbuilder["indentation"] = "";
            return Json::writeString(wbuilder, json);
        }
        static intrusive_ptr<TRef> create_command(const std::string& payload)
        {
            Json::Value json;
            Json::Reader reader;
            reader.parse(payload, json);

            auto type = json.getMemberNames()[0];
            auto command = shared().build(type);
            if (command != nullptr)
                command->deserialize(json[type]);
            return command;
        }
    #else
        static std::string serialize_command(intrusive_ptr<TRef> command)
        {
            pugi::xml_document doc;
            auto root = doc.append_child(command->get_type().c_str());
            command->serialize(root);

            std::stringstream stream;
            pugi::xml_writer_stream writer(stream);
            doc.save(writer, "", pugi::format_no_declaration | pugi::format_raw, pugi::xml_encoding::encoding_utf8);
            return stream.str();
        }
        static intrusive_ptr<TRef> create_command(const std::string& payload)
        {
            pugi::xml_document doc;
            doc.load(payload.c_str());
            auto root = doc.root().first_child();
            auto command = shared().build(root.name());
            command->deserialize(root);
            return command;
        }
    #endif

        template <class TType>
        static intrusive_ptr<TType> create_command(const std::string& payload)
        {
            return dynamic_pointer_cast_intrusive<TType>(create_command(payload));
        }

    private:
        std::map<std::string, intrusive_ptr<IObject>> _builders;
    };

    using Factory = TFactory<SerializedObject>;
}

#endif
'''


cpp_files = [
    ['@{namespace}_extensions.h', functions_hpp],
    ['@{namespace}_extensions.cpp', functions_cpp],
    ['intrusive_ptr.h', intrusive_hpp],
    ['intrusive_ptr.cpp', intrusive_cpp],
    ['Factory.h', factory_hpp],
]
