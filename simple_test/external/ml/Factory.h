#ifndef __CommandFactory_h__
#define __CommandFactory_h__
#include <string>
#include "IntrusivePtr.h"
#include <map>
#include <iostream>
#include "SerializedObject.h"
#include <assert.h>

#define REGISTRATION_OBJECT( T ) class registrator__##T {public: registrator__##T() { Factory::shared().registrationCommand<T>( T::__type__ ); } }___registrator__##T; 

void throw_error( const std::string& message );

typedef std::string string;



class Factory
{
	class IObject : public mg::SerializedObject
	{
	public: virtual IntrusivePtr<mg::SerializedObject> build() = 0;
	};
	template<class T>
	class Object : public IObject
	{
	public: 
		virtual IntrusivePtr<mg::SerializedObject> build()
		{
			return dynamic_pointer_cast_intrusive<mg::SerializedObject>( make_intrusive<T>() );
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
		auto ptr = make_intrusive<Object<T>>();
		_builders[key] = ptr;
	};

	IntrusivePtr<mg::SerializedObject> build( const std::string & key )
	{
		bool isreg = _builders.find( key ) != _builders.end();
		if( !isreg )
			return nullptr;
		return isreg ? _builders[key]->build() : nullptr;
	}

	template < class T >
	IntrusivePtr<T> build( const std::string & key )
	{
		IntrusivePtr<mg::SerializedObject> ptr = build( key );
		IntrusivePtr<T> result = dynamic_pointer_cast_intrusive<T>( ptr );
		return result;
	};

	template < class T >
	static IntrusivePtr<T> build()
	{
		auto result = make_intrusive<T>();
		return result;
	};
private:
	std::map< std::string, IntrusivePtr<IObject> > _builders;
};

#endif