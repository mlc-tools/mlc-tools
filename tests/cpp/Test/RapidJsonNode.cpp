#include "RapidJsonNode.h"
#include "rapidjson/document.h"
#include "rapidjson/stringbuffer.h"
#include "rapidjson/writer.h"
#include <fstream>
#include "Generics.h"
#include "cocos2d.h"


void throw_error( const std::string& message )
{
	std::cout << std::endl << message;
	assert( 0 );
}


RapidJsonNode::RapidJsonNode()
	: _doc( nullptr )
	, _rootNode( nullptr )
	, _value( nullptr )
{
	_doc = std::make_shared<rapidjson::Document>();
	_value = &_doc->SetObject();
	_rootNode = this;
}

RapidJsonNode::RapidJsonNode( const std::string& jsonString )
	: RapidJsonNode()
{
	parse( jsonString );
}

RapidJsonNode::RapidJsonNode( const RapidJsonNode* node )
	: _doc(nullptr)
	, _rootNode( node->_rootNode )
	, _value( node->_value )
{
}

RapidJsonNode& RapidJsonNode::operator=(const RapidJsonNode&node)
{
	_doc = node._doc;
	_rootNode = node._rootNode;
	_value = node._value;
	return *this;
}

RapidJsonNode::~RapidJsonNode()
{
	_doc.reset();
}

void RapidJsonNode::__set( rapidjson::Value* value )
{
	_value = value;
}

RapidJsonNode RapidJsonNode::__append( const std::string& key, rapidjson::Type type )
{
	RapidJsonNode node( _rootNode );
	if( _rootNode->_doc )
	{
		auto& allocator = _rootNode->_doc->GetAllocator();
		rapidjson::Value name;
		name.SetString( key.c_str(), key.size(), allocator );
		_value->AddMember( name, rapidjson::Value( type ), allocator );
		node.__set( &(*_value)[key.c_str()] );
	}
	return node;
}

bool RapidJsonNode::is_exist( const std::string& key )const
{
	if( _value && _value->IsObject() )
	{
		auto iterMember = _value->FindMember( key.c_str() );
		return iterMember != _value->MemberEnd();
	}
	return false;
}

void RapidJsonNode::parse( const std::string& jsonString )
{
	if( _doc && jsonString.empty() == false && jsonString != "null" )
		_doc->Parse( jsonString.c_str() );
}

void RapidJsonNode::toString( std::string& jsonString )const
{
	if( _value )
	{
		rapidjson::StringBuffer buffer;
		rapidjson::Writer<rapidjson::StringBuffer> writer( buffer );
		_value->Accept( writer );
		jsonString = buffer.GetString();
	}
}

bool RapidJsonNode::saveFile( const std::string& file )const
{
	std::string jsonString;
	toString( jsonString );
	std::fstream fstream( file, std::fstream::out );
	if( fstream.is_open() )
		fstream << jsonString;
	return fstream.is_open();
}

bool RapidJsonNode::loadFile( const std::string& file )
{
	std::fstream fsteam( file, std::fstream::in );
	size_t size = 1024 * 1024 * 1024;
	char* buf = new char[size];
	fsteam.read( buf, size );
	parse( buf );
	delete buf;
	return true;
}

RapidJsonNode RapidJsonNode::append_node( const std::string& key )
{
	return __append( key, rapidjson::kObjectType );
}

RapidJsonNode RapidJsonNode::append_array( const std::string& key )
{
	return __append( key, rapidjson::kArrayType );
}

RapidJsonNode RapidJsonNode::push_back()
{
	assert( _rootNode->_doc );
	_value->PushBack( rapidjson::Value( rapidjson::kObjectType ), _rootNode->_doc->GetAllocator() );
	return node( this->size() - 1 );
}

RapidJsonNode RapidJsonNode::node( const std::string& key )
{
	RapidJsonNode node( *this );
	if( _value && _value->IsObject() )
	{
		auto iterMember = _value->FindMember( key.c_str() );
		if( iterMember != _value->MemberEnd() )
			node.__set( &(*_value)[key.c_str()] );
		else
			node.__set( nullptr );
	}
	return node;
}

RapidJsonNode RapidJsonNode::node( size_t index )
{
	RapidJsonNode node( *this );
	if( _value && _value->IsArray() )
	{
		if( index < _value->Size() )
			node.__set( &(*_value)[index] );
		else
			node.__set( nullptr );
	}
	return node;
}

RapidJsonNode RapidJsonNode::node( const std::string& key )const
{
	RapidJsonNode node( *this );
	if( _value && _value->IsObject() )
	{
		auto iterMember = _value->FindMember( key.c_str() );
		if( iterMember != _value->MemberEnd() )
			node.__set( &(*_value)[key.c_str()] );
		else
			node.__set( nullptr );
	}
	return node;
}

RapidJsonNode RapidJsonNode::node( size_t index )const
{
	RapidJsonNode node( *this );
	if( _value && _value->IsArray() )
	{
		if( index < _value->Size() )
			node.__set( &(*_value)[index] );
		else
			node.__set( nullptr );
	}
	return node;
}

template<> bool RapidJsonNode::set( int32_t value )
{
	if( _value ) _value->SetInt( value );
	return _value != nullptr;
}

template<> bool RapidJsonNode::set( uint32_t value )
{
	if( _value ) _value->SetUint( value );
	return _value != nullptr;
}

template<> bool RapidJsonNode::set( float value )
{
	if( _value ) _value->SetDouble( static_cast<double>(value) );
	return _value != nullptr;
}

template<> bool RapidJsonNode::set( std::string value )
{
	if( _rootNode->_doc )
	{
		auto& allocator = _rootNode->_doc->GetAllocator();
		if( _value ) _value->SetString( value.c_str(), value.size(), allocator );
		return _value != nullptr;
	}
	return false;
}

template<> bool RapidJsonNode::set( char const * value )
{
	return set<std::string>( value );
}

template<> bool RapidJsonNode::set( bool value )
{
	if( _value ) _value->SetBool( value );
	return _value != nullptr;
}

template<> bool RapidJsonNode::set( cocos2d::Point value )
{
	return set<std::string>( toStr( value ) );
}

template<> std::string RapidJsonNode::get( const std::string& key )const
{
	if( _value && _value->IsObject() && _value->FindMember( key.c_str() ) != _value->MemberEnd() )
		return (*_value)[key.c_str()].GetString();
	else
		return std::string();
}

template<> int32_t RapidJsonNode::get( const std::string& key )const
{
	if( _value && _value->IsObject() && _value->FindMember( key.c_str() ) != _value->MemberEnd() )
		return (*_value)[key.c_str()].GetInt();
	else
		return 0;
}

template<> uint32_t RapidJsonNode::get( const std::string& key )const
{
	if( _value && _value->IsObject() && _value->FindMember( key.c_str() ) != _value->MemberEnd() )
		return (*_value)[key.c_str()].GetUint();
	else
		return 0;
}

template<> float RapidJsonNode::get( const std::string& key )const
{
	if( _value && _value->IsObject() && _value->FindMember( key.c_str() ) != _value->MemberEnd() )
		return static_cast<float>((*_value)[key.c_str()].GetDouble());
	else
		return 0.f;
}

template<> bool RapidJsonNode::get( const std::string& key )const
{
	if( _value && _value->IsObject() && _value->FindMember( key.c_str() ) != _value->MemberEnd() )
		return (*_value)[key.c_str()].GetBool();
	else
		return false;
}

template<> cocos2d::Point RapidJsonNode::get( const std::string& key )const
{
	if( _value && _value->IsObject() && _value->FindMember( key.c_str() ) != _value->MemberEnd() )
		return strTo<cocos2d::Point>( (*_value)[key.c_str()].GetString() );
	else
		return cocos2d::Point();
}

template<> std::string RapidJsonNode::get( size_t index )const
{
	return _value && index < _value->Size() ? (*_value)[index].GetString() : std::string();
}

template<> int RapidJsonNode::get( size_t index )const
{
	return _value && index < _value->Size() ? (*_value)[index].GetInt() : 0;
}

template<> float RapidJsonNode::get( size_t index )const
{
	return _value && index < _value->Size() ? static_cast<float>((*_value)[index].GetDouble()) : 0.f;
}

template<> bool RapidJsonNode::get( size_t index )const
{
	return strTo<bool>( get<std::string>( index ) );
}

template<> cocos2d::Point RapidJsonNode::get( size_t index )const
{
	return strTo<cocos2d::Point>( get<std::string>( index ) );
}

bool RapidJsonNode::contain( const std::string & key ) const
{
	return _value && _value->IsObject() && _value->FindMember( key.c_str() ) != _value->MemberEnd();
}

RapidJsonNode::operator bool()const
{
	return _value != nullptr && !_value->IsNull();
}

bool RapidJsonNode::operator !()const
{
	return _value == nullptr || _value->IsNull();
}

bool RapidJsonNode::operator ==(const RapidJsonNode& node)const
{
	return _value == node._value;
}

size_t RapidJsonNode::size()const
{
	if( !_value )
		return 0;
	return
		_value->IsArray() ? _value->Size() :
		_value->IsObject() ? _value->MemberCount() :
		0;
}

RapidJsonNode RapidJsonNode::at( size_t index )const
{
	assert( _value );
	if( _value->IsArray() )
	{
		return node( index );
	}
	else if( _value->IsObject() )
	{
		auto iter = _value->MemberBegin() + index;
		return node( iter->name.GetString() );
	}
	return RapidJsonNode();
}
