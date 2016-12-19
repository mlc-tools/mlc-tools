#include "TestSerialization.h"
#include "TestSerializationCommandSequence.h"
#include "../../../out/RoutePoint.h"
#include "../../../out/BattleSystem.h"
#include "cocos2d.h"
#include "Factory.h"
#include "CommandSequence.h"
#include "Generics.h"
#include "../../../out/RequestAuthorize.h"
#include "../../../out/ResponseAuthorize.h"
#include "../../../out/IVisitorRequest.h"
#include "../../../out/IVisitorResponse.h"
#include "jsoncpp/json.h"

using namespace mg;


class VisitorRequest : public IVisitorRequest 
{
public:
	VisitorRequest() 
	{
	};

	virtual void visit( Request* ctx )
	{
	}

	virtual void visit( RequestCreateTower* ctx )
	{
	}

	virtual void visit( RequestAuthorize* ctx )
	{
	}

	virtual void visit( RequestCreateBonusItem* ctx )
	{
	}

	virtual void visit( RequestUpgradeTower* ctx )
	{
	}

	virtual void visit( RequestSellTower* ctx )
	{
	}

	virtual void visit( RequestLoadLevel* ctx )
	{
	}

	virtual void visit( RequestLoadedLevelData* ctx )
	{
	}

	virtual void visit( RequestStartLevel* ctx )
	{
	}

	virtual void visit( RequestStartWave* ctx )
	{
	}

	virtual void visit( RequestBreakLevel* ctx )
	{
	}

	virtual std::string getType() const
	{
		return "";
	}

};

class VisitorResponse : public IVisitorResponse
{
public:
	virtual std::string getType() const
	{
		return "";
	}
	virtual void visit( Response* ctx )
	{}

	virtual void visit( ResponseCreateTower* ctx )
	{}

	virtual void visit( ResponseAuthorize* ctx )
	{}

	virtual void visit( ResponseChangeLevelScore* ctx )
	{}

	virtual void visit( ResponseCreateCreep* ctx )
	{}

	virtual void visit( ResponseCreateBonusItem* ctx )
	{}

	virtual void visit( ResponseUpgradeTower* ctx )
	{}

	virtual void visit( ResponseRemoveUnit* ctx )
	{}

	virtual void visit( ResponseLevelData* ctx )
	{}

	virtual void visit( ResponseStartLevel* ctx )
	{}

	virtual void visit( ResponseFinishLevel* ctx )
	{}

	virtual void visit( ResponseWaveStarted* ctx )
	{}

	virtual void visit( ResponseWavePredelay* ctx )
	{}

	virtual void visit( ResponseWaveFinished* ctx )
	{}

	virtual void visit( ResponseAllWavesFinished* ctx )
	{}

	virtual void visit( ResponseBreakLevel* ctx )
	{}

	virtual void visit( ResponseCaptureTarget* ctx )
	{}

	virtual void visit( ResponseUnitsDeath* ctx )
	{}

	virtual void visit( ResponseSynchronizeTime* ctx )
	{}
};

cocos2d::Point RoutePoint::getDynamic()
{
	return cocos2d::Point();
}
void mg::BattleSystem::load( pugi::xml_node xml )
{
}

cocos2d::Point cocos2d::Point::ZERO;

int main()
{
	//Json::Value root;
	//root["123"][1] = 1;
	//
	//Json::StreamWriterBuilder wbuilder;
	//wbuilder["indentation"] = "";
	//wbuilder["slightly"] = " ";
	//auto str = Json::writeString( wbuilder, root );
	//std::cout << str;
	//
	//Json::Value value;
	//Json::Reader reader;
	//reader.parse( str, value );
	//std::cout << std::endl << value;
	//
	//float t;
	//if( value.isMember( "123" ) && value["123"].isArray() )
	//	t = strTo<float>( value["123"][0].asString() );
	//if( value.isMember( "1231" ) )
	//{
	//	std::cout << value["1231"].asFloat();
	//}
	//if( json.is_exist( "health" ) )
	//	health = json.get<float>( "health" );

	VisitorRequest visitor;
	VisitorResponse visitor2;

	//Command* command = new RequestAuthorize;
	//command->accept( &visitor );
	//
	//command = new ResponseAuthorize;
	//command->accept( &visitor2 );
	std::vector< std::shared_ptr<TestCase> > tests;
	tests.push_back( std::make_shared<TestSerializationCommandSequence>() );
	tests.push_back( std::make_shared<TestSerialization>() );
	bool result = true;
	for( auto test : tests )
	{
		result = test->execute() && result;
	}
	return result ? 0 : -1;

}