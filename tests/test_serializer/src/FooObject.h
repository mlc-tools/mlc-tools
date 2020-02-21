#ifndef __mg_FooObject_h__
#define __mg_FooObject_h__

#include "intrusive_ptr.h"
#include <string>

class SerializerXml;
class DeserializerXml;
class SerializerJson;
class DeserializerJson;

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
        virtual void serialize(SerializerXml& xml) const;
        virtual void deserialize(DeserializerXml& xml);
        virtual void serialize(SerializerJson& json) const;
        virtual void deserialize(DeserializerJson& json);
        bool operator < (const FooObject& rhs) const;

        int _reference_counter;
        int value;
        std::string name;
    };

    class BarObject : public FooObject
    {
    public:
        virtual std::string get_type() const override { return "BarObject"; }
        virtual void serialize(SerializerXml& xml) const override;
        virtual void deserialize(DeserializerXml& xml) override;
        virtual void serialize(SerializerJson& json) const override;
        virtual void deserialize(DeserializerJson& json) override;
        bool operator < (const BarObject& rhs) const;

        FooObject foo;
        intrusive_ptr<FooObject> foo_ptr = nullptr;
    };

} //namespace mg

#endif //#ifndef __mg_AllTypesChildren_h__
