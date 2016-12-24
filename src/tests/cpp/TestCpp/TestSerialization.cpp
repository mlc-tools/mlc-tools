#include "TestSerialization.h"
#include "../../../out/Command.cpp"
#include "../../../out/QuestTaskBase.cpp"
#include "../../../out/QuestTaskSimple.cpp"
#include "../../../out/QuestBase.cpp"


void TestSerialization::build()
{
_tests.push_back( new TestT<mg::Command> );
_tests.push_back( new TestT<mg::QuestTaskBase> );
_tests.push_back( new TestT<mg::QuestTaskSimple> );
_tests.push_back( new TestT<mg::QuestBase> );

}
