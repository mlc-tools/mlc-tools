#include "intrusive_ptr.h"
#include "../mg_Factory.h"
#include "VisualUnit.h"
#include "../mg_extensions.h"
#include "SerializerJson.h"
#include "SerializerXml.h"

namespace mg
{
    const std::string VisualUnit::TYPE("VisualUnit");

    VisualUnit::VisualUnit()
    : name("")
    , icon("")
    , _reference_counter(1)
    {

    }

    VisualUnit::~VisualUnit()
    {
    }

    bool VisualUnit::operator ==(const VisualUnit& rhs) const
    {
        bool result = true;
        result = result && this->name == rhs.name;
        result = result && this->icon == rhs.icon;
        return result;
    }

    bool VisualUnit::operator !=(const VisualUnit& rhs) const
    {
        return !(*this == rhs);
    }

    int VisualUnit::retain()
    {
        this->_reference_counter += 1;
        return this->_reference_counter;
    }

    int VisualUnit::release()
    {
        this->_reference_counter -= 1;
        auto c = this->_reference_counter;
        if( c == 0)
        {
            delete this;
        }
        return c;
    }

    std::string VisualUnit::get_type() const
    {
        return VisualUnit::TYPE;
    }

    void VisualUnit::serialize_xml(SerializerXml& serializer) const
    {
        serializer.serialize(name, "name", std::string(""));
        serializer.serialize(icon, "icon", std::string(""));

    }

    void VisualUnit::deserialize_xml(DeserializerXml& deserializer)
    {
        deserializer.deserialize(name, "name", std::string(""));
        deserializer.deserialize(icon, "icon", std::string(""));

    }

    void VisualUnit::serialize_json(SerializerJson& serializer) const
    {
        serializer.serialize(name, "name", std::string(""));
        serializer.serialize(icon, "icon", std::string(""));

    }

    void VisualUnit::deserialize_json(DeserializerJson& deserializer)
    {
        deserializer.deserialize(name, "name", std::string(""));
        deserializer.deserialize(icon, "icon", std::string(""));

    }

} //namespace mg
