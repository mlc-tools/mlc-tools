#ifndef __RapidJson_h__
#define __RapidJson_h__
#include "rapidjson/document.h"
#include <memory>
#include <math.h>
#include <algorithm>
#include <iostream>
#include <string>

void throw_error( const std::string& message );

typedef std::string string;

class RapidJsonNode
{
public:
	RapidJsonNode();
	RapidJsonNode( const std::string& jsonString );
	RapidJsonNode( const RapidJsonNode* );
	~RapidJsonNode();
	RapidJsonNode& operator=(const RapidJsonNode&);
private:
	void __set( rapidjson::Value* value );
	RapidJsonNode __append( const std::string& key, rapidjson::Type type );
public:
	bool is_exist( const std::string& key )const;
	void parse( const std::string& jsonString );
	void toString( std::string& jsonString )const;
	bool saveFile( const std::string& file )const;
	bool loadFile( const std::string& file );

	RapidJsonNode append_node( const std::string& key );
	RapidJsonNode append_array( const std::string& key );
	RapidJsonNode push_back();

	RapidJsonNode node( const std::string& key );
	RapidJsonNode node( size_t index );
	RapidJsonNode node( const std::string& key )const;
	RapidJsonNode node( size_t index )const;

	template< class T> bool set( T value );

	template< class T> T get( const std::string& key)const;
	template< class T> T get( size_t index )const;
	template< class T> T operator[]( const std::string& key )const { return get<T>( key ); }
	template< class T> T operator[]( size_t index )const { return get<T>( index ); }

	bool contain( const std::string & key ) const;

	operator bool()const;
	bool operator !()const;
	bool operator == (const RapidJsonNode& node)const;

	size_t size()const;
	RapidJsonNode at( size_t index )const;
private:
	std::shared_ptr<rapidjson::Document> _doc;
	RapidJsonNode const* _rootNode;
	rapidjson::Value *_value;
};

#endif
