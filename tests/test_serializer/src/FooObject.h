#ifndef __mg_FooObject_h__
#define __mg_FooObject_h__

#include "intrusive_ptr.h"
#include <string>

namespace mg
{
    class SerializerXml;
    class DeserializerXml;
    class SerializerJson;
    class DeserializerJson;

    class FooObject
    {
    public:
        FooObject();
        virtual ~FooObject();
        void retain();
        int release();
        virtual std::string get_type() const;
        virtual void serialize_xml(SerializerXml& xml) const;
        virtual void deserialize_xml(DeserializerXml& xml);
        virtual void serialize_json(SerializerJson& json) const;
        virtual void deserialize_json(DeserializerJson& json);
        bool operator < (const FooObject& rhs) const;

        int _reference_counter;
        int value;
        std::string name;
    };

    class BarObject : public FooObject
    {
    public:
        virtual std::string get_type() const override { return "BarObject"; }
        virtual void serialize_xml(SerializerXml& xml) const override;
        virtual void deserialize_xml(DeserializerXml& xml) override;
        virtual void serialize_json(SerializerJson& json) const override;
        virtual void deserialize_json(DeserializerJson& json) override;
        bool operator < (const BarObject& rhs) const;

        FooObject foo;
        intrusive_ptr<FooObject> foo_ptr = nullptr;
    };

} //namespace mg

#endif //#ifndef __mg_AllTypesChildren_h__
