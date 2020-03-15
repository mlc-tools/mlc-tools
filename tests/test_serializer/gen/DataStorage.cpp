#include "intrusive_ptr.h"
#include "mg_Factory.h"
#include "DataStorage.h"
#include "data/DataUnit.h"
#include <string>
#include "mg_extensions.h"
#include "SerializerJson.h"
#include "SerializerXml.h"

namespace mg
{
    const std::string DataStorage::TYPE("DataStorage");

    DataStorage::DataStorage()
    : units()
    , _loaded(false)
    {

    }

    DataStorage::~DataStorage()
    {
    }

    const DataStorage& DataStorage::shared()
    {
        static DataStorage instance;
        return instance;
    }

    void DataStorage::initialize_xml(const std::string& content) const
    {
        pugi::xml_document doc;
        doc.load(content.c_str());
        pugi::xml_node node = doc.root().first_child();
        DeserializerXml deserializer(node);
        const_cast<DataStorage*>(this)->deserialize_xml(deserializer);
        const_cast<DataStorage*>(this)->_loaded = doc.root() != nullptr;
    }

    void DataStorage::initialize_json(const std::string& content) const
    {
        Json::Value json;
        Json::Reader reader;
        reader.parse(content, json);
        DeserializerJson deserializer(json);
        const_cast<DataStorage*>(this)->deserialize_json(deserializer);
        const_cast<DataStorage*>(this)->_loaded = true;
    }

    template<>const DataUnit* DataStorage::get(const std::string& name) const
    {
        return _loaded ? &units.at(name) : &const_cast<DataStorage*>(this)->units[name];
    }

    template<>const FooObject* DataStorage::get(const std::string& name) const
    {
        return _loaded ? &foo_objects.at(name) : &const_cast<DataStorage*>(this)->foo_objects[name];
    }

    std::string DataStorage::get_type() const
    {
        return DataStorage::TYPE;
    }

    void DataStorage::serialize_xml(SerializerXml& serializer) const
    {
//        serializer.serialize(units, "units");

    }

    void DataStorage::deserialize_xml(DeserializerXml& deserializer)
    {
//        deserializer.deserialize(units, "units");

    }

    void DataStorage::serialize_json(SerializerJson& serializer) const
    {
//        serializer.serialize(units, "units");

    }

    void DataStorage::deserialize_json(DeserializerJson& deserializer)
    {
//        deserializer.deserialize(units, "units");
    }

} //namespace mg
