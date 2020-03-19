#include "intrusive_ptr.h"
#include "mg_Factory.h"
#include "AllTypesChildren.h"
#include "mg_extensions.h"
#include "SerializerJson.h"
#include "SerializerXml.h"

namespace mg
{
    const std::string AllTypesChildren::TYPE("AllTypesChildren");

    AllTypesChildren::AllTypesChildren()
    : value(0)
    , _reference_counter(1)
    {

    }

    AllTypesChildren::~AllTypesChildren()
    {
    }

    bool AllTypesChildren::operator ==(const AllTypesChildren& rhs) const
    {
        bool result = true;
        result = result && this->value == rhs.value;
        return result;
    }

    bool AllTypesChildren::operator !=(const AllTypesChildren& rhs) const
    {
        return !(*this == rhs);
    }

    int AllTypesChildren::retain()
    {
        this->_reference_counter += 1;
        return this->_reference_counter;
    }

    int AllTypesChildren::release()
    {
        this->_reference_counter -= 1;
        auto c = this->_reference_counter;
        if( c == 0)
        {
            delete this;
        }
        return c;
    }

    std::string AllTypesChildren::get_type() const
    {
        return AllTypesChildren::TYPE;
    }

    void AllTypesChildren::serialize_xml(SerializerXml& serializer) const
    {
        serializer.serialize(value, "value", int(0));

    }

    void AllTypesChildren::deserialize_xml(DeserializerXml& deserializer)
    {
        deserializer.deserialize(value, "value", int(0));

    }

    void AllTypesChildren::serialize_json(SerializerJson& serializer) const
    {
        serializer.serialize(value, "value", int(0));

    }

    void AllTypesChildren::deserialize_json(DeserializerJson& deserializer)
    {
        deserializer.deserialize(value, "value", int(0));

    }

} //namespace mg
