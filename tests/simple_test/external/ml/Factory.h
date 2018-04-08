/******************************************************************************/
/*
* Copyright 2014-2017 Vladimir Tolmachev
*
* Author: Vladimir Tolmachev
* Project: ml
* e-mail: tolm_vl@hotmail.com
* If you received the code is not the author, please contact me
*/
/******************************************************************************/

#ifndef __CommandFactory_h__
#define __CommandFactory_h__
#include <string>
#include "IntrusivePtr.h"
#include <map>
#include <iostream>
#include "SerializedObject.h"
#include "config.h"
#include <assert.h>

#if MG_SERIALIZE_FORMAT == MG_JSON
#	include "jsoncpp/json.h"
#else
#	include <sstream>
#endif

#define REGISTRATION_OBJECT( T ) class registrator__##T {public: registrator__##T() { Factory::shared().registrationCommand<T>( T::TYPE ); } }___registrator__##T;

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

	template <class T>
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

#if MG_SERIALIZE_FORMAT == MG_JSON
	static std::string serialize_command(intrusive_ptr<mg::SerializedObject> command){
		Json::Value json;
		command->serialize(json[command->get_type()]);
		
		Json::StreamWriterBuilder wbuilder;
		wbuilder["indentation"] = "";
		return Json::writeString(wbuilder, json);
	}
	static intrusive_ptr<mg::SerializedObject> create_command(const std::string& payload){
		Json::Value json;
		Json::Reader reader;
		reader.parse(payload, json);
		
		auto type = json.getMemberNames()[0];
		auto command = Factory::shared().build<mg::SerializedObject>(type);
		if (command != nullptr)
			command->deserialize(json[type]);
		return command;
	}
#else
	static std::string serialize_command(intrusive_ptr<mg::SerializedObject> command){
		pugi::xml_document doc;
		auto root = doc.append_child(command->get_type().c_str());
		command->serialize(root);
		
		std::stringstream stream;
		pugi::xml_writer_stream writer(stream);
		doc.save(writer, "", pugi::format_no_declaration | pugi::format_raw, pugi::xml_encoding::encoding_utf8);
		return stream.str();
	}
	static intrusive_ptr<mg::SerializedObject> create_command(const std::string& payload){
		pugi::xml_document doc;
		doc.load(payload.c_str());
		auto root = doc.root().first_child();
		auto command = Factory::shared().build<mg::SerializedObject>(root.name());
		command->deserialize(root);
		return command;
	}
#endif
	
private:
	std::map< std::string, IntrusivePtr<IObject> > _builders;
};

#endif
