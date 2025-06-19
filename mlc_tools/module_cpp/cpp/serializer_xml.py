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