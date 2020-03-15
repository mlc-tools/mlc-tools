#ifndef __mg_TestEnum_h__
#define __mg_TestEnum_h__

#include "intrusive_ptr.h"
#include <string>

class SerializerXml;
class DeserializerXml;
class SerializerJson;
class DeserializerJson;

namespace mg
{
    class BaseEnum
    {
    public:
        constexpr BaseEnum(int value_ = 0): value(value_) {}
        constexpr BaseEnum(const BaseEnum& rhs): value(rhs.value) {}
        constexpr operator int() const { return value; }
        virtual std::string str() const {assert(0 && "Override me"); return std::string(); }
    protected:
        int value;
    };

    class TestEnum : public BaseEnum
    {
    public:
        TestEnum();
        TestEnum(const BaseEnum& rhs):BaseEnum(rhs){}
        TestEnum(int _value);
        TestEnum(const TestEnum& rhs);
        TestEnum(const std::string& _value);
        const TestEnum& operator =(const TestEnum& rhs);
        const TestEnum& operator =(int rhs);
        const TestEnum& operator =(const std::string& _value);
        bool operator ==(const TestEnum& rhs) const;
        bool operator ==(int rhs) const;
        bool operator ==(const std::string& rhs) const;
        friend bool operator ==(const std::string& lhs, const TestEnum& rhs);
        bool operator <(const TestEnum& rhs) const;
        operator std::string() const;
        virtual std::string str() const;

        static constexpr BaseEnum value1 = 0;
        static constexpr BaseEnum value2 = 1;
    };
} //namespace mg

#endif //#ifndef __mg_TestEnum_h__
