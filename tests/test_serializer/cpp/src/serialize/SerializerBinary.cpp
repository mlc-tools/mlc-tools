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
