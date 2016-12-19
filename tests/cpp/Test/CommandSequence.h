#ifndef __CommandSequence_h__
#define __CommandSequence_h__

#include "../../../out/Command.h"
#include "jsoncpp/json.h"
#include <memory>
#include <vector>

class CommandDelegate;

std::shared_ptr<mg::Command> createCommand( const Json::Value& json );

class CommandSequence : public mg::Command
{
public:
	static const std::string __type__;
	virtual std::string getType()const override;
	virtual void serialize( Json::Value& json )const override;
	virtual void deserialize( const Json::Value& json )override;
public:
	std::vector<std::shared_ptr<Command>> _list;
};


#endif