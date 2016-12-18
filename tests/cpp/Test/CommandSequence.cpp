#include "CommandSequence.h"
#include "Factory.h"


const std::string CommandSequence::__type__( "sequence" );
REGISTRATION_OBJECT( CommandSequence );


std::shared_ptr<mg::Command> createCommand( const RapidJsonNode& json )
{
	auto type = json.node( "command" ).get<std::string>( "type" );
	auto command = Factory::shared().build<mg::Command>( type );
	if( command != nullptr )
		command->deserialize( json );
	return command;
}

namespace mg
{
	void Command::serialize( RapidJsonNode& json ) const
	{
		auto node = json.append_node( "command" );
		node.append_node( "id" ).set( id );
		node.append_node( "type" ).set( getType() );
	}

	void Command::deserialize( const RapidJsonNode& json )
	{
		id = json.node("command").get<int>( "id" );
	}

	std::string Command::getSerializedString() const
	{
		RapidJsonNode json;
		serialize( json );
		std::string string;
		json.toString( string );
		return string;
	}
}

std::string CommandSequence::getType()const
{
	return __type__;
}

void CommandSequence::serialize( RapidJsonNode& json )const
{
	Command::serialize( json );
	auto jsonObj = json.append_array( "commands" );
	for( auto& command : _list )
	{
		command->serialize( jsonObj.push_back() );
	}
}

void CommandSequence::deserialize( const RapidJsonNode& json )
{
	Command::deserialize( json );
	auto jsonObj = json.node( "commands" );
	auto size = jsonObj.size();
	for( size_t i = 0; i < size; ++i )
	{
		auto command = createCommand( jsonObj.at( i ) );
		assert( command );
		_list.push_back( command );
	}
}
