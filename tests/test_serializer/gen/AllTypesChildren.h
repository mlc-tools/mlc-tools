#ifndef __mg_AllTypesChildren_h__
#define __mg_AllTypesChildren_h__

#include "intrusive_ptr.h"
#include "pugixml/pugixml.hpp"
#include <string>

namespace mg
{
    class SerializerXml;
    class DeserializerXml;
    class SerializerJson;
    class DeserializerJson;

    class AllTypesChildren
    {
    public:
        AllTypesChildren();
        ~AllTypesChildren();
        bool operator ==(const AllTypesChildren& rhs) const;
        bool operator !=(const AllTypesChildren& rhs) const;
        bool operator < (const AllTypesChildren& rhs) const {return this < &rhs;}
        int retain();
        int release();
        std::string get_type() const;
        void serialize_xml(SerializerXml& serializer) const;
        void deserialize_xml(DeserializerXml& deserializer);
        void serialize_json(SerializerJson& serializer) const;
        void deserialize_json(DeserializerJson& deserializer);

        int value;
        int _reference_counter;
        static const std::string TYPE;

    };
} //namespace mg

#endif //#ifndef __mg_AllTypesChildren_h__
