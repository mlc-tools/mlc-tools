FACTORY_HPP = '''#ifndef __@{namespace}_Factory_h__
#define __@{namespace}_Factory_h__
#include <string>
#include <map>
#include <iostream>
#include <assert.h>
#include "intrusive_ptr.h"
#include "jsoncpp/json.h"
#include <sstream>
#include "pugixml/pugixml.hpp"

@{registration}
namespace @{namespace}
{

    class Factory
    {
        class IBuilder
        {
        public:
            virtual ~IBuilder() {}
            virtual void* build() = 0;
        };

        template<class TType>
        class Builder : public IBuilder
        {
        public:
            virtual void* build() override
            {
                return new TType();
            };
        };

        ~Factory()
        {
            for(auto& pair : _builders)
            {
                delete pair.second;
            }
            _builders.clear();
        }
    public:
        static Factory& shared()
        {
            static Factory instance;
            return instance;
        }

        template <class TType>
        void registrationCommand( const std::string & key )
        {
            if( _builders.find( key ) != _builders.end() )
            {
                std::cout <<std::endl <<"I already have object with key [" <<key <<"]";
            }
            assert( _builders.find( key ) == _builders.end() );
            _builders[key] = new Builder<TType>();
        };

        template <class TType>
        intrusive_ptr<TType> build( const std::string & key ) const
        {
            bool isreg = _builders.find( key ) != _builders.end();
            if( !isreg )
            {
                return nullptr;
            }
            auto builder = _builders.at(key);
            intrusive_ptr<TType> result(reinterpret_cast<TType*>(builder->build()));
            result->release();
            return result;
        }
    private:
        std::map<std::string, IBuilder*> _builders;
    };
}

#endif // __@{namespace}_Factory_h__
'''
FACTORY_REGISTRATION = '''
#define REGISTRATION_OBJECT(TType)                                      \\
class registration__##TType                                             \\
{                                                                       \\
public:                                                                 \\
    registration__##TType()                                             \\
    {                                                                   \\
        Factory::shared().registrationCommand<TType>(TType::TYPE);      \\
    }                                                                   \\
} ___registration___##TType;
'''