//
// Created by Vladimir Tolmachev on 18/02/2020.
//

#include "SerializerXml.h"
#include "../../third/pugixml/pugixml.hpp"
#include <iostream>
#include <sstream>


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

int DeserializerXml::get_attribute(const std::string &key, int default_value)
{
    return _node->attribute(key.c_str()).as_int(default_value);
}

bool DeserializerXml::get_attribute(const std::string &key, bool default_value)
{
    return _node->attribute(key.c_str()).as_bool(default_value);
}

float DeserializerXml::get_attribute(const std::string &key, float default_value)
{
    return _node->attribute(key.c_str()).as_float(default_value);
}

std::string DeserializerXml::get_attribute(const std::string &key, const std::string &default_value)
{
    return _node->attribute(key.c_str()).as_string(default_value.c_str());
}

DeserializerXml DeserializerXml::begin()
{
    return DeserializerXml(*_node ? *_node->begin() : pugi::xml_node());
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