//
// Created by Vladimir Tolmachev on 2020-02-21.
//

#include "SerializerJson.h"
#include "../../third/jsoncpp/json.h"
#include <iostream>
#include <sstream>


SerializerJson::SerializerJson(Json::Value& json)
: _json(json)
{
}

SerializerJson::SerializerJson(const SerializerJson& rhs) = default;


SerializerJson::~SerializerJson() = default;

SerializerJson::SerializerJson(SerializerJson&& rhs) noexcept = default;

//SerializerJson& SerializerJson::operator=(const SerializerJson& rhs){
//    if(this == &rhs)
//        return *this;
//    *_json = *rhs._json;
//    return *this;
//}

void SerializerJson::log(const Json::Value& json)
{
    std::cout << "JSON:\n" << SerializerJson::toStr(json) << std::endl;
}

std::string SerializerJson::toStr(const Json::Value& json)
{
    Json::StreamWriterBuilder wbuilder;
    wbuilder["indentation"] = " ";
    return Json::writeString(wbuilder, json);
}

SerializerJson SerializerJson::add_child(const std::string& name){
    return SerializerJson(_json[name]);
}
SerializerJson SerializerJson::add_array(const std::string& name){
    return SerializerJson(_json[name]);
}
SerializerJson SerializerJson::add_array_item(){
    return SerializerJson(_json.append(Json::Value()));
}
void SerializerJson::add_attribute(const std::string& key, const int& value, int default_value){
    if(value != default_value)
        _json[key] = value;
}
void SerializerJson::add_attribute(const std::string& key, const bool& value, bool default_value){
    if(value != default_value)
        _json[key] = value;
}
void SerializerJson::add_attribute(const std::string& key, const float& value, float default_value){
    if(value != default_value)
        _json[key] = value;
}
void SerializerJson::add_attribute(const std::string& key, const std::string& value, const std::string& default_value){
    if(value != default_value)
        _json[key] = value;
}
void SerializerJson::add_array_item(const int& value){
    _json.append(value);
}
void SerializerJson::add_array_item(const bool& value){
    _json.append(value);
}
void SerializerJson::add_array_item(const float& value){
    _json.append(value);
}
void SerializerJson::add_array_item(const std::string& value){
    _json.append(value);
}


//DeSerializerJson::DeSerializerJson(pugi::xml_json node)
//{
//    _json = node;
//}
//DeSerializerJson::DeSerializerJson(const DeSerializerJson& rhs) = default;
//DeSerializerJson::DeSerializerJson(DeSerializerJson&& rhs) noexcept: _json(std::move(rhs._json)) {
//}
//DeSerializerJson::~DeSerializerJson() = default;
//DeSerializerJson& DeSerializerJson::operator=(const DeSerializerJson& rhs){
//    if(this == &rhs){
//        return *this;
//    }
//    *_json = *rhs._json;
//    return *this;
//}
//DeSerializerJson DeSerializerJson::get_child(const std::string& name){
//    return DeSerializerJson(_json->child(name.c_str()));
//}
//int DeSerializerJson::get_attribute(const std::string& key, int default_value){
//    return _json->attribute(key.c_str()).as_int(default_value);
//}
//bool DeSerializerJson::get_attribute(const std::string& key, bool default_value){
//    return _json->attribute(key.c_str()).as_bool(default_value);
//}
//float DeSerializerJson::get_attribute(const std::string& key, float default_value){
//    return _json->attribute(key.c_str()).as_float(default_value);
//}
//std::string DeSerializerJson::get_attribute(const std::string& key, const std::string& default_value){
//    return _json->attribute(key.c_str()).as_string(default_value.c_str());
//}
//
//DeSerializerJson DeSerializerJson::begin(){
//    return DeSerializerJson(*_json ? *_json->begin() : pugi::xml_json());
//}
//DeSerializerJson DeSerializerJson::end(){
//    return DeSerializerJson(pugi::xml_json());
//}
//bool DeSerializerJson::operator != (const DeSerializerJson& rhs) const{
//    return *_json != *rhs._json;
//}
//DeSerializerJson& DeSerializerJson::operator ++ (){
//    _json = _json->next_sibling();
//    return *this;
//}
//DeSerializerJson DeSerializerJson::operator *(){
//    return *this;
//}
