#include "CommandExtension.h"
#include "Factory.h"


IntrusivePtr<mg::Command> createCommand( const Json::Value& json )
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

