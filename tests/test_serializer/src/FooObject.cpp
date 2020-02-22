#include "intrusive_ptr.h"
#include "FooObject.h"
#include "serialize/SerializerXml.h"
#include "serialize/SerializerJson.h"

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

    void FooObject::serialize(SerializerXml& serializer) const
    {
        serializer.serialize(value, "value", 0);
        serializer.serialize(name, "name", std::string(""));
    }
    void FooObject::deserialize(DeserializerXml& xml)
    {
        xml.deserialize(value, "value", 0);
        xml.deserialize(name, "name", std::string(""));
    }
    void FooObject::serialize(SerializerJson& json) const
    {
        json.serialize(value, "value", 0);
        json.serialize(name, "name", std::string(""));
    }
    void FooObject::deserialize(DeserializerJson& json)
    {
        json.deserialize(value, "value", 0);
        json.deserialize(name, "name", std::string(""));
    }

    bool FooObject::operator<(const FooObject &rhs) const{
        return this < &rhs;
    }
    
    void BarObject::serialize(SerializerXml& serializer) const
    {
        FooObject::serialize(serializer);
        serializer.serialize(foo, "foo");
        serializer.serialize(foo_ptr, "foo_ptr");
    }

    void BarObject::deserialize(DeserializerXml& deserializer)
    {
        FooObject::deserialize(deserializer);
        deserializer.deserialize(foo, "foo");
        deserializer.deserialize(foo_ptr, "foo_ptr");
    }
    void BarObject::serialize(SerializerJson& json) const
    {
        
    }
    void BarObject::deserialize(DeserializerJson& json)
    {
        FooObject::deserialize(json);
        json.deserialize(foo, "foo");
        json.deserialize(foo_ptr, "foo_ptr");
    }
    
    bool BarObject::operator<(const BarObject &rhs) const{
        return this < &rhs;
    }

} //namespace mg
