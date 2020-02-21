#include "intrusive_ptr.h"
#include "AllTypesChildren.h"
#include "../third/pugixml/pugixml.hpp"
#include "Serializer.h"

namespace mg
{
    const std::string AllTypesChildren::TYPE("AllTypesChildren");

    AllTypesChildren::AllTypesChildren()
    : value(0)
    , _reference_counter(1)
    {

    }

    AllTypesChildren::~AllTypesChildren()
    {
    }

    bool AllTypesChildren::operator ==(const AllTypesChildren& rhs) const
    {
        if(this == &rhs){
            return true;
        }
        bool result = true;
        result = result && this->value == rhs.value;
        return result;
    }

    bool AllTypesChildren::operator !=(const AllTypesChildren& rhs) const
    {
        return !(*this == rhs);
    }

    void AllTypesChildren::retain()
    {
        this->_reference_counter += 1;
    }

    int AllTypesChildren::release()
    {
        this->_reference_counter -= 1;
        auto counter = this->_reference_counter;
        if(counter == 0)
        delete this;
        return counter;
    }

    std::string AllTypesChildren::get_type() const
    {
        return AllTypesChildren::TYPE;
    }

    void AllTypesChildren::serialize(Serializer& xml) const
    {
        xml.serialize(value, "value", 0);
    }

    void AllTypesChildren::deserialize(Deserializer& xml)
    {
        xml.deserialize(value, "value", 0);
    }

    bool AllTypesChildren::operator<(const AllTypesChildren &rhs) const{
        return this < &rhs;
    }

} //namespace mg
