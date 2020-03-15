#ifndef __mg_DataUnit_h__
#define __mg_DataUnit_h__

#include "intrusive_ptr.h"
#include "pugixml/pugixml.hpp"
#include "VisualUnit.h"
#include <map>
#include <string>
#include <vector>

namespace mg
{
    class SerializerXml;
    class DeserializerXml;
    class SerializerJson;
    class DeserializerJson;
    class Logger;

    class DataUnit
    {
    public:
        DataUnit();
        ~DataUnit();
        bool operator ==(const DataUnit& rhs) const;
        bool operator !=(const DataUnit& rhs) const;
        int retain();
        int release();
        std::string get_type() const;
        void serialize_xml(SerializerXml& serializer) const;
        void deserialize_xml(DeserializerXml& deserializer);
        void serialize_json(SerializerJson& serializer) const;
        void deserialize_json(DeserializerJson& deserializer);

        std::string name;
        VisualUnit visual;
        const DataUnit* link_to_data;
        std::vector<const DataUnit*> all_units;
        std::map<std::string, int> map_units;
        int _reference_counter;
        static const std::string TYPE;

    };
} //namespace mg

#endif //#ifndef __mg_DataUnit_h__
