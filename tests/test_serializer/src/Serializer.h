//
// Created by Vladimir Tolmachev on 18/02/2020.
//

#ifndef SERIALIZER_SERIALIZER_H
#define SERIALIZER_SERIALIZER_H

#include "Pimpl.hpp"
#include "intrusive_ptr.h"
#include "AllTypesChildren.h"
#include "FooObject.h"
#include <string>
#include <map>
#include <vector>

namespace pugi {
    class xml_node;
    class xml_document;
}

template <class T>
struct is_attribute {
    constexpr static bool value = std::is_same<int, T>::value ||
                                  std::is_same<bool, T>::value ||
                                  std::is_same<float, T>::value ||
                                  std::is_same<std::string, T>::value;

    constexpr bool operator()() {
        return value;
    }
};

struct default_value {

    template<class T> static typename std::enable_if<std::is_same<int, T>::value, int>::type
    value() { return 0; }

    template<class T> static typename std::enable_if<std::is_same<bool, T>::value, bool>::type
    value() { return false; }

    template<class T> static typename std::enable_if<std::is_same<float, T>::value, float>::type
    value() { return 0.f; }

    template<class T> static typename std::enable_if<std::is_same<std::string, T>::value, std::string>::type
    value() { return std::string(); }


};

class Serializer
{
public:
    explicit Serializer(pugi::xml_node node);
    Serializer(const Serializer& rhs);
    Serializer(Serializer&& rhs) noexcept;
    ~Serializer();
    Serializer& operator=(const Serializer& rhs);

    static void log(const pugi::xml_document& document);
    static std::string toStr(const pugi::xml_document &document);

    Serializer add_child(const std::string& name);
    void add_attribute(const std::string& key, const int& value, int default_value=0);
    void add_attribute(const std::string& key, const bool& value, bool default_value=false);
    void add_attribute(const std::string& key, const float& value, float default_value=0.f);
    void add_attribute(const std::string& key, const std::string& value, const std::string& default_value);

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
            Serializer child = key.empty() ? *this : add_child(key);
            child.add_attribute("type", value->get_type(), "");
            value->serialize(child);
        }
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    serialize(const T& value, const std::string& key){
        Serializer child = key.empty() ? *this : add_child(key);
        value.serialize(child);
    }

    template <class T>
    typename std::enable_if<is_attribute<T>::value, void>::type
    serialize(const std::vector<T>& values, const std::string& key) {
        if(values.empty())
            return;
        Serializer child = key.empty() ? *this : add_child(key);
        for(const T& value : values){
            Serializer item = child.add_child("item");
            item.serialize(value, "value", default_value::value<T>());
        }
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    serialize(const std::vector<mg::intrusive_ptr<T>>& values, const std::string& key) {
        if(values.empty())
            return;
        Serializer child = key.empty() ? *this : add_child(key);
        for(const mg::intrusive_ptr<T>& value : values){
            Serializer item = child.add_child(value->get_type());
            value->serialize(item);
        }
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    serialize(const std::vector<T>& values, const std::string& key) {
        if(values.empty())
            return;
        Serializer child = key.empty() ? *this : add_child(key);
        for(const T& value : values){
            Serializer item = child.add_child("item");
            item.serialize(value, "");
        }
    }

    // Map<simple, simple>
    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key) {
        if(values.empty())
            return;
        Serializer child = key.empty() ? *this : add_child(key);
        for(auto& pair : values){
            Serializer item = child.add_child("pair");
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
        Serializer child = key.empty() ? *this : add_child(key);
        for(auto& pair : values){
            Serializer item = child.add_child("pair");
            Serializer value = item.add_child("value");
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
        Serializer child = key.empty() ? *this : add_child(key);
        for(auto& pair : values){
            Serializer item = child.add_child("pair");
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
        Serializer child = key.empty() ? *this : add_child(key);
        for(auto& pair : values){
            Serializer item = child.add_child("pair");
            Serializer pair_key = item.add_child("key");
            Serializer value = item.add_child("value");
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
        Serializer child = key.empty() ? *this : add_child(key);
        for(auto& pair : values){
            Serializer item = child.add_child("pair");
            item.add_attribute("key", pair.first, default_value::value<Key>());
            if(pair.second) {
                Serializer value = item.add_child("value");
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
        Serializer child = key.empty() ? *this : add_child(key);
        for(auto& pair : values){
            Serializer item = child.add_child("pair");
            Serializer pair_key = item.add_child("key");
            pair.first.serialize(pair_key);
            if(pair.second) {
                Serializer value = item.add_child("value");
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
        Serializer child = key.empty() ? *this : add_child(key);
        for(auto& pair : values){
            Serializer item = child.add_child("pair");
            Serializer pair_key = item.add_child("key");
            Serializer value = item.add_child("value");
            if(pair.first)
                pair.first->serialize(pair_key);
            if(pair.second)
                pair.second->serialize(value);
        }
    }

private:
    Pimpl<pugi::xml_node, 8> _node;

};

class Deserializer
{
public:
    explicit Deserializer(pugi::xml_node node);
    Deserializer(const Deserializer& rhs);
    Deserializer(Deserializer&& rhs) noexcept;
    ~Deserializer();
    Deserializer& operator=(const Deserializer& rhs);

    Deserializer get_child(const std::string& name);
    int get_attribute(const std::string& key, int default_value=0);
    bool get_attribute(const std::string& key, bool default_value=false);
    float get_attribute(const std::string& key, float default_value=0.f);
    std::string get_attribute(const std::string& key, const std::string& default_value);

    Deserializer begin();
    Deserializer end();
    bool operator != (const Deserializer& rhs) const;
    Deserializer& operator ++ ();
    Deserializer operator ++ (int) = delete;
    Deserializer operator *();

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
        Deserializer child = key.empty() ? *this : get_child(key);
//        value = mg::Factory::build<T>(child.get_attribute("type", std::string()));
        value = mg::make_intrusive<mg::AllTypesChildren>();
        value->deserialize(child);
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    deserialize(T& value, const std::string& key){
        Deserializer child = key.empty() ? *this : get_child(key);
        value.deserialize(child);
    }

    template <class T>
    typename std::enable_if<is_attribute<T>::value, void>::type
    deserialize(std::vector<T>& values, const std::string& key) {
        Deserializer child = key.empty() ? *this : get_child(key);
        for(auto item : child){
            T value;
            item.deserialize(value, "value", default_value::value<T>());
            values.push_back(value);
        }
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    deserialize(std::vector<mg::intrusive_ptr<T>>& values, const std::string& key) {
        Deserializer child = key.empty() ? *this : get_child(key);
        for(auto item : child){
            auto type = item.get_attribute("type", "");
//            mg::intrusive_ptr<T> object = mg::Factory::build<T>(child.get_attribute("type", std::string()));
            mg::intrusive_ptr<T> object = mg::make_intrusive<T>();
            object->deserialize(item);
            values.push_back(object);
        }
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    deserialize(std::vector<T>& values, const std::string& key) {
        Deserializer child = key.empty() ? *this : get_child(key);
        for(auto item : child){
            T value;
            value.deserialize(item);
            values.push_back(value);
        }
    }

    // Map<simple, simple>
    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& values, const std::string& key) {
        Deserializer child = key.empty() ? *this : get_child(key);
        for(Deserializer item : child){
            values[item.get_attribute("key", default_value::value<Key>())] =
                    item.get_attribute("value", default_value::value<Value>());
        }
    }

    // Map<simple, object>
    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& values, const std::string& key) {
        Deserializer child = key.empty() ? *this : get_child(key);
        for(Deserializer item : child){
            Deserializer value = item.get_child("value");
            Value object;
            object.deserialize(value);
            values[item.get_attribute("key", default_value::value<Key>())] = object;
        }
    }

    // Map<object, simple>
    template <class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& values, const std::string& key) {
        Deserializer child = key.empty() ? *this : get_child(key);
        for(Deserializer item : child){
            Key object;
            object.deserialize(item);
            values[object] = item.get_attribute("value", default_value::value<Value>());
        }
//
//        Deserializer child = key.empty() ? *this : get_child(key);
//        for(auto& pair : values){
//            Deserializer item = child.get_child("pair");
//            item.get_attribute("value", pair.second, default_value::value<Value>());
//            pair.first.deserialize(item);
//        }
    }

    // Map<object, object>
    template <class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& values, const std::string& key) {
        Deserializer child = key.empty() ? *this : get_child(key);
        for(auto& pair : values){
            Deserializer item = child.get_child("pair");
            Deserializer pair_key = item.get_child("key");
            Deserializer value = item.get_child("value");
            pair.first.deserialize(pair_key);
            pair.second.deserialize(value);
        }
    }

    // Map<simple, pointer object>
    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, mg::intrusive_ptr<Value>>& values, const std::string& key) {
        Deserializer child = key.empty() ? *this : get_child(key);
        for(auto item : child){
            Key map_key = item.get_attribute("key", default_value::value<Key>());
//            mg::intrusive_ptr<Value> object = mg::Factory::build<Value>(pair.get_attribute("type", std::string()));
            mg::intrusive_ptr<Value> object = mg::make_intrusive<mg::AllTypesChildren>();
            Deserializer value = item.get_child("value");
            object->deserialize(value);
            values[map_key] = object;
        }
    }

    // Map<object, pointer object>
    template <class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, mg::intrusive_ptr<Value>>& values, const std::string& key) {
        Deserializer child = key.empty() ? *this : get_child(key);
        for(Deserializer pair : child){
            Deserializer pair_key = pair.get_child("key");
            Deserializer pair_value = pair.get_child("value");
            Key key_object;
            key_object.deserialize(pair_key);
//            mg::intrusive_ptr<Value> object = mg::Factory::build<Value>(pair.get_attribute("type", std::string()));
            mg::intrusive_ptr<Value> value_object = mg::make_intrusive<Value>();
            value_object->deserialize(pair_value);
            values[key_object] = value_object;
        }
    }

    // Map<pointer object, pointer object>
    template <class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    deserialize(std::map<mg::intrusive_ptr<Key>, mg::intrusive_ptr<Value>>& values, const std::string& key) {
        Deserializer child = key.empty() ? *this : get_child(key);
        for(Deserializer pair : child){
            Deserializer pair_key = pair.get_child("key");
            Deserializer pair_value = pair.get_child("value");
//            mg::intrusive_ptr<Value> key_object = mg::Factory::build<Value>(pair_key.get_attribute("type", std::string()));
            mg::intrusive_ptr<Key> key_object = mg::make_intrusive<Key>();
            key_object->deserialize(pair_key);
//            mg::intrusive_ptr<Value> value_object = mg::Factory::build<Value>(pair_value.get_attribute("type", std::string()));
            mg::intrusive_ptr<Value> value_object = mg::make_intrusive<Value>();
            value_object->deserialize(pair_value);
            values[key_object] = value_object;
        }
    }

private:
    Pimpl<pugi::xml_node, 8> _node;

};


#endif //SERIALIZER_SERIALIZER_H
