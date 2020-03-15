#ifndef __mg_VisualUnit_h__
#define __mg_VisualUnit_h__

#include "intrusive_ptr.h"
#include "pugixml/pugixml.hpp"
#include <string>

namespace mg
{
    class SerializerXml;
    class DeserializerXml;
    class SerializerJson;
    class DeserializerJson;

    class VisualUnit
    {
    public:
        VisualUnit();
        ~VisualUnit();
        bool operator ==(const VisualUnit& rhs) const;
        bool operator !=(const VisualUnit& rhs) const;
        int retain();
        int release();
        std::string get_type() const;
        void serialize_xml(SerializerXml& serializer) const;
        void deserialize_xml(DeserializerXml& deserializer);
        void serialize_json(SerializerJson& serializer) const;
        void deserialize_json(DeserializerJson& deserializer);

        std::string name;
        std::string icon;
        int _reference_counter;
        static const std::string TYPE;

    };
} //namespace mg

#endif //#ifndef __mg_VisualUnit_h__
