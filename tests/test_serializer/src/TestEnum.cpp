#include "intrusive_ptr.h"
#include "TestEnum.h"
#include "../third/pugixml/pugixml.hpp"
#include "Serializer.h"

namespace mg
{
    const int TestEnum::value1;
    const int TestEnum::value2;

    TestEnum::TestEnum()
    : value(value1)
    {

    }

    TestEnum::~TestEnum()
    {
    }

    TestEnum::TestEnum(int _value)
    {
        value = _value;
    }

    TestEnum::TestEnum(const TestEnum& rhs)
    {
        value = rhs.value;
    }

    TestEnum::TestEnum(const std::string& _value)
    {
        if(_value == "value1")
        {
            value = value1;
            return;
        }
        if(_value == "value2")
        {
            value = value2;
            return;
        }
        value = 0;
    }

    const TestEnum& TestEnum::operator =(const TestEnum& rhs)
    {
        value = rhs.value;
        return *this;
    }

    const TestEnum& TestEnum::operator =(int rhs)
    {
        value = rhs;
        return *this;
    }

    const TestEnum& TestEnum::operator =(const std::string& _value)
    {
        if(_value == "value1")
        {
            value = value1;
            return *this;
        }
        if(_value == "value2")
        {
            value = value2;
            return *this;
        }
        return *this;
    }

    bool TestEnum::operator ==(const TestEnum& rhs) const
    {
        return value == rhs.value;
    }

    bool TestEnum::operator ==(int rhs) const
    {
        return value == rhs;
    }

    bool TestEnum::operator ==(const std::string& rhs) const
    {
        return *this == TestEnum(rhs);
    }

    bool operator ==(const std::string& lhs, const TestEnum& rhs)
    {
        return TestEnum(lhs) == rhs;
    }

    bool TestEnum::operator <(const TestEnum& rhs) const
    {
        return value < rhs.value;
    }

    TestEnum::operator int() const
    {
        return value;
    }

    TestEnum::operator std::string() const
    {
        if(value == value1)
        {
            return "value1";
        }
        if(value == value2)
        {
            return "value2";
        }
        return std::string();
    }

    std::string TestEnum::str() const
    {
        if(value == value1)
        {
            return "value1";
        }
        if(value == value2)
        {
            return "value2";
        }
        return std::string();
    }

    void TestEnum::serialize(Serializer& xml) const
    {
        xml.serialize(str(), "value", std::string(""));
    }

    void TestEnum::deserialize_xml(const pugi::xml_node& xml)
    {
        value = xml.attribute("value").as_int(value1);

    }

} //namespace mg
