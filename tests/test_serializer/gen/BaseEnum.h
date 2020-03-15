#ifndef __mg_BaseEnum_h__
#define __mg_BaseEnum_h__

#include <string>

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
}

#endif