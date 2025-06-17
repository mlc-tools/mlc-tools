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
    Data();
    Data(Data&& data);
    Data(const Data& data);
    Data(const std::vector<unsigned char>& blob);
    Data& operator=(const Data& data);
    
    void set_data(const std::vector<unsigned char>& data);
    std::vector<unsigned char> get_data() const;
    
    void set_offset(size_t offset) const;
    
    template <class T>
    typename std::enable_if<is_simple<T>::value, size_t>::type
    write(T value)
    {
        auto s = _data.size();
        auto append = sizeof(T);
        _data.resize(s + append);
        memcpy(&_data.at(s), &value, append);
        return append;
    }
    template <class T>
    typename std::enable_if<is_simple<T>::value, T>::type
    read() const
    {
        T result;
        auto size = sizeof(result);
        memcpy(&result, &_data.at(_iter_read), size);
        _iter_read += size;
        return result;
    }
    
    /* BaseEnum */
    template <class T>
    typename std::enable_if<is_enum<T>::value, size_t>::type
    write(T value)
    {
        auto s = _data.size();
        auto append = sizeof(T);
        _data.resize(s + append);
        auto int_value = (int)value;
        memcpy(&_data.at(s), &int_value, append);
        return append;
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
        auto result = write(static_cast<int32_t>(value.size()));
        std::copy(value.begin(), value.end(), std::back_inserter(_data));
        result += value.size();
        return result;
        
    }
    template <class T>
    typename std::enable_if<is_string<T>::value, T>::type
    read() const
    {
        int32_t len = read<int32_t>();
        auto begin = _data.begin() + _iter_read;
        auto end = _data.begin() + (_iter_read + len);
        std::string result;
        std::copy(begin, end, std::back_inserter(result));
        _iter_read += len;
        return result;
    }
    
    // —————————————— std::vector<T> ——————————————
    template <class Container>
    typename std::enable_if<is_vector<Container>::value && !is_bool<typename Container::value_type>::value, size_t>::type
    write(const Container& vector)
    {
        auto size = vector.size();
        auto len = sizeof(typename Container::value_type) * size;
        if(_data.capacity() < _data.size() + len)
            _data.reserve(_data.size() + len);
        
        auto result = write<uint64_t>(size) + len;
        auto data = reinterpret_cast<const unsigned char*>(vector.data());
        std::copy(data, data + len, std::back_inserter(_data));
        return result;
    }
    
    template <class Container>
    typename std::enable_if<is_vector<Container>::value && is_bool<typename Container::value_type>::value, size_t>::type
    write(const Container& vector)
    {
        std::vector<char> temp;
        temp.reserve(vector.size());
        for(auto value : vector)
            temp.push_back(static_cast<int32_t>(value));
        return write(temp);
    }
    
    template <class Container>
    typename std::enable_if<is_vector<Container>::value, Container>::type
    read() const
    {
        auto size = read<uint64_t>();
        auto len = size * sizeof(typename Container::value_type);
        const typename Container::value_type* begin = reinterpret_cast<const typename Container::value_type*>(&_data.at(_iter_read));
        const typename Container::value_type* end = begin + size;
        Container result(begin, end);
        _iter_read += len;
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
