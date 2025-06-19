SERIALIZER_BINARY_HPP = '''#ifndef __mg_SerializerBinary_H__
#define __mg_SerializerBinary_H__

#include <string>
#include <map>
#include <vector>
#include "intrusive_ptr.h"
#include "SerializerCommon.h"
#include "DataStorage.h"
#include "mg_Factory.h"
#include "binary/binary.h"

namespace mg
{


class SerializerBinary
{

public:
    explicit SerializerBinary(BinaryFormat& chunk);
    SerializerBinary(const SerializerBinary& rhs);
    SerializerBinary(SerializerBinary&& rhs) noexcept;
    ~SerializerBinary();
    SerializerBinary& operator=(const SerializerBinary& rhs) = delete;

    SerializerBinary add_child(const std::string& name);
    SerializerBinary add_array(const std::string& name);

    void add_attribute(const std::string& key, const int& value, int default_value = 0);
    void add_attribute(const std::string& key, const int64_t& value, int64_t default_value = 0);
    void add_attribute(const std::string& key, const unsigned int& value, unsigned int default_value = 0);
    void add_attribute(const std::string& key, const uint64_t& value, uint64_t default_value = 0);
    void add_attribute(const std::string& key, const bool& value, bool default_value = false);
    void add_attribute(const std::string& key, const float& value, float default_value = 0.f);
    void add_attribute(const std::string& key, const double& value, double default_value = 0.f);
    void add_attribute(const std::string& key, const std::string& value, const std::string& default_value);
    
    void add_array(const std::vector<int32_t>&      vector);
    void add_array(const std::vector<int64_t>&      vector);
    void add_array(const std::vector<uint32_t>&     vector);
    void add_array(const std::vector<uint64_t>&     vector);
    void add_array(const std::vector<bool>&         vector);
    void add_array(const std::vector<float>&        vector);
    void add_array(const std::vector<double>&       vector);
    void add_array(const std::vector<std::string>&  vector);
    void add_array(const std::vector<BaseEnum>&      vector);

    template <class T>
    typename std::enable_if<is_enum<T>::value, void>::type
    add_array_item(const T& value)
    {
        add_array_item(value.str());
    }

    template<class T>
    typename std::enable_if<is_attribute<T>::value, void>::type
    serialize(const T& value, const std::string& key, const T& default_value=default_value::value<T>())
    {
        add_attribute(key, value, default_value);
    }

    template<class T>
    typename std::enable_if<is_enum<T>::value, void>::type
    serialize(const T& value, const std::string& key)
    {
        add_attribute(key, value);
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    serialize(const T *value, const std::string& key)
    {
        if (value)
        {
            add_attribute(key, value->name, default_value::value<std::string>());
        }
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    serialize(const intrusive_ptr<T>& value, const std::string& key)
    {
        if (value)
        {
            SerializerBinary child = key.empty() ? *this : add_child(key);
            child.add_attribute("type", value->get_type(), "");
            value->serialize_binary(child);
        }
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value && !is_enum<T>::value, void>::type
    serialize(const T& value, const std::string& key)
    {
        SerializerBinary child = key.empty() ? *this : add_child(key);
        value.serialize_binary(child);
    }
/* Vectors serialization start */
    template<class T>
    typename std::enable_if<is_attribute<T>::value, void>::type
    serialize(const std::vector<T>& values, const std::string& key)
    {
        _binary.add_array(key, values);
    }
    template<class T>
    typename std::enable_if<is_enum<T>::value, void>::type
    serialize(const std::vector<T>& values, const std::string& key)
    {
        std::vector<int32_t> temp;
        temp.reserve(values.size());
        for(auto value : values)
            temp.push_back((int)value);
        _binary.add_array(key, temp);
    }

    template<class T>
    typename std::enable_if<is_data<T>::value, void>::type
    serialize(const std::vector<T>& values, const std::string& key)
    {
        std::vector<std::string> temp;
        temp.reserve(values.size());
        for(auto value : values)
            temp.push_back(value ? value->name : "");
        _binary.add_array(key, temp);
    }
    
    template<class T>
    typename std::enable_if<is_not_serialize_to_attribute<T>::value, void>::type
    serialize(const std::vector<T>& values, const std::string& key)
    {
        // вектор сериализируемых объектов
        SerializerBinary child = key.empty() ? *this : add_child(key);
        for (const T &value : values)
        {
            SerializerBinary item = child.add_child("");
            item.serialize(value, "");
        }
    }
/* Vectors serialization finish */
/* Maps serialization start */
    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        _binary.add_map(key, values);
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_enum<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        _binary.add_map(key, values);
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_data<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerBinary child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerBinary item(child.add_child(""));
            item.serialize(pair.first, "key");
            item.serialize(pair.second, "value");
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_not_serialize_to_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
                    return;
        SerializerBinary child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerBinary item = child.add_child("");
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
        SerializerBinary child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerBinary item(child.add_child(""));
            item.add_attribute("key", (int32_t)pair.first, default_value::value<int32_t>());
            item.add_attribute("value", pair.second, default_value::value<Value>());
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_enum<Key>::value && is_enum<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerBinary child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerBinary item(child.add_child(""));
            item.serialize(pair.first, "key");
            item.serialize(pair.second, "value");
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_enum<Key>::value && is_data<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerBinary child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerBinary item(child.add_child(""));
            item.serialize(pair.first, "key");
            item.serialize(pair.second, "value");
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_enum<Key>::value && is_not_serialize_to_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerBinary child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerBinary item(child.add_child(""));
            item.serialize(pair.first, "key");
            item.serialize(pair.second, "value");
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_data<Key>::value && is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerBinary child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerBinary item(child.add_child(""));
            item.serialize(pair.first, "key");
            item.serialize(pair.second, "value");
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_data<Key>::value && is_enum<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerBinary child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerBinary item(child.add_child(""));
            item.serialize(pair.first, "key");
            item.serialize(pair.second, "value");
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_data<Key>::value && is_data<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerBinary child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerBinary item(child.add_child(""));
            item.serialize(pair.first, "key");
            item.serialize(pair.second, "value");
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_data<Key>::value && is_not_serialize_to_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerBinary child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerBinary item(child.add_child(""));
            item.serialize(pair.first, "key");
            item.serialize(pair.second, "value");
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_not_serialize_to_attribute<Key>::value && is_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerBinary child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerBinary item(child.add_child(""));
            item.serialize(pair.first, "key");
            item.serialize(pair.second, "value");
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_not_serialize_to_attribute<Key>::value && is_enum<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerBinary child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerBinary item(child.add_child(""));
            item.serialize(pair.first, "key");
            item.serialize(pair.second, "value");
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_not_serialize_to_attribute<Key>::value && is_data<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerBinary child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerBinary item(child.add_child(""));
            item.serialize(pair.first, "key");
            item.serialize(pair.second, "value");
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_not_serialize_to_attribute<Key>::value && is_not_serialize_to_attribute<Value>::value, void>::type
    serialize(const std::map<Key, Value>& values, const std::string& key)
    {
        if (values.empty())
            return;
        SerializerBinary child = key.empty() ? *this : add_child(key);
        for (auto& pair : values)
        {
            SerializerBinary item(child.add_child(""));
            item.serialize(pair.first, "key");
            item.serialize(pair.second, "value");
        }
    }
/* Maps serialization finish */

private:
    BinaryFormat& _binary;
};

class DeserializerBinary
{
public:
    explicit DeserializerBinary(BinaryFormat& chunk);
    DeserializerBinary(const DeserializerBinary& rhs);
    DeserializerBinary(DeserializerBinary&& rhs) noexcept;
    ~DeserializerBinary();

    DeserializerBinary get_child(const std::string& name);

    int get_attribute(const std::string& key, int default_value = 0);
    int64_t get_attribute(const std::string& key, int64_t default_value = 0);
    unsigned int get_attribute(const std::string& key, unsigned int default_value = 0);
    uint64_t get_attribute(const std::string& key, uint64_t default_value = 0);
    bool get_attribute(const std::string& key, bool default_value = false);
    float get_attribute(const std::string& key, float default_value = 0.f);
    double get_attribute(const std::string& key, double default_value = 0.f);
    std::string get_attribute(const std::string& key, const std::string& default_value);
    
    void get_array(const std::vector<int32_t>&      vector);
    void get_array(const std::vector<int64_t>&      vector);
    void get_array(const std::vector<uint32_t>&     vector);
    void get_array(const std::vector<uint64_t>&     vector);
    void get_array(const std::vector<bool>&         vector);
    void get_array(const std::vector<float>&        vector);
    void get_array(const std::vector<double>&       vector);
    void get_array(const std::vector<std::string>&  vector);

    template<class T>
    typename std::enable_if<is_attribute<T>::value, void>::type
    deserialize(T& value, const std::string& key, const T& default_value=default_value::value<T>())
    {
        value = get_attribute(key, default_value);
    }

    template<class T>
    typename std::enable_if<is_enum<T>::value, void>::type
    deserialize(T& value, const std::string& key)
    {
        value = get_attribute(!key.empty() ? key : "value", default_value::value<std::string>());
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    deserialize(const T *&value, const std::string& key)
    {
        value = DataStorage::shared().get<T>(get_attribute(key, default_value::value<std::string>()));
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value, void>::type
    deserialize(intrusive_ptr<T>& value, const std::string& key)
    {
        DeserializerBinary child = key.empty() ? *this : get_child(key);
        auto type = child.get_attribute("type", std::string());
        if(!type.empty())
        {
            value = Factory::shared().build<T>(type);
            if(value)
            {
                value->deserialize_binary(child);
            }
        }
    }

    template<class T>
    typename std::enable_if<!is_attribute<T>::value && !is_enum<T>::value, void>::type
    deserialize(T& value, const std::string& key)
    {
        DeserializerBinary child = key.empty() ? *this : get_child(key);
        value.deserialize_binary(child);
    }

/* Vectors deserialization start */
    template<class T>
    typename std::enable_if<is_attribute<T>::value, void>::type
    deserialize(std::vector<T>& values, const std::string& key)
    {
        values = _binary.get_array<T>(key);
    }

    template<class T>
    typename std::enable_if<is_enum<T>::value, void>::type
    deserialize(std::vector<T>& values, const std::string& key)
    {
        std::vector<int32_t> temp;
        deserialize(temp, key);
        values.clear();
        values.reserve(temp.size());
        for(auto value : temp)
        {
            values.emplace_back(value);
        }
    }

    template<class T>
    typename std::enable_if<is_data<T>::value, void>::type
    deserialize(std::vector<T>& values, const std::string& key)
    {
        std::vector<std::string> temp;
        deserialize(temp, key);
        values.clear();
        values.reserve(temp.size());
        for(auto value : temp)
        {
            T data = DataStorage::shared().get<typename data_type<T>::type>(value);
            values.push_back(data);
        }
    }

    template<class T>
    typename std::enable_if<is_not_serialize_to_attribute<T>::value, void>::type
    deserialize(std::vector<T>& values, const std::string& key)
    {
        DeserializerBinary child = key.empty() ? *this : get_child(key);
        for (BinaryFormat& item : child._binary.get_children())
        {
            DeserializerBinary inner(item);
            T value;
            inner.deserialize(value, "");
            values.push_back(value);
        }
    }
/* Vectors deserialization finish */
/* Maps deserialization start */
    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        map = _binary.get_map<Key, Value>(key);
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_enum<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerBinary child = key.empty() ? *this : get_child(key);
        for (BinaryFormat& item : child._binary.get_children())
        {
            DeserializerBinary inner(item);
            Key key_; inner.deserialize(key_, "key");
            Value value_; inner.deserialize(value_, "value");
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_data<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerBinary child = key.empty() ? *this : get_child(key);
        for (BinaryFormat& item : child._binary.get_children())
        {
            DeserializerBinary inner(item);
            Key key_; inner.deserialize(key_, "key");
            Value value_; inner.deserialize(value_, "value");
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_attribute<Key>::value && is_not_serialize_to_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerBinary child = key.empty() ? *this : get_child(key);
        for (BinaryFormat& item : child._binary.get_children())
        {
            DeserializerBinary inner(item);
            Key key_ = inner.get_attribute("key", default_value::value<Key>());
            Value value_;
            inner.deserialize(value_, "value");
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_enum<Key>::value && is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerBinary child = key.empty() ? *this : get_child(key);
        for (BinaryFormat& item : child._binary.get_children())
        {
            DeserializerBinary inner(item);
            int32_t key_ = inner.get_attribute("key", default_value::value<int32_t>());
            Value value_ = inner.get_attribute("value", default_value::value<Value>());
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_enum<Key>::value && is_enum<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerBinary child = key.empty() ? *this : get_child(key);
        for (BinaryFormat& item : child._binary.get_children())
        {
            DeserializerBinary inner(item);
            Key key_; inner.deserialize(key_, "key");
            Value value_; inner.deserialize(value_, "value");
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_enum<Key>::value && is_data<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerBinary child = key.empty() ? *this : get_child(key);
        for (BinaryFormat& item : child._binary.get_children())
        {
            DeserializerBinary inner(item);
            Key key_; inner.deserialize(key_, "key");
            Value value_; inner.deserialize(value_, "value");
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_enum<Key>::value && is_not_serialize_to_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerBinary child = key.empty() ? *this : get_child(key);
        for (BinaryFormat& item : child._binary.get_children())
        {
            DeserializerBinary inner(item);
            Key key_; inner.deserialize(key_, "key");
            Value value_; inner.deserialize(value_, "value");
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_data<Key>::value && is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerBinary child = key.empty() ? *this : get_child(key);
        for (BinaryFormat& item : child._binary.get_children())
        {
            DeserializerBinary inner(item);
            Key key_; inner.deserialize(key_, "key");
            Value value_; inner.deserialize(value_, "value");
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_data<Key>::value && is_enum<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerBinary child = key.empty() ? *this : get_child(key);
        for (BinaryFormat& item : child._binary.get_children())
        {
            DeserializerBinary inner(item);
            Key key_; inner.deserialize(key_, "key");
            Value value_; inner.deserialize(value_, "value");
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_data<Key>::value && is_data<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerBinary child = key.empty() ? *this : get_child(key);
        for (BinaryFormat& item : child._binary.get_children())
        {
            DeserializerBinary inner(item);
            Key key_; inner.deserialize(key_, "key");
            Value value_; inner.deserialize(value_, "value");
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_data<Key>::value && is_not_serialize_to_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerBinary child = key.empty() ? *this : get_child(key);
        for (BinaryFormat& item : child._binary.get_children())
        {
            DeserializerBinary inner(item);
            Key key_; inner.deserialize(key_, "key");
            Value value_; inner.deserialize(value_, "value");
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_not_serialize_to_attribute<Key>::value && is_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerBinary child = key.empty() ? *this : get_child(key);
        for (BinaryFormat& item : child._binary.get_children())
        {
            DeserializerBinary inner(item);
            Key key_; inner.deserialize(key_, "key");
            Value value_; inner.deserialize(value_, "value");
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_not_serialize_to_attribute<Key>::value && is_enum<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerBinary child = key.empty() ? *this : get_child(key);
        for (BinaryFormat& item : child._binary.get_children())
        {
            DeserializerBinary inner(item);
            Key key_; inner.deserialize(key_, "key");
            Value value_; inner.deserialize(value_, "value");
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_not_serialize_to_attribute<Key>::value && is_data<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerBinary child = key.empty() ? *this : get_child(key);
        for (BinaryFormat& item : child._binary.get_children())
        {
            DeserializerBinary inner(item);
            Key key_; inner.deserialize(key_, "key");
            Value value_; inner.deserialize(value_, "value");
            map[key_] = value_;
        }
    }

    template <class Key, class Value>
    typename std::enable_if<is_not_serialize_to_attribute<Key>::value && is_not_serialize_to_attribute<Value>::value, void>::type
    deserialize(std::map<Key, Value>& map, const std::string& key)
    {
        DeserializerBinary child = key.empty() ? *this : get_child(key);
        for (BinaryFormat& item : child._binary.get_children())
        {
            DeserializerBinary inner(item);
            Key key_; inner.deserialize(key_, "key");
            Value value_; inner.deserialize(value_, "value");
            map[key_] = value_;
        }
    }
/* Maps deserialization finish */

private:
    BinaryFormat& _binary;

};
}
#endif //__mg_SerializerBinary_H__

'''
SERIALIZER_BINARY_CPP = '''
#include "SerializerBinary.h"
#include "binary/binary.h"

namespace mg
{

SerializerBinary::SerializerBinary(BinaryFormat &chunk) : _binary(chunk)
{
}

SerializerBinary::SerializerBinary(const SerializerBinary &rhs) = default;


SerializerBinary::~SerializerBinary() = default;

SerializerBinary::SerializerBinary(SerializerBinary &&rhs) noexcept = default;


SerializerBinary SerializerBinary::add_child(const std::string &name)
{
    return SerializerBinary(_binary.add_node(name));
}

void SerializerBinary::add_attribute(const std::string &key, const int &value, int default_value)
{
    _binary.add(key, value);
}

void SerializerBinary::add_attribute(const std::string &key, const int64_t &value, int64_t default_value)
{
    _binary.add(key, value);
}

void SerializerBinary::add_attribute(const std::string &key, const unsigned int &value, unsigned int default_value)
{
    _binary.add(key, value);
}

void SerializerBinary::add_attribute(const std::string &key, const uint64_t &value, uint64_t default_value)
{
    _binary.add(key, value);
}

void SerializerBinary::add_attribute(const std::string &key, const bool &value, bool default_value)
{
    _binary.add(key, value);
}

void SerializerBinary::add_attribute(const std::string &key, const float &value, float default_value)
{
    _binary.add(key, value);
}

void SerializerBinary::add_attribute(const std::string &key, const double &value, double default_value)
{
    _binary.add(key, value);
}

void SerializerBinary::add_attribute(const std::string &key, const std::string &value, const std::string &default_value)
{
    _binary.add(key, value);
}

DeserializerBinary::DeserializerBinary(BinaryFormat &chunk) : _binary(chunk)
{
    
}

DeserializerBinary::DeserializerBinary(const DeserializerBinary &rhs) : _binary(rhs._binary)
{
    
}

DeserializerBinary::DeserializerBinary(DeserializerBinary &&rhs) noexcept = default;

DeserializerBinary::~DeserializerBinary() = default;

DeserializerBinary DeserializerBinary::get_child(const std::string &name)
{
    return DeserializerBinary(_binary.get_node(name));
}

int DeserializerBinary::get_attribute(const std::string &key, int default_value)
{
    return _binary.get_int(key, default_value);
}

int64_t DeserializerBinary::get_attribute(const std::string &key, int64_t default_value)
{
    return _binary.get_int64(key, default_value);
}

unsigned int DeserializerBinary::get_attribute(const std::string &key, unsigned int default_value)
{
    return _binary.get_unsigned(key, default_value);
}

uint64_t DeserializerBinary::get_attribute(const std::string &key, uint64_t default_value)
{
    return _binary.get_unsigned64(key, default_value);
}

bool DeserializerBinary::get_attribute(const std::string &key, bool default_value)
{
    return _binary.get_bool(key, default_value);
}

float DeserializerBinary::get_attribute(const std::string &key, float default_value)
{
    return _binary.get_float(key, default_value);
}

double DeserializerBinary::get_attribute(const std::string &key, double default_value)
{
    return _binary.get_double(key, default_value);
}

std::string DeserializerBinary::get_attribute(const std::string &key, const std::string &default_value)
{
    return _binary.get_string(key, default_value);
}
}

'''