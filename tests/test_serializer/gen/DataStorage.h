#ifndef __mg_DataStorage_h__
#define __mg_DataStorage_h__

#include "intrusive_ptr.h"
#include "pugixml/pugixml.hpp"
#include "data/DataUnit.h"
#include "src/FooObject.h"
#include <map>
#include <string>

namespace mg
{
    class SerializerXml;
    class DeserializerXml;
    class SerializerJson;
    class DeserializerJson;
    class DataAdd;
    class DataComplexMap;
    class DataUnit;

    class DataStorage
    {
    public:
        DataStorage();
        ~DataStorage();
        static const DataStorage& shared();
        void initialize_xml(const std::string& content) const;
        void initialize_json(const std::string& content) const;
        template <class T> const T* get(const std::string& name) const;
        std::string get_type() const;
        void serialize_xml(SerializerXml& serializer) const;
        void deserialize_xml(DeserializerXml& deserializer);
        void serialize_json(SerializerJson& serializer) const;
        void deserialize_json(DeserializerJson& deserializer);

        std::map<std::string, DataUnit> units;
        std::map<std::string, FooObject> foo_objects;
    public:
        bool _loaded;
    public:
        static const std::string TYPE;

    };
} //namespace mg

#endif //#ifndef __mg_DataStorage_h__
