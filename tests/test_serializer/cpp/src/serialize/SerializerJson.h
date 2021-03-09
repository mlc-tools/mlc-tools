#ifndef __mg_SERIALIZERJSON_H__
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
    void add_attribute(const std::string &key, const bool &value, bool default_value = false);
    void add_attribute(const std::string &key, const float &value, float default_value = 0.f);
    void add_attribute(const std::string &key, const std::string &value, const std::string &default_value);

    void add_array_item(const int &value);
    void add_array_item(const int64_t &value);
    void add_array_item(const bool &value);
    void add_array_item(const float &value);
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
            child.add_array_item(value->name);
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
            item.add_attribute("value", pair.second->name, default_value::value<std::string>());            
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
            item.add_attribute("value", pair.second->name, default_value::value<std::string>());            
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
            item.add_attribute("key", pair.first->name, default_value::value<std::string>());
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
            item.add_attribute("key", pair.first->name, default_value::value<std::string>());
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
            item.add_attribute("key", pair.first->name, default_value::value<std::string>());
            item.add_attribute("value", pair.second->name, default_value::value<std::string>());            
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
            item.add_attribute("key", pair.first->name, default_value::value<std::string>());
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
            item.add_attribute("value", pair.second->name, default_value::value<std::string>());            
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
    bool get_attribute(const std::string &key, bool default_value = false);
    float get_attribute(const std::string &key, float default_value = 0.f);
    std::string get_attribute(const std::string &key, const std::string &default_value);

    void get_array_item(int &value);
    void get_array_item(int64_t &value);
    void get_array_item(bool &value);
    void get_array_item(float &value);
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
