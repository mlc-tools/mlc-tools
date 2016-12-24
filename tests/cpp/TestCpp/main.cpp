#include "TestSerialization.h"
#include "TestSerializationCommandSequence.h"
#include "cocos2d.h"
#include "Factory.h"
#include "Generics.h"
#include "jsoncpp/json.h"
#include "QuestBase.h"
#include "QuestTaskBase.h"
#include "Model.h"
#include "Controller.h"
#include "Item.h"
#include "QuestTaskFindItem.h"
#include "QuestBase.h"
#include "Observer.h"
#include "IntrusivePtr.h"

using namespace mg;

cocos2d::Point cocos2d::Point::ZERO;

int main()
{
	Controller controller;
	Model model;
	controller.model = &model;

	QuestTaskFindItem task;
	task.item = "test";
	task._goal = 1;

	QuestBase quest;
	quest.tasks.emplace_back( &task );
	model.quests.emplace_back( &quest );
	
	Item item0;
	item0.type = "notest";
	Item item1;
	item1.type = "test";

	controller.loot( &item0 );
	controller.loot( &item1 );


	std::vector< IntrusivePtr<TestCase> > tests;
	tests.push_back( make_intrusive<TestSerializationCommandSequence>() );
	tests.push_back( make_intrusive<TestSerialization>() );
	bool result = true;
	for( auto test : tests )
	{
		result = test->execute() && result;
	}
	return result ? 0 : -1;
}