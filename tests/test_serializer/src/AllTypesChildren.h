#ifndef __mg_AllTypesChildren_h__
#define __mg_AllTypesChildren_h__

#include "intrusive_ptr.h"
#include "../third/pugixml/pugixml.hpp"
#include <string>

namespace pugi
{
    class xml_node;
}
class Serializer;
class Deserializer;

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
        void serialize(Serializer& xml) const;
        void deserialize(Deserializer& xml);
        bool operator < (const AllTypesChildren& rhs) const;

        int value;
    private:
        int _reference_counter;
    public:
        static const std::string TYPE;

    };
} //namespace mg

#endif //#ifndef __mg_AllTypesChildren_h__
