#ifndef __mg_VisualUnit_h__
#define __mg_VisualUnit_h__

#include "intrusive_ptr.h"
#include "pugixml/pugixml.hpp"
#include <string>

namespace mg
{
    class SerializerXml;
    class DeserializerXml;
    class SerializerBinary;
    class DeserializerBinary;

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
        void serialize_binary(SerializerBinary& serializer) const;
        void deserialize_binary(DeserializerBinary& deserializer);

        std::string name;
        std::string icon;
        int _reference_counter;
        static const std::string TYPE;

    };
} //namespace mg

#endif //#ifndef __mg_VisualUnit_h__
