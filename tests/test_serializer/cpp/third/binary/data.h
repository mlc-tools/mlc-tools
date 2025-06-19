//
//  BinaryFormat.hpp
//  Serializer
//
//  Created by Vladimir Tolmachev on 17.06.2025.
//

#ifndef binary_data_h
#define binary_data_h

#include <stdio.h>
#include <string>
#include <vector>
#include <map>
#include <type_traits>
#include <memory>
#include "SerializerCommon.h"

namespace mg{

template<class T>
struct is_simple
{
    constexpr static bool value = (std::is_same<int32_t, T>::value ||
                                   std::is_same<uint32_t, T>::value ||
                                   std::is_same<int64_t, T>::value ||
                                   std::is_same<uint64_t, T>::value ||
                                   std::is_same<char, T>::value ||
                                   std::is_same<bool, T>::value ||
                                   std::is_same<float, T>::value ||
                                   std::is_same<double, T>::value) && (!std::is_same<const char*, T>::value);
    constexpr bool operator()() { return value; }
};

template<class T>
struct is_string
{
    constexpr static bool value = (std::is_same<std::string, T>::value || std::is_same<const char*, T>::value);
    constexpr bool operator()() { return value; }
};
template<class T>
struct is_bool
{
    constexpr static bool value = (std::is_same<bool, T>::value);
    constexpr bool operator()() { return value; }
};
template<class T>
struct is_vector : std::false_type {};

template<class T, class A>
struct is_vector<std::vector<T,A>> : std::true_type {
    using value_type = T;
};

template<class T>
struct is_map : std::false_type {};

template<class K, class V, class C, class A>
struct is_map<std::map<K,V,C,A>> : std::true_type {
    using key_type   = K;
    using mapped_type = V;
};

static_assert(!is_simple<const char*>::value, "const char* is string");
static_assert(is_string<const char*>::value, "const char* is string");

class Data
{
public:
    enum class data_type : int32_t
    {
        t_int32,
        t_uint32,
        t_int64,
        t_uint64,
        t_bool,
        t_float,
        t_double,
        t_string,
        t_char,
        t_vector,
        t_map,
    };
    
    template <class T> static typename std::enable_if<std::is_same<T, char>::value, const data_type>::type get_data_type(){ return data_type::t_char; }
    template <class T> static typename std::enable_if<std::is_same<T, int32_t>::value, const data_type>::type get_data_type(){ return data_type::t_int32; }
    template <class T> static typename std::enable_if<std::is_same<T, uint32_t>::value, const data_type>::type get_data_type(){ return data_type::t_uint32; }
    template <class T> static typename std::enable_if<std::is_same<T, int64_t>::value, const data_type>::type get_data_type(){ return data_type::t_int64; }
    template <class T> static typename std::enable_if<std::is_same<T, uint64_t>::value, const data_type>::type get_data_type(){ return data_type::t_uint64; }
    template <class T> static typename std::enable_if<std::is_same<T, bool>::value, const data_type>::type get_data_type(){ return data_type::t_bool; }
    template <class T> static typename std::enable_if<std::is_same<T, float>::value, const data_type>::type get_data_type(){ return data_type::t_float; }
    template <class T> static typename std::enable_if<std::is_same<T, double>::value, const data_type>::type get_data_type(){ return data_type::t_double; }
    template <class T> static typename std::enable_if<std::is_same<T, std::string>::value, const data_type>::type get_data_type(){ return data_type::t_string; }
    template <class T> static typename std::enable_if<is_vector<T>::value, const data_type>::type get_data_type(){ return data_type::t_vector; }
    template <class T> static typename std::enable_if<is_map<T>::value, const data_type>::type get_data_type(){ return data_type::t_map; }
public:
    Data();
    Data(Data&& data);
    Data(const Data& data);
    Data(const std::vector<unsigned char>& blob);
    Data& operator=(const Data& data);
    
    void set_data(const std::vector<unsigned char>& data);
    std::vector<unsigned char> get_data() const;
    
    void set_offset(size_t offset) const;
    
    data_type read_type(size_t offset) const;

    template <class T>
    typename std::enable_if<is_simple<T>::value, size_t>::type
    write(T value)
    {
        auto s = _data.size();
        auto append = sizeof(T) + sizeof(data_type);
        _data.resize(s + append);
        auto type = get_data_type<T>();
        memcpy(&_data.at(s + 0), &type, sizeof(data_type));
        memcpy(&_data.at(s + sizeof(data_type)), &value, append);
        return append;
    }
    template <class T>
    typename std::enable_if<is_simple<T>::value, T>::type
    read() const
    {
        T result;
        auto size = sizeof(result);
        assert(_iter_read + size + sizeof(data_type) <= _data.size());
        
        const data_type type_request = get_data_type<T>();
        data_type type_read;
        memcpy(&type_read, &_data.at(_iter_read + 0), sizeof(data_type));
        memcpy(&result, &_data.at(_iter_read + sizeof(data_type)), size);
        assert(type_read == type_request);
        
        _iter_read += size + sizeof(data_type);
        return result;
    }
    
    /* BaseEnum */
    template <class T>
    typename std::enable_if<is_enum<T>::value, size_t>::type
    write(T value)
    {
        return write<int32_t>(value);
    }
    template <class T>
    typename std::enable_if<is_enum<T>::value, T>::type
    read() const
    {
        return read<int32_t>();
    }
    
    template <class T>
    typename std::enable_if<is_string<T>::value, size_t>::type
    write(T value)
    {
        auto type = get_data_type<T>();
        auto s = _data.size();
        auto value_size = value.size();
        
        _data.resize(s + sizeof(data_type) + sizeof(int64_t));
        memcpy(&_data.at(s + 0), &type, sizeof(data_type));
        memcpy(&_data.at(s + sizeof(data_type)), &value_size, sizeof(int64_t));
        
        std::copy(value.begin(), value.end(), std::back_inserter(_data));
        size_t result = sizeof(data_type) + sizeof(int64_t) + value.size();
        return result;
        
    }
    template <class T>
    typename std::enable_if<is_string<T>::value, T>::type
    read() const
    {
        data_type type_read;
        int64_t len;

        memcpy(&type_read, &_data.at(_iter_read + 0), sizeof(data_type));
        assert(type_read == get_data_type<T>());
        memcpy(&len, &_data.at(_iter_read + sizeof(data_type)), sizeof(int64_t));
        assert(_iter_read + sizeof(data_type) + sizeof(int64_t) + len <= _data.size());

        auto begin = _data.begin() + (_iter_read + sizeof(data_type) + sizeof(int64_t));
        auto end = begin + len;
        std::string result;
        std::copy(begin, end, std::back_inserter(result));
        _iter_read += len + sizeof(data_type) + sizeof(int64_t);
        return result;
    }
    
    // —————————————— std::vector<T> ——————————————
    template <class Container>
    typename std::enable_if<is_vector<Container>::value && !is_bool<typename Container::value_type>::value && !is_string<typename Container::value_type>::value, size_t>::type
    write(const Container& vector)
    {
        auto type = get_data_type<Container>();
        auto s = _data.size();
        auto container_size = vector.size();
        auto item_size = sizeof(typename Container::value_type);
        
        _data.resize(s + sizeof(data_type) + sizeof(int64_t) + item_size * container_size);
        memcpy(&_data.at(s + 0), &type, sizeof(data_type));
        memcpy(&_data.at(s + sizeof(data_type)), &container_size, sizeof(int64_t));
        
        if(container_size > 0)
        {
            auto data = reinterpret_cast<const unsigned char*>(vector.data());
            memcpy(&_data.at(s + sizeof(data_type) + sizeof(int64_t)), data, item_size * container_size);
        }

        size_t result = sizeof(data_type) + sizeof(int64_t) + item_size * container_size;
        return result;
    }
    template <class Container>
    typename std::enable_if<is_vector<Container>::value && is_string<typename Container::value_type>::value, size_t>::type
    write(const Container& vector)
    {
        auto type = get_data_type<Container>();
        auto s = _data.size();
        auto container_size = vector.size();

        size_t append_size = 0;
        for(auto& value : vector){
            append_size += sizeof(int64_t) + value.size();
        }
        
        _data.resize(s + sizeof(data_type) + sizeof(int64_t) + append_size);
        memcpy(&_data.at(s + 0), &type, sizeof(data_type));
        memcpy(&_data.at(s + sizeof(data_type)), &container_size, sizeof(int64_t));
        
        size_t offset = s + sizeof(data_type) + sizeof(int64_t);
        for(auto& value : vector)
        {
            auto size = value.size();
            auto data = value.data();
            memcpy(&_data.at(offset + 0), &size, sizeof(int64_t));
            if(size > 0)
                memcpy(&_data.at(offset + sizeof(int64_t)), data, size);
            offset += sizeof(int64_t) + size;
        }
        size_t result = sizeof(data_type) + sizeof(int64_t) + append_size;
        return result;
    }
    
    template <class Container>
    typename std::enable_if<is_vector<Container>::value && is_bool<typename Container::value_type>::value, size_t>::type
    write(const Container& vector)
    {
        std::vector<char> temp;
        temp.reserve(vector.size());
        for(auto value : vector)
            temp.push_back(static_cast<char>(value));
        return write(temp);
    }
    
    template <class Container>
    typename std::enable_if<is_vector<Container>::value && !is_bool<typename Container::value_type>::value && !is_string<typename Container::value_type>::value, Container>::type
    read() const
    {
        data_type type_read;
        int64_t container_size;
        auto item_size = sizeof(typename Container::value_type);

        memcpy(&type_read, &_data.at(_iter_read + 0), sizeof(data_type));
        assert(type_read == get_data_type<Container>());
        memcpy(&container_size, &_data.at(_iter_read + sizeof(data_type)), sizeof(int64_t));
        assert(_iter_read + sizeof(data_type) + sizeof(int64_t) + container_size * item_size <= _data.size());

        if(container_size > 0)
        {
            const typename Container::value_type* begin = reinterpret_cast<const typename Container::value_type*>(&_data.at(_iter_read + sizeof(data_type) + sizeof(int64_t)));
            const typename Container::value_type* end = begin + container_size;
            Container result(begin, end);
            _iter_read += sizeof(data_type) + sizeof(int64_t) + container_size * item_size;
            assert(_iter_read <= _data.size());
            return result;
        }
        return {};
    }
    
    template <class Container>
    typename std::enable_if<is_vector<Container>::value && is_string<typename Container::value_type>::value, Container>::type
    read() const
    {
        data_type type_read;
        int64_t container_size;

        memcpy(&type_read, &_data.at(_iter_read + 0), sizeof(data_type));
        assert(type_read == get_data_type<Container>());
        memcpy(&container_size, &_data.at(_iter_read + sizeof(data_type)), sizeof(int64_t));

        Container result;
        size_t offset = _iter_read + sizeof(data_type) + sizeof(int64_t);
        for(size_t i=0; i<container_size; ++i)
        {
            int64_t len;
            memcpy(&len, &_data.at(offset + 0), sizeof(int64_t));
            assert(offset + sizeof(int64_t) + len <= _data.size());
            if(len > 0)
            {
                result.push_back(std::string(reinterpret_cast<const char*>(&_data.at(offset + sizeof(int64_t))), len));
            }
            else
            {
                result.push_back(std::string());
            }
            offset += sizeof(int64_t) + len;
        }
        _iter_read = offset;
        return result;
    }
    
    template <class Container>
    typename std::enable_if<is_vector<Container>::value && is_bool<typename Container::value_type>::value, Container>::type
    read() const
    {
        std::vector<char> temp;
        temp = read<std::vector<char>>();
        std::vector<bool> result;
        result.insert(result.end(), temp.begin(), temp.end());
        return result;
    }
    
    template <class Container>
    typename std::enable_if<is_map<Container>::value, size_t>::type
    write(const Container& map)
    {
        uint64_t size = map.size();
        uint64_t result = write<uint64_t>(size);
        for(auto& pair : map)
        {
            result += write<typename Container::key_type>(pair.first);
            result += write<typename Container::mapped_type>(pair.second);
        }
        return result;
    }
    template <class Container>
    typename std::enable_if<is_map<Container>::value, Container>::type
    read() const
    {
        uint64_t size = read<uint64_t>();
        Container result;
        for(size_t i=0; i<size; ++i)
        {
            typename Container::key_type key = read<typename Container::key_type>();
            typename Container::mapped_type value = read<typename Container::mapped_type>();
            result[key] = value;
        }
        return result;
    }
    
    size_t write_data(const Data& data)
    {
        uint64_t result = write<uint64_t>(data._data.size());
        _data.insert(_data.end(), data._data.begin(), data._data.end());
        result += data._data.size();
        return result;
    }
    Data read_data() const
    {
        uint64_t size = read<uint64_t>();
        Data result;
        assert(_iter_read + size <= _data.size());
        result._data.insert(result._data.begin(), _data.begin() + _iter_read, _data.begin() + _iter_read + size);
        _iter_read += size;
        return result;
    }
    
private:
    std::vector<unsigned char> _data;
    mutable size_t _iter_read;
};
}

#endif /* BinaryFormat_hpp */
