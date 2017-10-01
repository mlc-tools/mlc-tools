/******************************************************************************/
/*
* Copyright 2014-2017 Vladimir Tolmachev
*
* Author: Vladimir Tolmachev
* Project: ml
* e-mail: tolm_vl@hotmail.com
* If you received the code is not the author, please contact me
*/
/******************************************************************************/
#include "core/CommandBase.h"
#include "TestEnum.h"
#include "IntrusivePtr.h"
#include "tests/Visitor.h"
#include "tests/Side.h"
#include "tests/Data.h"
#include "tests/TestSerializeAllTypes.h"
#include <iostream>
#include "DataStorage.h"
#include <fstream>
#include "config.h"

extern intrusive_ptr<mg::CommandBase> createCommand(const std::string& payload);


bool test_serialization();
bool test_enum();

void initialize_data_storage()
{
#if MG_SERIALIZE_FORMAT == MG_JSON
	std::fstream stream("../../assets/data.json", std::ios::in);
#endif
#if MG_SERIALIZE_FORMAT == MG_XML
	std::fstream stream("../../assets/data.xml", std::ios::in);
#endif

	std::string str((std::istreambuf_iterator<char>(stream)), std::istreambuf_iterator<char>());
	mg::DataStorage::shared().initialize(str);
}

int main()
{
	auto result = true;

	initialize_data_storage();

	result = test_serialization() && result;
	result = test_enum() && result;
	result = test_visitor() && result;
	result = test_side() && result;
	result = test_data() && result;
	result = test_all_types() && result;


	std::cout << "Execute results = " << (result ? "Ok" : "Fail") << std::endl;
	return result ? 0 : -1;
}


bool test_serialization()
{
	int test_user_id = 123;
	int test_time = 1231235245;

	auto command = make_intrusive<mg::CommandBase>();
	command->user_id = test_user_id;
	command->current_time = test_time;
	auto buffer = command->getSerializedString();
	auto deserialized = createCommand(buffer);

	std::cout << "serialized string:" << std::endl;
	std::cout << buffer << std::endl;

	auto result = true;
	result = result && deserialized->user_id == command->user_id;
	result = result && deserialized->current_time == command->current_time;

	if(!result)
	    std::cout << "Test serialization failed." << std::endl;
	else
		std::cout << "Test serialization success." << std::endl;

	return result;
}

bool test_enum()
{
    mg::TestEnum foo;

    bool result = foo.value1 != foo.value2;
    result = result && foo.value1 == foo.value1;
    result = result && foo.value2 == foo.value2;

	if(!result)
	    std::cout << "Test compare enum fields failed." << std::endl;
	else
		std::cout << "Test compare enum fields success." << std::endl;
	return result;
}