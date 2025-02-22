#include "SerializerJson.h"
#include "jsoncpp/json.h"


namespace mg
{
SerializerJson::SerializerJson(Json::Value &json) : _json(json)
{
}

SerializerJson::SerializerJson(const SerializerJson &rhs) = default;


SerializerJson::~SerializerJson() = default;

SerializerJson::SerializerJson(SerializerJson &&rhs) noexcept = default;


SerializerJson SerializerJson::add_child(const std::string &name)
{
    return SerializerJson(_json[name]);
}

SerializerJson SerializerJson::add_array(const std::string &name)
{
    return SerializerJson(_json[name]);
}

SerializerJson SerializerJson::add_array_item()
{
    return SerializerJson(_json.append(Json::Value()));
}

void SerializerJson::add_attribute(const std::string &key, const int &value, int default_value)
{
    if (value != default_value)
    {
        _json[key] = value;
    }
}

void SerializerJson::add_attribute(const std::string &key, const int64_t &value, int64_t default_value)
{
    if (value != default_value)
    {
        _json[key] = value;
    }
}

void SerializerJson::add_attribute(const std::string &key, const unsigned int &value, unsigned int default_value)
{
    if (value != default_value)
    {
        _json[key] = value;
    }
}

void SerializerJson::add_attribute(const std::string &key, const uint64_t &value, uint64_t default_value)
{
    if (value != default_value)
    {
        _json[key] = value;
    }
}

void SerializerJson::add_attribute(const std::string &key, const bool &value, bool default_value)
{
    if (value != default_value)
    {
        _json[key] = value;
    }
}

void SerializerJson::add_attribute(const std::string &key, const float &value, float default_value)
{
    if (value != default_value)
    {
        _json[key] = value;
    }
}

void SerializerJson::add_attribute(const std::string &key, const double &value, double default_value)
{
    if (value != default_value)
    {
        _json[key] = value;
    }
}

void SerializerJson::add_attribute(const std::string &key, const std::string &value, const std::string &default_value)
{
    if (value != default_value)
    {
        _json[key] = value;
    }
}

void SerializerJson::add_array_item(const int &value)
{
    _json.append(value);
}

void SerializerJson::add_array_item(const int64_t &value)
{
    _json.append(value);
}

void SerializerJson::add_array_item(const unsigned int &value)
{
    _json.append(value);
}

void SerializerJson::add_array_item(const uint64_t &value)
{
    _json.append(value);
}

void SerializerJson::add_array_item(const bool &value)
{
    _json.append(value);
}

void SerializerJson::add_array_item(const float &value)
{
    _json.append(value);
}

void SerializerJson::add_array_item(const double &value)
{
    _json.append(value);
}

void SerializerJson::add_array_item(const std::string &value)
{
    _json.append(value);
}


DeserializerJson::DeserializerJson(Json::Value &json) : _json(json)
{

}

DeserializerJson::DeserializerJson(const DeserializerJson &rhs) : _json(rhs._json)
{

}

DeserializerJson::DeserializerJson(DeserializerJson &&rhs) noexcept = default;

DeserializerJson::~DeserializerJson() = default;

DeserializerJson DeserializerJson::get_child(const std::string &name)
{
    return DeserializerJson(_json[name]);
}

int DeserializerJson::get_attribute(const std::string &key, int default_value)
{
    return _json.isMember(key) ? _json[key].asInt() : default_value;
}

int64_t DeserializerJson::get_attribute(const std::string &key, int64_t default_value)
{
    return _json.isMember(key) ? _json[key].asInt64() : default_value;
}

unsigned int DeserializerJson::get_attribute(const std::string &key, unsigned int default_value)
{
    return _json.isMember(key) ? _json[key].asUInt() : default_value;
}

uint64_t DeserializerJson::get_attribute(const std::string &key, uint64_t default_value)
{
    return _json.isMember(key) ? _json[key].asUInt64() : default_value;
}

bool DeserializerJson::get_attribute(const std::string &key, bool default_value)
{
    return _json.isMember(key) ? _json[key].asBool() : default_value;
}

float DeserializerJson::get_attribute(const std::string &key, float default_value)
{
    return _json.isMember(key) ? _json[key].asFloat() : default_value;
}

double DeserializerJson::get_attribute(const std::string &key, double default_value)
{
    return _json.isMember(key) ? _json[key].asFloat() : default_value;
}

std::string DeserializerJson::get_attribute(const std::string &key, const std::string &default_value)
{
    return _json.isMember(key) ? _json[key].asString() : default_value;
}

void DeserializerJson::get_array_item(int &value)
{
    value = _json.asInt();
}

void DeserializerJson::get_array_item(int64_t &value)
{
    value = _json.asInt64();
}

void DeserializerJson::get_array_item(bool &value)
{
    value = _json.asBool();
}

void DeserializerJson::get_array_item(float &value)
{
    value = _json.asFloat();
}

void DeserializerJson::get_array_item(double &value)
{
    value = _json.asDouble();
}

void DeserializerJson::get_array_item(std::string &value)
{
    value = _json.asString();
}

DeserializerJson::iterator DeserializerJson::begin()
{
    return DeserializerJson::iterator(_json.begin());
}

DeserializerJson::iterator DeserializerJson::end()
{
    return DeserializerJson::iterator(_json.end());
}

DeserializerJson::iterator::iterator(Json::ValueIterator iterator) : _iterator()
{
    _iterator = iterator;
}

bool DeserializerJson::iterator::operator!=(const iterator &rhs) const
{
    return *_iterator != *rhs._iterator;
}

DeserializerJson::iterator &DeserializerJson::iterator::operator++()
{
    ++*_iterator;
    return *this;
}

DeserializerJson DeserializerJson::iterator::operator*()
{
    return DeserializerJson(**_iterator);
}
}
