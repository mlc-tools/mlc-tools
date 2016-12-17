#ifndef __RapidJsonNode_h__
#define __RapidJsonNode_h__
#include <string>

typedef std::string string;

class RapidJsonNode
{
public:
	bool is_exist( const std::string& string )const;
	RapidJsonNode append_node( const std::string& string );
	
	template<class T>
	void set( const T& value );
	template<class T>
	T get( const std::string& name )const;
};

#endif