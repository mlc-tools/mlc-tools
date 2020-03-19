#include "intrusive_ptr.h"
#include "../mg_Factory.h"
#include "../DataStorage.h"
#include "DataUnit.h"
#include <string>
#include "../mg_extensions.h"
#include "SerializerJson.h"
#include "SerializerXml.h"

namespace mg
{
    const std::string DataUnit::TYPE("DataUnit");

    DataUnit::DataUnit()
    : name("")
    , visual()
    , link_to_data(nullptr)
    , all_units()
    , map_units()
    , _reference_counter(1)
    {

    }

    DataUnit::~DataUnit()
    {
    }

    bool DataUnit::operator ==(const DataUnit& rhs) const
    {
        bool result = true;
        result = result && this->name == rhs.name;
        result = result && this->visual == rhs.visual;
        result = result && this->all_units == rhs.all_units;
        result = result && this->map_units == rhs.map_units;
        return result;
    }

    bool DataUnit::operator !=(const DataUnit& rhs) const
    {
        return !(*this == rhs);
    }

    bool DataUnit::operator < (const DataUnit& rhs) const
    {
        return this->name < rhs.name;
    }

    int DataUnit::retain()
    {
        this->_reference_counter += 1;
        return this->_reference_counter;
    }

    int DataUnit::release()
    {
        this->_reference_counter -= 1;
        auto c = this->_reference_counter;
        if( c == 0)
        {
            delete this;
        }
        return c;
    }

    std::string DataUnit::get_type() const
    {
        return DataUnit::TYPE;
    }

    void DataUnit::serialize_xml(SerializerXml& serializer) const
    {
        serializer.serialize(name, "name", std::string(""));
        serializer.serialize(visual, "visual");
        serializer.serialize(link_to_data, "link_to_data");
        serializer.serialize(all_units, "all_units");
        serializer.serialize(map_units, "map_units");

    }

    void DataUnit::deserialize_xml(DeserializerXml& deserializer)
    {
        deserializer.deserialize(name, "name", std::string(""));
        deserializer.deserialize(visual, "visual");
        deserializer.deserialize(link_to_data, "link_to_data");
        deserializer.deserialize(all_units, "all_units");
        deserializer.deserialize(map_units, "map_units");

    }

    void DataUnit::serialize_json(SerializerJson& serializer) const
    {
        serializer.serialize(name, "name", std::string(""));
        serializer.serialize(visual, "visual");
        serializer.serialize(link_to_data, "link_to_data");
        serializer.serialize(all_units, "all_units");
        serializer.serialize(map_units, "map_units");

    }

    void DataUnit::deserialize_json(DeserializerJson& deserializer)
    {
        deserializer.deserialize(name, "name", std::string(""));
        deserializer.deserialize(visual, "visual");
        deserializer.deserialize(link_to_data, "link_to_data");
        deserializer.deserialize(all_units, "all_units");
        deserializer.deserialize(map_units, "map_units");

    }

} //namespace mg
