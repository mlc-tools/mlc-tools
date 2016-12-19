#include "CommandSequence.h"
#include "Factory.h"


const std::string CommandSequence::__type__( "sequence" );
REGISTRATION_OBJECT( CommandSequence );


std::shared_ptr<mg::Command> createCommand( const Json::Value& json )
{
	auto type = json["command"]["type"].asString();
	auto command = Factory::shared().build<mg::Command>( type );
	if( command != nullptr )
		command->deserialize( json );
	return command;
	return nullptr;
}

namespace mg
{
	void Command::serialize( Json::Value& json ) const
	{
		auto& node = json["command"];
		node["id"] = id;
		node["type"] = getType();
	}

	void Command::deserialize( const Json::Value& json )
	{
		id = json["command"]["id"].asInt();
	}

	std::string Command::getSerializedString() const
	{
		Json::Value json;
		serialize( json );

		Json::StreamWriterBuilder wbuilder;
		//wbuilder["indentation"] = "";
		auto string = Json::writeString( wbuilder, json );

		return string;
	}
}

std::string CommandSequence::getType()const
{
	return __type__;
}

void CommandSequence::serialize( Json::Value& json )const
{
	Command::serialize( json );
	auto& jsonObj = json["commands"];
	for( auto& command : _list )
	{
		command->serialize( jsonObj[jsonObj.size()] );
	}
}

void CommandSequence::deserialize( const Json::Value& json )
{
	Command::deserialize( json );
	auto& jsonObj = json["commands"];
	auto size = jsonObj.size();
	for( size_t i = 0; i < size; ++i )
	{
		auto command = createCommand( jsonObj[i] );
		assert( command );
		_list.push_back( command );
	}
}
