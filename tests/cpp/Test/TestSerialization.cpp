#include "TestSerialization.h"
#include "../../../out/Request.cpp"
#include "../../../out/Response.cpp"
#include "../../../out/RoutePoint.cpp"
#include "../../../out/Route.cpp"
#include "../../../out/TripleRoute.cpp"
#include "../../../out/BattleSystem.cpp"


void TestSerialization::build()
{
	_tests.push_back( new TestT<mg::Request> );
	_tests.push_back( new TestT<mg::Response> );
	_tests.push_back( new TestT<mg::RoutePoint> );
	_tests.push_back( new TestT<mg::Route> );
	_tests.push_back( new TestT<mg::TripleRoute> );
	_tests.push_back( new TestT<mg::BattleSystem> );

}
