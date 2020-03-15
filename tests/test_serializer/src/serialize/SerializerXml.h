//
// Created by Vladimir Tolmachev on 18/02/2020.
//

#ifndef __mg_SERIALIZERXML_H__
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
    typename std::enable_if<is_enum<T>::value, void>::type serialize(const T& value, const std::string& key)
    {
        add_attribute(key.empty() ? std::string("value") : key, value.str(), default_value::value<std::string>());
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type serialize(const T *value, const std::string& key)
    {
        if (value)
        {
            add_attribute(key, value->name, default_value::value<std::string>());
        }
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value && !is_enum<T>::value, void>::type
    serialize(const mg::intrusive_ptr<T>& value, const std::string& key)
    {
        if (value)
        {
            SerializerXml child = key.empty() ? *this : add_child(key);
            child.add_attribute("type", value->get_type(), "");
            value->serialize_xml(child);
        }
    }

    template <class T>
    typename std::enable_if<is_object<T>::value, void>::type serialize(const T& value, const std::string& key)
    {
        SerializerXml child = key.empty() ? *this : add_child(key);
        value.serialize_xml(child);
    }

    template <class T>
    typename std::enable_if<is_attribute<T>::value, void>::type
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
    typename std::enable_if<!is_attribute<T>::value, void>::type
    serialize(const std::vector<mg::intrusive_ptr<T>>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for (const mg::intrusive_ptr<T>& value : values)
        {
            SerializerXml item = child.add_child(value->get_type());
            value->serialize_xml(item);
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
    typename std::enable_if<is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerXml item = child.add_child("pair");
            SerializerXml value = item.add_child("value");
            item.add_attribute("key", pair.first, default_value::value<Key>());
            value.serialize(pair.second, "");
        }
    }

    template <class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && is_attribute<Value>::value, void>::type
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
    typename std::enable_if<!is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
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
        if (values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerXml item = child.add_child("pair");
            item.add_attribute("key", pair.first, default_value::value<Key>());
            if (pair.second)
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
        if (values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerXml item = child.add_child("pair");
            SerializerXml pair_key = item.add_child("key");
            pair.first.serialize_xml(pair_key);
            if (pair.second)
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
        if (values.empty())
            return;
        SerializerXml child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerXml item = child.add_child("pair");
            SerializerXml pair_key = item.add_child("key");
            SerializerXml value = item.add_child("value");
            if (pair.first)
            {
                pair_key.add_attribute("type", pair.first->get_type(), default_value::value<std::string>());
                pair.first->serialize_xml(pair_key);
            }
            if (pair.second)
            {
                value.add_attribute("type", pair.second->get_type(), default_value::value<std::string>());
                pair.second->serialize_xml(value);
            }
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
    typename std::enable_if<is_enum<T>::value, void>::type deserialize(T& value, const std::string& key)
    {
        value = get_attribute(!key.empty() ? key : "value", default_value::value<std::string>());
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type deserialize(const T *&value, const std::string& key)
    {
        value = mg::DataStorage::shared().get<T>(get_attribute(key, default_value::value<std::string>()));
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    deserialize(mg::intrusive_ptr<T>& value, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        value = Factory::shared().build<T>(child.get_attribute("type", std::string()));
        value->deserialize_xml(child);
    }

    template <class T>
    typename std::enable_if<!is_attribute<T>::value && !is_enum<T>::value, void>::type
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
        for (auto item : child)
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
        for (auto item : child)
        {
            mg::intrusive_ptr<T> object = mg::make_intrusive<T>();
            object->deserialize_xml(item);
            values.push_back(object);
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

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& values, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for (DeserializerXml item : child)
        {
            values[item.get_attribute("key", default_value::value<Key>())] = item.get_attribute("value",
                                                                                                default_value::value<Value>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& values, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for (DeserializerXml item : child)
        {
            DeserializerXml value = item.get_child("value");
            Value object;
            value.deserialize(object, "");
            values[item.get_attribute("key", default_value::value<Key>())] = object;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_enum<Key>::value && is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& values, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for (DeserializerXml item : child)
        {
            Key object;
            item.deserialize(object, "key");
            values[object] = item.get_attribute("value", default_value::value<Value>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_enum<Key>::value && is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& values, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for (DeserializerXml item : child)
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
        for (auto pair : child)
        {
            DeserializerXml pair_key = pair.get_child("key");
            DeserializerXml value = pair.get_child("value");
            Key key_object;
            Value value_object;
            key_object.deserialize_xml(pair_key);
            value_object.deserialize_xml(value);
            values[key_object] = value_object;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, mg::intrusive_ptr<Value>>& values, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for (auto item : child)
        {
            Key map_key = item.get_attribute("key", default_value::value<Key>());
            DeserializerXml value = item.get_child("value");
            mg::intrusive_ptr<Value> object = Factory::shared().build<Value>(value.get_attribute("type", std::string()));
            if(object)
            {
                object->deserialize_xml(value);
            }
            values[map_key] = object;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, mg::intrusive_ptr<Value>>& values, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for (DeserializerXml pair : child)
        {
            DeserializerXml pair_key = pair.get_child("key");
            DeserializerXml pair_value = pair.get_child("value");
            Key key_object;
            key_object.deserialize_xml(pair_key);
            mg::intrusive_ptr<Value> value_object = Factory::shared().build<Value>(pair_value.get_attribute("type", std::string()));
            if(value_object)
            {
                value_object->deserialize_xml(pair_value);
            }
            values[key_object] = value_object;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<!is_attribute<Key>::value && !is_attribute<Value>::value, void>::type
    deserialize(std::map<mg::intrusive_ptr<Key>, mg::intrusive_ptr<Value>>& values, const std::string& key)
    {
        DeserializerXml child = key.empty() ? *this : get_child(key);
        for (DeserializerXml pair : child)
        {
            DeserializerXml pair_key = pair.get_child("key");
            DeserializerXml pair_value = pair.get_child("value");
            mg::intrusive_ptr<Value> key_object = Factory::shared().build<Key>(pair_key.get_attribute("type", std::string()));
            if(key_object)
            {
                key_object->deserialize_xml(pair_key);
            }
            mg::intrusive_ptr<Value> value_object = Factory::shared().build<Value>(pair_value.get_attribute("type", std::string()));
            if(value_object)
            {
                value_object->deserialize_xml(pair_value);
            }
            values[key_object] = value_object;
        }
    }

private:
    Pimpl<pugi::xml_node, 8> _node;

};

}
#endif //__mg_SERIALIZERXML_H__
