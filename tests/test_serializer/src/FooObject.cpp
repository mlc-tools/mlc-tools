#include "intrusive_ptr.h"
#include "FooObject.h"
#include "Serializer.h"

namespace mg
{
    FooObject::FooObject()
    : _reference_counter(1)
    , value(0)
    {

    }

    FooObject::~FooObject() = default;

    void FooObject::retain()
    {
        this->_reference_counter += 1;
    }

    int FooObject::release()
    {
        this->_reference_counter -= 1;
        auto counter = this->_reference_counter;
        if(counter == 0)
            delete this;
        return counter;
    }

    std::string FooObject::get_type() const
    {
        return "FooObject";
    }

    void FooObject::serialize(Serializer& serializer) const
    {
        serializer.serialize(value, "value", 0);
        serializer.serialize(name, "name", std::string(""));
    }
    void FooObject::deserialize(Deserializer& xml)
    {
        xml.deserialize(value, "value", 0);
        xml.deserialize(name, "name", std::string(""));
    }

    bool FooObject::operator<(const FooObject &rhs) const{
        return this < &rhs;
    }

    void BarObject::serialize(Serializer& serializer) const
    {
        FooObject::serialize(serializer);
        serializer.serialize(foo, "foo");
        serializer.serialize(foo_ptr, "foo_ptr");
    }

} //namespace mg
