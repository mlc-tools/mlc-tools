#include "TestSerializationCommandSequence.h"
#include "CommandExtension.h"
#include "IntrusivePtr.h"

typedef std::string string;

#include "commands/Command.h"
#include "CommandSequence.h"

class Test
{
public:
	virtual IntrusivePtr<mg::Command> create() = 0;
	virtual bool compare( IntrusivePtr<mg::Command> command ) = 0;
	virtual void setCommand( IntrusivePtr<mg::Command> command ) = 0;
};

template<class T>
class TestT : public Test
{
public:
	virtual IntrusivePtr<mg::Command> create() override
	{
		return _create();
	}

	virtual bool compare( IntrusivePtr<mg::Command> arg ) override
	{
		auto c = std::dynamic_pointer_cast<T>(arg);
		return c != nullptr && *command == *c;
	}

	virtual void setCommand( IntrusivePtr<mg::Command> command )
	{
		this->command = command;
	}

	static IntrusivePtr<T> _create()
	{
		auto t = T::__create_instance__();
		auto p = make_intrusive<T>();
		*p = t;
		return p;
	}
	IntrusivePtr<mg::Command> command;
};

std::vector<Test*> tests;

bool TestSerializationCommandSequence::execute()
{
	mg::CommandSequence sequence;
	for( auto test : ::tests )
	{
		auto command = test->create();
		test->setCommand( command );
		sequence.commands.push_back( command );
	}
	auto str = sequence.getSerializedString();
	std::cout << std::endl << str;
	
	Json::Value json;
	Json::Reader reader;
	reader.parse( str, json );
	auto command = IntrusivePtr<mg::CommandSequence>( dynamic_cast<mg::CommandSequence*>(createCommand( json ).ptr()) );
	if( !command )
		return false;
	if( command->commands.size() != tests.size() )
		return false;
	int index( 0 );
	bool result = true;
	for( auto test : ::tests )
	{
		auto c = command->commands[index++];
		result = test->compare(c) && result;
	}
	return result;
}
