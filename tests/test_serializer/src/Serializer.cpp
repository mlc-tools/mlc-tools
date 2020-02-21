//
// Created by Vladimir Tolmachev on 18/02/2020.
//

#include "Serializer.h"
#include "../third/pugixml/pugixml.hpp"
#include <iostream>
#include <sstream>


Serializer::Serializer(pugi::xml_node node)
: _node()
{
    _node = node;
}

Serializer::Serializer(const Serializer& rhs) = default;


Serializer::~Serializer() = default;

Serializer::Serializer(Serializer&& rhs) noexcept
: _node(std::move(rhs._node))
{
}

Serializer& Serializer::operator=(const Serializer& rhs){
    if(this == &rhs)
        return *this;
    *_node = *rhs._node;
    return *this;
}

void Serializer::log(const pugi::xml_document& document)
{
    std::cout << "XML:\n" << Serializer::toStr(document) << std::endl;
}

std::string Serializer::toStr(const pugi::xml_document& document)
{
    std::stringstream stream;
    pugi::xml_writer_stream writer(stream);
    document.save(writer,
                  " ",
                  pugi::format_no_declaration | pugi::format_indent,
                  pugi::xml_encoding::encoding_auto);

    return stream.str();
}

Serializer Serializer::add_child(const std::string& name){
    return Serializer(_node->append_child(name.c_str()));
}
void Serializer::add_attribute(const std::string& key, const int& value, int default_value){
    if(value != default_value)
        _node->append_attribute(key.c_str()).set_value(value);
}
void Serializer::add_attribute(const std::string& key, const bool& value, bool default_value){
    if(value != default_value)
        _node->append_attribute(key.c_str()).set_value(value);
}
void Serializer::add_attribute(const std::string& key, const float& value, float default_value){
    if(value != default_value)
        _node->append_attribute(key.c_str()).set_value(value);
}
void Serializer::add_attribute(const std::string& key, const std::string& value, const std::string& default_value){
    if(value != default_value)
        _node->append_attribute(key.c_str()).set_value(value.c_str());
}


Deserializer::Deserializer(pugi::xml_node node)
{
    _node = node;
}
Deserializer::Deserializer(const Deserializer& rhs) = default;
Deserializer::Deserializer(Deserializer&& rhs) noexcept: _node(std::move(rhs._node)) {
}
Deserializer::~Deserializer() = default;
Deserializer& Deserializer::operator=(const Deserializer& rhs){
    if(this == &rhs){
        return *this;
    }
    *_node = *rhs._node;
    return *this;
}
Deserializer Deserializer::get_child(const std::string& name){
    return Deserializer(_node->child(name.c_str()));
}
int Deserializer::get_attribute(const std::string& key, int default_value){
    return _node->attribute(key.c_str()).as_int(default_value);
}
bool Deserializer::get_attribute(const std::string& key, bool default_value){
    return _node->attribute(key.c_str()).as_bool(default_value);
}
float Deserializer::get_attribute(const std::string& key, float default_value){
    return _node->attribute(key.c_str()).as_float(default_value);
}
std::string Deserializer::get_attribute(const std::string& key, const std::string& default_value){
    return _node->attribute(key.c_str()).as_string(default_value.c_str());
}

Deserializer Deserializer::begin(){
    return Deserializer(*_node ? *_node->begin() : pugi::xml_node());
}
Deserializer Deserializer::end(){
    return Deserializer(pugi::xml_node());
}
bool Deserializer::operator != (const Deserializer& rhs) const{
    return *_node != *rhs._node;
}
Deserializer& Deserializer::operator ++ (){
    _node = _node->next_sibling();
    return *this;
}
Deserializer Deserializer::operator *(){
    return *this;
}