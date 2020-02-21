#ifndef __mg_FooObject_h__
#define __mg_FooObject_h__

#include "intrusive_ptr.h"
#include <string>

class Serializer;
class Deserializer;

namespace mg
{

    class FooObject
    {
    public:
        FooObject();
        virtual ~FooObject();
        void retain();
        int release();
        virtual std::string get_type() const;
        virtual void serialize(Serializer& xml) const;
        virtual void deserialize(Deserializer& xml);
        bool operator < (const FooObject& rhs) const;

        int _reference_counter;
        int value;
        std::string name;
    };

    class BarObject : public FooObject
    {
    public:
        virtual std::string get_type() const override { return "BarObject"; }
        virtual void serialize(Serializer& xml) const override;

        FooObject foo;
        intrusive_ptr<FooObject> foo_ptr = nullptr;
    };

} //namespace mg

#endif //#ifndef __mg_AllTypesChildren_h__
