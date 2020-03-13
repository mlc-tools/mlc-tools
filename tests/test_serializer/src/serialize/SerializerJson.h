//
// Created by Vladimir Tolmachev on 2020-02-21.
//

#ifndef __mg_SERIALIZERJSON_H__
#define __mg_SERIALIZERJSON_H__

#include <string>
#include <map>
#include <vector>
#include "Pimpl.hpp"
#include "../intrusive_ptr.h"
#include "SerializerCommon.h"

namespace Json{
    class Value;
    class ValueIterator;
}

class SerializerJson {

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
            value.serialize(pair.second, "");
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
//        value = mg::DataStorage::shared().get<T>(get_attribute(key, default_value::value<std::string>()));
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    deserialize(mg::intrusive_ptr<T>& value, const std::string& key){
        DeserializerJson child = key.empty() ? *this : get_child(key);
        std::string type = child.get_attribute(std::string("type"), default_value::value<std::string>());
//        value = mg::Factory::build<T>(child.get_attribute("type", std::string()));
        value = mg::make_intrusive<T>();
        value->deserialize(child);
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    deserialize(T& value, const std::string& key){
        DeserializerJson child = key.empty() ? *this : get_child(key);
//        child.deserialize(value, default_value::value<std::string>());
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
//            auto value = mg::Factory::build<T>(child.get_attribute("type", std::string()));
            auto value = mg::make_intrusive<T>();
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
            value_json.deserialize(value, "");
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
//            auto value = mg::Factory::build<T>(value_json.get_attribute("type", std::string()));
            auto value = mg::make_intrusive<Value>();
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
//            auto value = mg::Factory::build<T>(value_json.get_attribute("type", std::string()));
            auto value = mg::make_intrusive<Value>();
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
//            auto value = mg::Factory::build<T>(value_json.get_attribute("type", std::string()));
            auto key_object = mg::make_intrusive<Value>();
            key_object->deserialize(key_json);

            DeserializerJson value_json = item.get_child("value");
//            auto value = mg::Factory::build<T>(value_json.get_attribute("type", std::string()));
            auto value = mg::make_intrusive<Value>();
            value->deserialize(value_json);

            values[key_object] = value;
        }
    }

private:
    Json::Value& _json;

};

#endif //__mg_SERIALIZERJSON_H__
