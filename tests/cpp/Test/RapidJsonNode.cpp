#include "RapidJsonNode.h"


bool RapidJsonNode::is_exist( const std::string& string )const
{
	return true;
}

RapidJsonNode RapidJsonNode::append_node( const std::string& string )
{
	return RapidJsonNode();
}

template <> void RapidJsonNode::set( const int& value )
{}
template <> void RapidJsonNode::set( const bool& value )
{}
template <> void RapidJsonNode::set( const float& value )
{}
template <> void RapidJsonNode::set( const std::string& value )
{}

template <> int RapidJsonNode::get( const std::string& name )const
{
	return 0;
}
template <> bool RapidJsonNode::get( const std::string& name )const
{
	return false;
}
template <> float RapidJsonNode::get( const std::string& name )const
{
	return 0.f;
}
template <> std::string RapidJsonNode::get( const std::string& name )const
{
	return "";
}
