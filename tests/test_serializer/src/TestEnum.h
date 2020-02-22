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

    class TestEnum
    {
    public:
        TestEnum();
        virtual ~TestEnum();
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
        operator int() const;
        operator std::string() const;
        std::string str() const;
        virtual void serialize(SerializerXml& xml) const;
        virtual void deserialize(DeserializerXml& xml);
        void serialize(SerializerJson& json) const;
        void deserialize(DeserializerJson& json);

        static constexpr int value1 = 0;
        static constexpr int value2 = 1;
    private:
        int value;

    };
} //namespace mg

#endif //#ifndef __mg_TestEnum_h__
