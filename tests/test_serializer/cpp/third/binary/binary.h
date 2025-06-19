//
//  BinaryFormat.hpp
//  Serializer
//
//  Created by Vladimir Tolmachev on 17.06.2025.
//

#ifndef binary_binary_hpp
#define binary_binary_hpp

#include "data.h"
#include "dictionary.h"

namespace mg{

class BinaryFormat
{
public:
public:
    BinaryFormat() = default;
    BinaryFormat(Data&& data);
    BinaryFormat(const std::vector<unsigned char>& data);
    
    void set_data(const std::vector<unsigned char>& data);
    void set_string_data(const std::string& data);
    std::vector<unsigned char> get_data() const;
    std::string get_string_data() const;
    
    std::string get_human_string(int indent=0) const;
    
    
    BinaryFormat& add_node(const std::string& name);
    BinaryFormat& get_node(const std::string& name);
    std::vector<BinaryFormat>& get_children() { return _children; }
    
    int32_t get_int(const std::string& key, int32_t default_value) const;
    int64_t get_int64(const std::string& key, int64_t default_value) const;
    uint32_t get_unsigned(const std::string& key, uint32_t default_value) const;
    uint64_t get_unsigned64(const std::string& key, uint64_t default_value) const;
    bool get_bool(const std::string& key, bool default_value) const;
    float get_float(const std::string& key, float default_value) const;
    double get_double(const std::string& key, double default_value) const;
    std::string get_string(const std::string& key, const std::string& default_value) const;
    
    void add(const std::string &key, const int32_t &value);
    void add(const std::string &key, const int64_t &value);
    void add(const std::string &key, const uint32_t &value);
    void add(const std::string &key, const uint64_t &value);
    void add(const std::string &key, const bool &value);
    void add(const std::string &key, const float &value);
    void add(const std::string &key, const double &value);
    void add(const std::string &key, const char* value);
    void add(const std::string &key, const std::string &value);
    
    template <class T>
    std::vector<T> get_array(const std::string &key)
    {
        auto offset = _dict.get(key).first;
        _data.set_offset(offset);
        auto result = _data.read<std::vector<T>>();
        return result;
    }
    template <class T>
    void add_array(const std::string &key, const std::vector<T>& vector)
    {
        _dict.add(key, _data.write(vector));
    }
    
    
    template <class K, class V>
    std::map<K, V> get_map(const std::string &key)
    {
        auto offset = _dict.get(key).first;
        _data.set_offset(offset);
        auto result = _data.read<std::map<K, V>>();
        return result;
    }
    template <class K, class V>
    void add_map(const std::string &key, const std::map<K, V>& map)
    {
        _dict.add(key, _data.write(map));
    }
private:
    Dictionary _dict;
    Data _data;
    std::vector<BinaryFormat> _children;
    std::vector<std::string> _childrenNames;
};


namespace tests
{
void test_binary_format();
}
}

#endif /* BinaryFormat_hpp */
