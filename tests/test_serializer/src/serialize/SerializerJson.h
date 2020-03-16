//
// Created by Vladimir Tolmachev on 2020-02-21.
//

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
    void add_attribute(const std::string &key, const bool &value, bool default_value = false);
    void add_attribute(const std::string &key, const float &value, float default_value = 0.f);
    void add_attribute(const std::string &key, const std::string &value, const std::string &default_value);

    void add_array_item(const int &value);
    void add_array_item(const bool &value);
    void add_array_item(const float &value);
    void add_array_item(const std::string &value);
    void add_array_item(const mg::BaseEnum &value);

    template<class T>
    typename std::enable_if<is_attribute<T>::value, void>::type
    serialize(const T &value, const std::string &key, const T &default_value)
    {
        add_attribute(key, value, default_value);
    }

    template<class T>
    typename std::enable_if<is_enum<T>::value, void>::type serialize(const T &value, const std::string &key)
    {
        add_attribute(key.empty() ? std::string("value") : key, value.str(), default_value::value<std::string>());
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type serialize(const T *value, const std::string &key)
    {
        if (value)
        {
            add_attribute(key, value->name, default_value::value<std::string>());
        }
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    serialize(const mg::intrusive_ptr<T> &value, const std::string &key)
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

    template<class T>
    typename std::enable_if<is_attribute<T>::value || is_enum<T>::value, void>::type
    serialize(const std::vector<T> &values, const std::string &key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_array(key);
        for (const T &value : values)
        {
            child.add_array_item(value);
        }
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    serialize(const std::vector<mg::intrusive_ptr<T>> &values, const std::string &key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_array(key);
        for (const mg::intrusive_ptr<T> &value : values)
        {
            SerializerJson item = child.add_array_item();
            item.add_attribute(std::string("type"), value->get_type(), default_value::value<std::string>());
            value->serialize_json(item);
        }
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value && !is_enum<T>::value, void>::type
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

    template<class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value> &values, const std::string &key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_array(key);
        for (auto &pair : values)
        {
            SerializerJson item = child.add_array_item();
            item.add_attribute("key", pair.first, default_value::value<Key>());
            item.add_attribute("value", pair.second, default_value::value<Value>());
        }
    }

    template<class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value> &values, const std::string &key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_child(key);
        for (auto &pair : values)
        {
            SerializerJson item = child.add_array_item();
            SerializerJson value = item.add_child("value");
            item.add_attribute("key", pair.first, default_value::value<Key>());
            value.serialize(pair.second, "");
        }
    }

    template<class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, const Value*> &values, const std::string &key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_child(key);
        for (auto &pair : values)
        {
            SerializerJson item = child.add_array_item();
            item.add_attribute("key", pair.first, default_value::value<Key>());
            item.add_attribute("value", pair.second->name, default_value::value<std::string>());
        }
    }

    template<class Key, class Value>
    typename std::enable_if<is_enum<Key>::value && is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value> &values, const std::string &key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_child(key);
        for (auto &pair : values)
        {
            SerializerJson item = child.add_array_item();
            item.add_attribute("value", pair.second, default_value::value<Value>());
            item.serialize(pair.first, "key");
        }
    }

    template<class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_enum<Key>::value && is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value> &values, const std::string &key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_child(key);
        for (auto &pair : values)
        {
            SerializerJson item = child.add_array_item();
            item.add_attribute("value", pair.second, default_value::value<Value>());
            item.serialize(pair.first, "key");
        }
    }

    template<class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && is_attribute<Value>::value, void>::type
    serialize(const std::map<const Key*, Value> &values, const std::string &key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_child(key);
        for (auto &pair : values)
        {
            SerializerJson item = child.add_array_item();
            item.add_attribute("key", pair.first->name, default_value::value<std::string>());
            item.add_attribute("value", pair.second, default_value::value<Value>());
        }
    }

    template<class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value> &values, const std::string &key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_child(key);
        for (auto &pair : values)
        {
            SerializerJson item = child.add_array_item();
            SerializerJson pair_key = item.add_child("key");
            SerializerJson value = item.add_child("value");
            pair.first.serialize_json(pair_key);
            pair.second.serialize_json(value);
        }
    }

    template<class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    serialize(const std::map<const Key*, const Value*> &values, const std::string &key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_child(key);
        for (auto &pair : values)
        {
            SerializerJson item = child.add_array_item();
            item.add_attribute("key", pair.first->name, default_value::value<std::string>());
            item.add_attribute("value", pair.second->name, default_value::value<std::string>());
//            SerializerJson item = child.add_array_item();
//            SerializerJson pair_key = item.add_child("key");
//            SerializerJson value = item.add_child("value");
//            pair.first.serialize_json(pair_key);
//            pair.second.serialize_json(value);
        }
    }

    template<class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, mg::intrusive_ptr<Value>> &values, const std::string &key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_child(key);
        for (auto &pair : values)
        {
            SerializerJson item = child.add_array_item();
            item.add_attribute("key", pair.first, default_value::value<Key>());
            if (pair.second)
            {
                SerializerJson value = item.add_child("value");
                value.add_attribute("type", pair.second->get_type(), default_value::value<std::string>());
                pair.second->serialize_json(value);
            }
        }
    }

    template<class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, mg::intrusive_ptr<Value>> &values, const std::string &key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_child(key);
        for (auto &pair : values)
        {
            SerializerJson item = child.add_array_item();
            SerializerJson pair_key = item.add_child("key");
            pair.first.serialize_json(pair_key);
            if (pair.second)
            {
                SerializerJson value = item.add_child("value");
                value.add_attribute("type", pair.second->get_type(), default_value::value<std::string>());
                pair.second->serialize_json(value);
            }
        }
    }

    template<class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    serialize(const std::map<mg::intrusive_ptr<Key>, mg::intrusive_ptr<Value>> &values, const std::string &key)
    {
        if (values.empty())
            return;
        SerializerJson child = key.empty() ? *this : add_child(key);
        for (auto &pair : values)
        {
            SerializerJson item = child.add_array_item();
            SerializerJson pair_key = item.add_child("key");
            SerializerJson value = item.add_child("value");
            if (pair.first)
            {
                pair_key.add_attribute("type", pair.first->get_type(), default_value::value<std::string>());
                pair.first->serialize_json(pair_key);
            }
            if (pair.second)
            {
                value.add_attribute("type", pair.second->get_type(), default_value::value<std::string>());
                pair.second->serialize_json(value);
            }
        }
    }

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
        Pimpl<Json::ValueIterator, 16> _iterator;
    };
public:
    explicit DeserializerJson(Json::Value &json);
    DeserializerJson(const DeserializerJson &rhs);
    DeserializerJson(DeserializerJson &&rhs) noexcept;
    ~DeserializerJson();

    DeserializerJson get_child(const std::string &name);

    int get_attribute(const std::string &key, int default_value = 0);
    bool get_attribute(const std::string &key, bool default_value = false);
    float get_attribute(const std::string &key, float default_value = 0.f);
    std::string get_attribute(const std::string &key, const std::string &default_value);

    void get_array_item(int &value);
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
    typename std::enable_if<is_enum<T>::value, void>::type deserialize(T &value, const std::string &key)
    {
        value = get_attribute(!key.empty() ? key : "value", default_value::value<std::string>());
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type deserialize(const T *&value, const std::string &key)
    {
        value = mg::DataStorage::shared().get<T>(get_attribute(key, default_value::value<std::string>()));
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    deserialize(mg::intrusive_ptr<T> &value, const std::string &key)
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
    typename std::enable_if<is_enum<T>::value, void>::type deserialize(std::vector<T> &values, const std::string &key)
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
    typename std::enable_if<!is_attribute<T>::value, void>::type
    deserialize(std::vector<mg::intrusive_ptr<T>> &values, const std::string &key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            auto type = item.get_attribute(std::string("type"), default_value::value<std::string>());
            auto value = Factory::shared().build<T>(item.get_attribute("type", std::string()));
            if(value)
            {
                value->deserialize_json(item);
            }
            values.push_back(value);
        }
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value && !is_enum<T>::value, void>::type
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

    template<class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value> &values, const std::string &key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            Key key_object;
            key_object = item.get_attribute("key", default_value::value<Key>());
            Value value;
            value = item.get_attribute("value", default_value::value<Value>());
            values[key_object] = value;
        }
    }

    template<class Key, class Value>
    typename std::enable_if<is_enum<Key>::value && is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value> &values, const std::string &key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            DeserializerJson key_json = item.get_child("key");
            std::string value_string;
            key_json.get_array_item(value_string);
            Key key_object(value_string);
            DeserializerJson value_json = item.get_child("value");
            Value value;
            value = item.get_attribute("value", default_value::value<Value>());
            values[key_object] = value;
        }
    }

    template<class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value> &values, const std::string &key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            DeserializerJson value_json = item.get_child("value");
            Key key_object;
            Value value;
            key_object = item.get_attribute("key", default_value::value<Key>());
            value_json.deserialize(value, "");
            values[key_object] = value;
        }
    }

    template<class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, const Value*> &values, const std::string &key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            Key key_object = item.get_attribute("key", default_value::value<Key>());
            const Value* value_object = DataStorage::shared().get<Value>(item.get_attribute("value", default_value::value<std::string>()));
            values[key_object] = value_object;
        }
    }

    template<class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && is_enum<Key>::value && !is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value> &values, const std::string &key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            std::string value_string;
            item.get_array_item(value_string);
            Key key_object(value_string);
            DeserializerJson value_json = item.get_child("value");
            Value value;
            value_json.deserialize(value, "");
            values[key_object] = value;
        }
    }

    template<class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_enum<Key>::value && is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value> &values, const std::string &key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            Key object;
            item.deserialize(object, "key");
            values[object] = get_attribute("value", default_value::value<Value>());
        }
    }

    template<class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_enum<Key>::value && is_attribute<Value>::value, void>::type
    deserialize(std::map<const Key*, Value> &values, const std::string &key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            const Key* object = DataStorage::shared().get<Key>(item.get_attribute("key", default_value::value<std::string>()));
            values[object] = item.get_attribute("value", default_value::value<Value>());
        }
    }

    template<class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value> &values, const std::string &key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            DeserializerJson key_json = item.get_child("key");
            Key key_object;
            key_object.deserialize_json(key_json);

            DeserializerJson value_json = item.get_child("value");
            Value value;
            value.deserialize_json(value_json);

            values[key_object] = value;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    deserialize(std::map<const Key*, const Value*>& values, const std::string& key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            const Value* key_data = DataStorage::shared().get<Key>(item.get_attribute("key", default_value::value<std::string>()));
            const Value* value_data = DataStorage::shared().get<Value>(item.get_attribute("value", default_value::value<std::string>()));
            values[key_data] = value_data;
        }
    }

    template<class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, mg::intrusive_ptr<Value>> &values, const std::string &key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            Key key_object;
            key_object = item.get_attribute("key", default_value::value<Key>());

            DeserializerJson value_json = item.get_child("value");
            auto value = Factory::shared().build<Value>(value_json.get_attribute("type", std::string()));
            if(value)
            {
                value->deserialize_json(value_json);
            }
            values[key_object] = value;
        }
    }

    template<class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, mg::intrusive_ptr<Value>> &values, const std::string &key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            DeserializerJson key_json = item.get_child("key");
            Key key_object;
            key_object.deserialize_json(key_json);

            DeserializerJson value_json = item.get_child("value");
            auto value = Factory::shared().build<Value>(value_json.get_attribute("type", std::string()));
            if(value)
            {
                value->deserialize_json(value_json);
            }
            values[key_object] = value;
        }
    }

    template<class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    deserialize(std::map<mg::intrusive_ptr<Key>, mg::intrusive_ptr<Value>> &values, const std::string &key)
    {
        DeserializerJson child = key.empty() ? *this : get_child(key);
        for (DeserializerJson item : child)
        {
            DeserializerJson key_json = item.get_child("key");
            auto key_object = Factory::shared().build<Key>(key_json.get_attribute("type", std::string()));
            key_object->deserialize_json(key_json);

            DeserializerJson value_json = item.get_child("value");
            auto value = Factory::shared().build<Value>(value_json.get_attribute("type", std::string()));
            if(value)
            {
                value->deserialize_json(value_json);
            }

            values[key_object] = value;
        }
    }

private:
    Json::Value &_json;

};
}
#endif //__mg_SERIALIZERJSON_H__
