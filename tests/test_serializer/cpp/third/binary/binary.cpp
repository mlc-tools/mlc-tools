//
//  BinaryFormat.cpp
//  Serializer
//
//  Created by Vladimir Tolmachev on 17.06.2025.
//

#include "binary.h"
#include <cassert>
#include <list>
#include "mg_extensions.h"

namespace mg{


BinaryFormat::BinaryFormat(Data&& data)
: _data(std::move(data))
{
}
BinaryFormat::BinaryFormat(const std::vector<unsigned char>& data)
{
    set_data(data);
}

void BinaryFormat::set_data(const std::vector<unsigned char>& rawdata)
{
    Data data(rawdata);
    _dict.read(data);
    _data = data.read_data();
    auto children_count = data.read<uint64_t>();
    _childrenNames.reserve(children_count);
    _children.reserve(children_count);
    for(size_t i=0; i<children_count; ++i)
    {
        auto name = data.read<std::string>();
        _childrenNames.push_back(name);
    }
    for(size_t i=0; i<children_count; ++i)
    {
        auto child_data = data.read_data();
        BinaryFormat child;
        child.set_data(child_data.get_data());
        _children.push_back(std::move(child));
    }
}
void BinaryFormat::set_string_data(const std::string& data)
{
    std::vector<unsigned char> udata(data.begin(), data.end());
    set_data(udata);
}

std::string BinaryFormat::get_human_string(int indent) const
{
    auto get_indent = [](int indent){
        std::string res;
        for(int i=0; i<indent; ++i)
            res += " ";
        return res;
    };
    auto dataTypeToStr = [](const Data::data_type& type) -> std::string
    {
        switch(type)
        {
            case Data::data_type::t_int32: return "t_int32";
            case Data::data_type::t_uint32: return "t_uint32";
            case Data::data_type::t_int64: return "t_int64";
            case Data::data_type::t_uint64: return "t_uint64";
            case Data::data_type::t_bool: return "t_bool";
            case Data::data_type::t_float: return "t_float";
            case Data::data_type::t_double: return "t_double";
            case Data::data_type::t_string: return "t_string";
            case Data::data_type::t_char: return "t_char";
            case Data::data_type::t_vector: return "t_vector";
            case Data::data_type::t_map: return "t_map";
            default:
                assert(0);
        }
        return "";
    };
    std::string result;
    std::list<std::pair<std::string, std::pair<size_t, size_t>>> keys;
    keys.insert(keys.end(), _dict.get_all().begin(), _dict.get_all().end());
    keys.sort([](const std::pair<std::string, std::pair<size_t, size_t>>& lhs, const std::pair<std::string, std::pair<size_t, size_t>>& rhs){
        return lhs.second.first < rhs.second.first;
    });
    for(auto& pair : keys)
    {
        auto type = _data.read_type(pair.second.first);
        result += get_indent(indent) + pair.first + ": offset=" + toStr(pair.second.first) + ", size=" + toStr(pair.second.second) + ", type: " + dataTypeToStr(type);
        if(type == Data::data_type::t_string)
        {
            _data.set_offset(pair.second.first);
            result += ", value: " + _data.read<std::string>();
        }
        result += "\n";
    }
    result += get_indent(indent) + "children count=" + toStr(_children.size()) + ":\n";
    for(size_t i=0; i<_children.size(); ++i)
    {
        result += get_indent(indent) + "name=" + _childrenNames.at(i) + ":\n";
        result += _children.at(i).get_human_string(indent + 2);
    }
    return result;
}

std::vector<unsigned char> BinaryFormat::get_data() const
{
    Data temp;
    _dict.write(temp);
    temp.write_data(_data);
    temp.write<uint64_t>(_childrenNames.size());
    for(auto name : _childrenNames)
        temp.write(name);
    for(auto& child : _children)
        temp.write_data(child.get_data());
    return temp.get_data();
}
std::string BinaryFormat::get_string_data() const
{
    auto data = get_data();
    return std::string(data.begin(), data.end());
}

BinaryFormat& BinaryFormat::add_node(const std::string& name)
{
    _children.emplace_back();
    _childrenNames.push_back(name);
    return _children.back();
}

BinaryFormat& BinaryFormat::get_node(const std::string& name)
{
    static BinaryFormat empty;
    auto iter = std::find(_childrenNames.begin(), _childrenNames.end(), name);
    if(iter != _childrenNames.end())
    {
        auto index = iter - _childrenNames.begin();
        return _children.at(index);
    }
    return empty;
}

int32_t BinaryFormat::get_int(const std::string& key, int32_t default_value) const
{
    if(!_dict.has(key))return default_value;
    _data.set_offset(_dict.get(key).first);
    return _data.read<int32_t>();
}
int64_t BinaryFormat::get_int64(const std::string& key, int64_t default_value) const
{
    if(!_dict.has(key))return default_value;
    _data.set_offset(_dict.get(key).first);
    return _data.read<int64_t>();
}
uint32_t BinaryFormat::get_unsigned(const std::string& key, uint32_t default_value) const
{
    if(!_dict.has(key))return default_value;
    _data.set_offset(_dict.get(key).first);
    return _data.read<uint32_t>();
}
uint64_t BinaryFormat::get_unsigned64(const std::string& key, uint64_t default_value) const
{
    if(!_dict.has(key))return default_value;
    _data.set_offset(_dict.get(key).first);
    return _data.read<uint64_t>();
}
bool BinaryFormat::get_bool(const std::string& key, bool default_value) const
{
    if(!_dict.has(key))return default_value;
    _data.set_offset(_dict.get(key).first);
    return _data.read<bool>();
}
float BinaryFormat::get_float(const std::string& key, float default_value) const
{
    if(!_dict.has(key))return default_value;
    _data.set_offset(_dict.get(key).first);
    return _data.read<float>();
}
double BinaryFormat::get_double(const std::string& key, double default_value) const
{
    if(!_dict.has(key))return default_value;
    _data.set_offset(_dict.get(key).first);
    return _data.read<double>();
}
std::string BinaryFormat::get_string(const std::string& key, const std::string& default_value) const
{
    if(!_dict.has(key))return default_value;
    _data.set_offset(_dict.get(key).first);
    return _data.read<std::string>();
}

void BinaryFormat::add(const std::string &key, const int32_t &value)
{
    _dict.add(key, _data.write(value));
}
void BinaryFormat::add(const std::string &key, const int64_t &value)
{
    _dict.add(key, _data.write(value));
}
void BinaryFormat::add(const std::string &key, const uint32_t &value)
{
    _dict.add(key, _data.write(value));
}
void BinaryFormat::add(const std::string &key, const uint64_t &value)
{
    _dict.add(key, _data.write(value));
}
void BinaryFormat::add(const std::string &key, const bool &value)
{
    _dict.add(key, _data.write(value));
}
void BinaryFormat::add(const std::string &key, const float &value)
{
    _dict.add(key, _data.write(value));
}
void BinaryFormat::add(const std::string &key, const double &value)
{
    _dict.add(key, _data.write(value));
}
void BinaryFormat::add(const std::string &key, const char* value)
{
    _dict.add(key, _data.write(std::string(value)));
}
void BinaryFormat::add(const std::string &key, const std::string &value)
{
    _dict.add(key, _data.write(value));
}

namespace tests
{
void test_data()
{
    std::map<int32_t, int32_t> map1 = {
        {1, 2},
        {3, 4},
        {5, 6},
        {7, 8},
    };
    std::map<std::string, int32_t> map2 = {
        {"1", 12},
        {"3", 14},
        {"5", 16},
        {"7", 18},
    };
    std::map<std::string, std::string> map3 = {
        {"1", "12"},
        {"3", "14"},
        {"5", "16"},
        {"7", "18"},
    };
    std::map<std::string, std::vector<int>> map4 = {
        {"1", {1, 4, 12}},
        {"3", {31, 54, 712}},
    };
    
    Data writer;
    writer.write<int32_t>(1);
    writer.write<int32_t>(3);
    writer.write<float>(3);
    writer.write<std::string>("hello world 1");
    writer.write<std::vector<int32_t>>({2, 4, 6, 8});
    writer.write<std::vector<float>>({2, 4, 6, 8});
    writer.write(map1);
    writer.write<int32_t>(5);
    writer.write<int32_t>(7);
    writer.write<std::string>("hello world 2");
    writer.write<std::vector<int32_t>>({12, 14, 16, 18});
    writer.write(map2);
    writer.write(map3);
    writer.write(map4);
    
    Data reader(writer);
    assert(reader.read<int32_t>() == 1);
    assert(reader.read<int32_t>() == 3);
    assert(reader.read<float>() == 3);
    assert(reader.read<std::string>() == "hello world 1");
    assert(reader.read<std::vector<int32_t>>() == std::vector<int32_t>({2, 4, 6, 8}));
    assert(reader.read<std::vector<float>>() == std::vector<float>({2, 4, 6, 8}));
    assert((reader.read<std::map<int32_t, int32_t>>() == map1));
    assert(reader.read<int32_t>() == 5);
    assert(reader.read<int32_t>() == 7);
    assert(reader.read<std::string>() == "hello world 2");
    assert(reader.read<std::vector<int32_t>>() == std::vector<int32_t>({12, 14, 16, 18}));
    assert((reader.read<std::map<std::string, int32_t>>() == map2));
    assert((reader.read<std::map<std::string, std::string>>() == map3));
    assert((reader.read<std::map<std::string, std::vector<int>>>() == map4));
}

void test_dictionary()
{
    Data data;
    Dictionary dict;
    dict.add("1", 1);
    dict.add("2", 2);
    dict.add("3", 3);
    dict.add("4", 4);
    dict.write(data);
    
    Data reader(data.get_data());
    Dictionary dict2;
    dict2.read(reader);
    assert(dict2.get("1").first == 0);
    assert(dict2.get("2").first == 1);
    assert(dict2.get("3").first == 3);
    assert(dict2.get("4").first == 6);
    
    assert(dict2.get("1").second == 1);
    assert(dict2.get("2").second == 2);
    assert(dict2.get("3").second == 3);
    assert(dict2.get("4").second == 4);
}

void test_binary_format_()
{
    BinaryFormat writer;
    writer.add("key0", (int32_t)1);
    writer.add("key1", "test_string");
    writer.add_node("inner_node1").add("k", 123.f);
    writer.add_node("inner_node2").add("l", 223.f);
    writer.add_node("inner_node3").add("m", 323.f);
    writer.add_node("inner_node4").add("n", 423.f);
    
    std::cout << writer.get_human_string() << std::endl;
    
    BinaryFormat reader(writer.get_data());
    assert(reader.get_int("key0", 0) == 1);
    assert(reader.get_string("key1", "") == "test_string");
    assert(reader.get_node("inner_node1").get_float("k", 0.f) == 123.f);
    assert(reader.get_node("inner_node2").get_float("l", 0.f) == 223.f);
    assert(reader.get_node("inner_node3").get_float("m", 0.f) == 323.f);
    assert(reader.get_node("inner_node4").get_float("n", 0.f) == 423.f);
}

void test_binary_format()
{
    test_data();
    test_dictionary();
    test_binary_format_();
}
}
}
