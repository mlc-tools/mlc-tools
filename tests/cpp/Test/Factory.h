#ifndef __CommandFactory_h__
#define __CommandFactory_h__
#include <string>
#include <memory>
#include <map>
#include <iostream>
#include "../../../out/SerializedObject.h"
#include <assert.h>

#define REGISTRATION_OBJECT( T ) class registrator__##T {public: registrator__##T() { Factory::shared().registrationCommand<T>( T::__type__ ); } }___registrator__##T; 

void throw_error( const std::string& message );

typedef std::string string;



class Factory
{
	class IObject
	{
	public: virtual std::shared_ptr<mg::SerializedObject> build() = 0;
	};
	template<class T>
	class Object : public IObject
	{
	public: 
		virtual std::shared_ptr<mg::SerializedObject> build()
		{
			return std::static_pointer_cast<mg::SerializedObject>(std::make_shared<T>());
		};
	};
public:
	static Factory& shared()
	{
		static Factory instance;
		return instance;
	}

	template <class T>
	void registrationCommand( const std::string & key )
	{
		if( _builders.find( key ) != _builders.end() )
		{
			std::cout << std::endl << "I already have object with key [" << key << "]";
		}
		assert( _builders.find( key ) == _builders.end() );
		auto ptr = std::make_shared<Object<T>>();
		_builders[key] = ptr;
	};

	std::shared_ptr<mg::SerializedObject> build( const std::string & key )
	{
		bool isreg = _builders.find( key ) != _builders.end();
		if( !isreg )
			return nullptr;
		return isreg ? _builders[key]->build() : nullptr;
	}

	template < class T >
	std::shared_ptr<T> build( const std::string & key )
	{
		std::shared_ptr<mg::SerializedObject> ptr = build( key );
		std::shared_ptr<T> result = std::dynamic_pointer_cast<T>( ptr );
		return result;
	};

	template < class T >
	static std::shared_ptr<T> build()
	{
		auto result = std::make_shared<T>();
		return result;
	};
private:
	std::map< std::string, std::shared_ptr<IObject> > _builders;
};

#endif