
#include <cstdlib>
#include <sstream>
#include <vector>
#include "mg_extensions.h"

namespace mg
{
    float random_float()
    {
        return std::rand() / static_cast<float>(RAND_MAX);
    }

    int random_int(int min, int max)
    {
        auto diff = max - min;
        if(diff > 0)
        {
            return std::rand() % diff + min;
        }
        return min;
    }

    bool string_empty(const std::string& string)
    {
        return string.empty();
    }

    int string_size(const std::string& string)
    {
        return static_cast<int>(string.size());
    }

    std::string boolToStr(bool value)
    {
        return value ? "yes" : "no";
    };

    std::string intToStr(int value)
    {
        std::stringstream ss;
        ss << value;
        return ss.str();
    };

    std::string floatToStr(float value)
    {
        std::stringstream ss;
        ss.precision(5);
        ss << value;
        return ss.str();
    };

    bool strToBool(const std::string& value)
    {
        if (value.empty())
            return false;
        bool result(false);
        result = result || value == "yes";
        result = result || value == "Yes";
        result = result || value == "true";
        result = result || value == "True";
        return result;
    }

    int strToInt(const std::string& value)
    {
        std::stringstream ss(value);
        int result(0);
        ss >> result;
        return result;
    }

    float strToFloat(const std::string& value)
    {
        std::stringstream ss(value);
        float result(0.f);
        ss >> result;
        return result;
    }

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

    //XML
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

    //JSON
//    template <> void set( Json::Value& json, int8_t value ) { json = value; }
//    template <> void set( Json::Value& json, int16_t value ) { json = value; }
//    template <> void set( Json::Value& json, int32_t value ) { json = value; }
//    template <> void set( Json::Value& json, int64_t value ) { json = value; }
//    template <> void set( Json::Value& json, uint8_t value ) { json = value; }
//    template <> void set( Json::Value& json, uint16_t value ) { json = value; }
//    template <> void set( Json::Value& json, uint32_t value ) { json = value; }
//    template <> void set( Json::Value& json, uint64_t value ) { json = value; }
//    template <> void set( Json::Value& json, bool value ) { json = value; }
//    template <> void set( Json::Value& json, float value ) { json = value; }
//    template <> void set( Json::Value& json, std::string value ) { json = value; }
//
//    template <> int8_t get( const Json::Value& json ) { return json.asInt(); }
//    template <> int16_t get( const Json::Value& json ) { return json.asInt(); }
//    template <> int32_t get( const Json::Value& json ) { return json.asInt(); }
//    template <> int64_t get( const Json::Value& json ) { return json.asInt64(); }
//    template <> uint8_t get( const Json::Value& json ) { return json.asUInt(); }
//    template <> uint16_t get( const Json::Value& json ) { return json.asUInt(); }
//    template <> uint32_t get( const Json::Value& json ) { return json.asUInt(); }
//    template <> uint64_t get( const Json::Value& json ) { return json.asUInt64(); }
//    template <> bool get( const Json::Value& json ) { return json.asBool(); }
//    template <> float get( const Json::Value& json ) { return json.asFloat(); }
//    template <> std::string get( const Json::Value& json ) { return json.asString(); }

    std::string format(const char *fmt, ...)
    {
        va_list args;
        va_start(args, fmt);
        std::vector<char> v(1024);
        while (true)
        {
            va_list args2;
            va_copy(args2, args);
            int res = vsnprintf(v.data(), v.size(), fmt, args2);
            if ((res >= 0) && (res < static_cast<int>(v.size())))
            {
                va_end(args);
                va_end(args2);
                return std::string(v.data());
            }
            size_t size;
            if (res < 0)
                size = v.size() * 2;
            else
                size = static_cast<size_t>(res) + 1;
            v.clear();
            v.resize(size);
            va_end(args2);
        }
    }
}

