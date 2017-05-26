#include "TestSerializeAllTypes.h"
#include "AllTypes.h"
#include <stdlib.h>
#include <iostream>

extern std::string getSerializedString(const mg::SerializedObject* object);
extern void deserialize(mg::SerializedObject* object, const std::string& payload);

std::string rand_str()
{
	std::string result;
	int count = rand() % 10;
	for(int i=0; i<count;++i)
		result.push_back(static_cast<char>('a' + rand() % 26));
	return result;
}

bool test_all_types()
{
	mg::AllTypes objA;
	mg::AllTypes objB;

	objA.int_value0 = rand();
	objA.int_value1= rand();
	objA.float_value0 = rand() / 10000.f;
	objA.float_value1 = rand() / 10000.f;
	objA.bool_value0 = rand() % 2 == 1;
	objA.bool_value1 = rand() % 2 == 1;
	objA.str_value0 = rand_str();
	objA.str_value1 = rand_str();

	int count = rand() % 10;
	for(int i=0; i<count;++i) 
		objA.int_list.push_back(rand());
	for(int i=0; i<count;++i)
		objA.float_list.push_back(rand() / 10000.f);
	for(int i=0; i<count;++i)
		objA.bool_list.push_back(rand() % 2 == 1);
	for(int i=0; i<count;++i)
		objA.string_list.push_back(rand_str());

    auto str = getSerializedString(&objA);
    std::cout << str << std::endl;
	deserialize(&objB, str);

	auto result = true;
	result = result && objA.int_value0 == objB.int_value0;
	result = result && objA.int_value1 == objB.int_value1;
	result = result && objA.float_value0 == objB.float_value0;
	result = result && objA.float_value1 == objB.float_value1;
	result = result && objA.bool_value0 == objB.bool_value0;
	result = result && objA.bool_value1 == objB.bool_value1;
	result = result && objA.str_value0 == objB.str_value0;
	result = result && objA.str_value1 == objB.str_value1;

	result = result && objA.int_list == objB.int_list;
	result = result && objA.float_list == objB.float_list;
	result = result && objA.bool_list == objB.bool_list;
	result = result && objA.string_list == objB.string_list;

	return result;	
}
