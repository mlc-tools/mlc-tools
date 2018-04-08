/******************************************************************************/
/*
* Copyright 2014-2017 Vladimir Tolmachev
*
* Author: Vladimir Tolmachev
* Project: ml
* e-mail: tolm_vl@hotmail.com
* If you received the code is not the author, please contact me
*/
/******************************************************************************/

#include <cstdint>
#include "Generics.h"
#include "converters.h"
#include "jsoncpp/json.h"

// from string

template <> std::string strTo(const std::string &value)
{
	return value;
}
template <> float strTo(const std::string &value)
{
	return strToFloat(value);
}
template <> int32_t strTo(const std::string &value)
{
	return strToInt(value);
}
template <> int64_t strTo(const std::string &value)
{
	return strToInt(value);
}
template <> uint32_t strTo(const std::string &value)
{
	return static_cast<uint32_t>(strToInt(value));
}
template <> uint64_t strTo(const std::string &value)
{
	return static_cast<uint64_t>(strToInt(value));
}
template <> bool strTo(const std::string &value)
{
	return strToBool(value);
}

// to string

template <> std::string toStr(std::string value)
{
	return value;
}
template <> std::string toStr( char const * value )
{
	return std::string( value ? value : "" );
}
template <> std::string toStr(const std::string &value)
{
	return value;
}
template <> std::string toStr(int value)
{
	return intToStr(value);
}
template <> std::string toStr(long value)
{
	return intToStr(static_cast<int>(value));
}
template <> std::string toStr(long long value)
{
	return intToStr(static_cast<int>(value));
}
template <> std::string toStr(unsigned int value)
{
	return intToStr(static_cast<int>(value));
}
template <> std::string toStr( unsigned long value)
{
	return intToStr(static_cast<int>(value));
}
template <> std::string toStr( unsigned long long value)
{
	return intToStr(static_cast<int>(value));
}
template <> std::string toStr(bool value)
{
	return boolToStr( value );
}
template <> std::string toStr( float value )
{
	return floatToStr( value );
}


//JSON
template <> void set( Json::Value& json, int8_t value ) { json = value; }
template <> void set( Json::Value& json, int16_t value ) { json = value; }
template <> void set( Json::Value& json, int32_t value ) { json = value; }
template <> void set( Json::Value& json, int64_t value ) { json = value; }
template <> void set( Json::Value& json, uint8_t value ) { json = value; }
template <> void set( Json::Value& json, uint16_t value ) { json = value; }
template <> void set( Json::Value& json, uint32_t value ) { json = value; }
template <> void set( Json::Value& json, uint64_t value ) { json = value; }
template <> void set( Json::Value& json, bool value ) { json = value; }
template <> void set( Json::Value& json, float value ) { json = value; }
template <> void set( Json::Value& json, std::string value ) { json = value; }

template <> int8_t get( const Json::Value& json ) { return json.asInt(); }
template <> int16_t get( const Json::Value& json ) { return json.asInt(); }
template <> int32_t get( const Json::Value& json ) { return json.asInt(); }
template <> int64_t get( const Json::Value& json ) { return json.asInt64(); }
template <> uint8_t get( const Json::Value& json ) { return json.asUInt(); }
template <> uint16_t get( const Json::Value& json ) { return json.asUInt(); }
template <> uint32_t get( const Json::Value& json ) { return json.asUInt(); }
template <> uint64_t get( const Json::Value& json ) { return json.asUInt64(); }
template <> bool get( const Json::Value& json ) { return json.asBool(); }
template <> float get( const Json::Value& json ) { return json.asFloat(); }
template <> std::string get( const Json::Value& json ) { return json.asString(); }

//XML
//template <class T> void set(pugi::xml_attribute& xml, T value);
//template <class T> T get(const pugi::xml_attribute& xml);

template <> void set(pugi::xml_attribute& xml, int8_t value) { xml.set_value(value); }
template <> void set(pugi::xml_attribute& xml, int16_t value) { xml.set_value(value); }
template <> void set(pugi::xml_attribute& xml, int32_t value) { xml.set_value(value); }
template <> void set(pugi::xml_attribute& xml, int64_t value) { xml.set_value(static_cast<int32_t>(value)); }
template <> void set(pugi::xml_attribute& xml, uint8_t value) { xml.set_value(value); }
template <> void set(pugi::xml_attribute& xml, uint16_t value) { xml.set_value(value); }
template <> void set(pugi::xml_attribute& xml, uint32_t value) { xml.set_value(value); }
template <> void set(pugi::xml_attribute& xml, uint64_t value) { xml.set_value(static_cast<uint32_t>(value)); }
template <> void set(pugi::xml_attribute& xml, bool value) { xml.set_value(value); }
template <> void set(pugi::xml_attribute& xml, float value) { xml.set_value(value); }
template <> void set(pugi::xml_attribute& xml, std::string value) { xml.set_value(value.c_str()); }

template <> int8_t get(const pugi::xml_attribute& xml) { return xml.as_int(); }
template <> int16_t get(const pugi::xml_attribute& xml) { return xml.as_int(); }
template <> int32_t get(const pugi::xml_attribute& xml) { return xml.as_int(); }
template <> int64_t get(const pugi::xml_attribute& xml) { return xml.as_int(); }
template <> uint8_t get(const pugi::xml_attribute& xml) { return xml.as_uint(); }
template <> uint16_t get(const pugi::xml_attribute& xml) { return xml.as_uint(); }
template <> uint32_t get(const pugi::xml_attribute& xml) { return xml.as_uint(); }
template <> uint64_t get(const pugi::xml_attribute& xml) { return xml.as_uint(); }
template <> bool get(const pugi::xml_attribute& xml) { return xml.as_bool(); }
template <> float get(const pugi::xml_attribute& xml) { return xml.as_float(); }
template <> std::string get(const pugi::xml_attribute& xml) { return xml.as_string(); }

