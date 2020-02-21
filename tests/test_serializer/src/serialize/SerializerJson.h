//
// Created by Vladimir Tolmachev on 2020-02-21.
//

#ifndef SERIALIZER_SERIALIZERJSON_H
#define SERIALIZER_SERIALIZERJSON_H

#include <string>
#include <map>
#include <vector>
#include "../intrusive_ptr.h"
#include "Pimpl.hpp"
#include "SerializerCommon.h"

namespace Json{
    class Value;
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
//        SerializerJson child = key.empty() ? *this : add_array(key);
//        for(const mg::intrusive_ptr<T>& value : values){
//            SerializerJson item = child.add_child(value->get_type());
//            value->serialize(item);
//        }
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
//        SerializerJson child = key.empty() ? *this : add_array(key);
//        for(const T& value : values){
//            SerializerJson item = child.add_child("item");
//            item.serialize(value, "");
//        }
    }

    // Map<simple, simple>
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

    // Map<simple, object>
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

    // Map<object, simple>
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

    // Map<object, object>
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

    // Map<simple, pointer object>
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

    // Map<object, pointer object>
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

    // Map<pointer object, pointer object>
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
//    Pimpl<Json::Value, 40> _json;
    Json::Value& _json;
};


#endif //SERIALIZER_SERIALIZERJSON_H
