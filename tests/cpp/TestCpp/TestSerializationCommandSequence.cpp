#include "TestSerializationCommandSequence.h"
#include "CommandSequence.h"

typedef std::string string;

#include "../../../out/Command.h"
#include "../../../out/ResponseChangeLevelScore.h"
#include "../../../out/ResponseCreateCreep.h"
#include "../../../out/ResponseCreateBonusItem.h"
#include "../../../out/RequestLoadLevel.h"
#include "../../../out/ResponseFinishLevel.h"
#include "../../../out/ResponseWaveStarted.h"
#include "../../../out/ResponseWavePredelay.h"
#include "../../../out/ResponseWaveFinished.h"
#include "../../../out/ResponseAllWavesFinished.h"
#include "../../../out/ResponseBreakLevel.h"
#include "../../../out/ResponseCaptureTarget.h"
#include "../../../out/ResponseUnitsDeath.h"
#include "../../../out/ResponseSynchronizeTime.h"
#include "../../../out/Request.h"
#include "../../../out/Response.h"
#include "../../../out/RequestCreateTower.h"
#include "../../../out/ResponseCreateTower.h"
#include "../../../out/RequestAuthorize.h"
#include "../../../out/ResponseAuthorize.h"
#include "../../../out/RequestCreateBonusItem.h"
#include "../../../out/RequestUpgradeTower.h"
#include "../../../out/ResponseUpgradeTower.h"
#include "../../../out/RequestSellTower.h"
#include "../../../out/ResponseRemoveUnit.h"
#include "../../../out/RequestLoadedLevelData.h"
#include "../../../out/ResponseLevelData.h"
#include "../../../out/RequestStartLevel.h"
#include "../../../out/ResponseStartLevel.h"
#include "../../../out/RequestStartWave.h"
#include "../../../out/RequestBreakLevel.h"

class Test
{
public:
	virtual std::shared_ptr<mg::Command> create() = 0;
	virtual bool compare( std::shared_ptr<mg::Command> command ) = 0;
	virtual void setCommand( std::shared_ptr<mg::Command> command ) = 0;
};

template<class T>
class TestT : public Test
{
public:
	virtual std::shared_ptr<mg::Command> create() override
	{
		return _create();
	}

	virtual bool compare( std::shared_ptr<mg::Command> arg ) override
	{
		auto c = std::dynamic_pointer_cast<T>(arg);
		return c != nullptr && *command == *c;
	}

	virtual void setCommand( std::shared_ptr<mg::Command> command )
	{
		this->command = command;
	}

	static std::shared_ptr<T> _create()
	{
		auto t = T::__create_instance__();
		auto p = std::make_shared<T>();
		*p = t;
		return p;
	}
	std::shared_ptr<mg::Command> command;
};

std::vector<Test*> tests;

bool TestSerializationCommandSequence::execute()
{
	tests.push_back( new ::TestT<mg::Command> );
	tests.push_back( new ::TestT<mg::ResponseChangeLevelScore> );
	tests.push_back( new ::TestT<mg::ResponseCreateCreep> );
	tests.push_back( new ::TestT<mg::ResponseCreateBonusItem> );
	tests.push_back( new ::TestT<mg::RequestLoadLevel> );
	tests.push_back( new ::TestT<mg::ResponseFinishLevel> );
	tests.push_back( new ::TestT<mg::ResponseWaveStarted> );
	tests.push_back( new ::TestT<mg::ResponseWavePredelay> );
	tests.push_back( new ::TestT<mg::ResponseWaveFinished> );
	tests.push_back( new ::TestT<mg::ResponseAllWavesFinished> );
	tests.push_back( new ::TestT<mg::ResponseBreakLevel> );
	tests.push_back( new ::TestT<mg::ResponseCaptureTarget> );
	tests.push_back( new ::TestT<mg::ResponseUnitsDeath> );
	tests.push_back( new ::TestT<mg::ResponseSynchronizeTime> );
	tests.push_back( new ::TestT<mg::Request> );
	tests.push_back( new ::TestT<mg::Response> );
	tests.push_back( new ::TestT<mg::RequestCreateTower> );
	tests.push_back( new ::TestT<mg::ResponseCreateTower> );
	tests.push_back( new ::TestT<mg::RequestAuthorize> );
	tests.push_back( new ::TestT<mg::ResponseAuthorize> );
	tests.push_back( new ::TestT<mg::RequestCreateBonusItem> );
	tests.push_back( new ::TestT<mg::RequestUpgradeTower> );
	tests.push_back( new ::TestT<mg::ResponseUpgradeTower> );
	tests.push_back( new ::TestT<mg::RequestSellTower> );
	tests.push_back( new ::TestT<mg::ResponseRemoveUnit> );
	tests.push_back( new ::TestT<mg::RequestLoadedLevelData> );
	tests.push_back( new ::TestT<mg::ResponseLevelData> );
	tests.push_back( new ::TestT<mg::RequestStartLevel> );
	tests.push_back( new ::TestT<mg::ResponseStartLevel> );
	tests.push_back( new ::TestT<mg::RequestStartWave> );
	tests.push_back( new ::TestT<mg::RequestBreakLevel> );


	CommandSequence sequence;
	for( auto test : ::tests )
	{
		auto command = test->create();
		test->setCommand( command );
		sequence._list.push_back( command );
	}
	auto str = sequence.getSerializedString();
	std::cout << std::endl << str;
	Json::Value json;
	Json::Reader reader;
	reader.parse( str, json );
	auto command = std::dynamic_pointer_cast<CommandSequence> (createCommand( json ));
	
	if( !command )
		return false;
	if( command->_list.size() != tests.size() )
		return false;
	
	int index( 0 );
	bool result = true;
	for( auto test : ::tests )
	{
		auto c = command->_list[index++];
		result = test->compare(c) && result;
	}
	return result;
}
