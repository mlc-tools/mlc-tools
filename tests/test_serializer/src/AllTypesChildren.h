#ifndef __mg_AllTypesChildren_h__
#define __mg_AllTypesChildren_h__

#include "intrusive_ptr.h"
#include <string>

class SerializerXml;
class DeserializerXml;
class SerializerJson;
class DeserializerJson;

namespace mg
{

    class AllTypesChildren
    {
    public:
        AllTypesChildren();
        ~AllTypesChildren();
        bool operator ==(const AllTypesChildren& rhs) const;
        bool operator !=(const AllTypesChildren& rhs) const;
        void retain();
        int release();
        std::string get_type() const;
        void serialize(SerializerXml& xml) const;
        void deserialize(DeserializerXml& xml);
        void serialize(SerializerJson& json) const;
        void deserialize(DeserializerJson& json);
        bool operator < (const AllTypesChildren& rhs) const;

        int value;
    private:
        int _reference_counter;
    public:
        static const std::string TYPE;

    };
} //namespace mg

#endif //#ifndef __mg_AllTypesChildren_h__
