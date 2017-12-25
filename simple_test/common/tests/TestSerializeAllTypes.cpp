#include "TestSerializeAllTypes.h"
#include "AllTypes.h"
#include <stdlib.h>
#include <iostream>
#include "ml/Generics.h"
#include <cmath>

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

	int count = rand() % 100;
	for(int i=0; i<count;++i) 
		objA.int_list.push_back(rand());
	for(int i=0; i<count;++i)
		objA.float_list.push_back(rand() / 10000.f);
	for(int i=0; i<count;++i)
		objA.bool_list.push_back(rand() % 2 == 1);
	for(int i=0; i<count;++i)
		objA.string_list.push_back(rand_str());

	for (int i = 0; i < count; ++i)
		objA.int_string_map[i] = rand_str();
	for (int i = 0; i < count; ++i)
		objA.float_string_map[static_cast<float>(i)] = rand_str();
	for (int i = 0; i < 2; ++i)
		objA.bool_string_map[static_cast<bool>(i)] = rand_str();
	for (int i = 0; i < count; ++i)
		objA.string_string_map[toStr(i)] = rand_str();
	for (int i = 0; i < count; ++i)
		objA.string_int_map[toStr(i)] = i;
	for (int i = 0; i < count; ++i)
		objA.string_float_map[toStr(i)] = static_cast<float>(i);
	for (int i = 0; i < 2; ++i)
		objA.string_bool_map[toStr(i)] = static_cast<bool>(i);

	objA.object.value = rand();
	
	objA.object_ptr = make_intrusive<mg::AllTypesChildren>();
	objA.object_ptr->value = rand();
	
	for (int i = 0; i < count; ++i)
	{
		mg::AllTypesChildren object;
		object.value = rand();
		objA.object_list.push_back(object);
	}
	for (int i = 0; i < count; ++i)
	{
		auto object_ptr = make_intrusive<mg::AllTypesChildren>();
		object_ptr->value = rand();
		objA.object_ptr_list.push_back(object_ptr);
	}
	for (int i = 0; i < count; ++i)
	{
		mg::AllTypesChildren object;
		object.value = rand();
		objA.object_map[toStr(i)] = object;
	}
	for (int i = 0; i < count; ++i)
	{
		auto object_ptr = make_intrusive<mg::AllTypesChildren>();
		object_ptr->value = rand();
		objA.object_ptr_map[toStr(i)] = object_ptr;
	}

    auto str = getSerializedString(&objA);
    std::cout << str << std::endl;
	deserialize(&objB, str);

	auto result = true;
	result = result && objA.int_value0 == objB.int_value0;
	result = result && objA.int_value1 == objB.int_value1;
	result = result && std::fabs(objA.float_value0 - objB.float_value0) < 0.0001f;
	result = result && std::fabs(objA.float_value1 - objB.float_value1) < 0.0001f;
	result = result && objA.bool_value0 == objB.bool_value0;
	result = result && objA.bool_value1 == objB.bool_value1;
	result = result && objA.str_value0 == objB.str_value0;
	result = result && objA.str_value1 == objB.str_value1;

	result = result && objA.int_list == objB.int_list;
	result = result && objA.float_list == objB.float_list;
	result = result && objA.bool_list == objB.bool_list;
	result = result && objA.string_list == objB.string_list;

	result = result && objA.int_string_map == objB.int_string_map;
	result = result && objA.float_string_map == objB.float_string_map;
	result = result && objA.bool_string_map == objB.bool_string_map;
	result = result && objA.string_string_map == objB.string_string_map;
	result = result && objA.string_int_map == objB.string_int_map;
	result = result && objA.string_float_map == objB.string_float_map;
	result = result && objA.string_bool_map == objB.string_bool_map;
	result = result && objA.object == objB.object;
	result = result && *objA.object_ptr == *objB.object_ptr;
	result = result && objA.object_list == objB.object_list;
	result = result && objA.object_map == objB.object_map;

	result = result && objA.object_ptr_list.size() == objB.object_ptr_list.size();
	for(size_t i=0; i<objA.object_ptr_list.size(); ++i)
		result = result && *objA.object_ptr_list[i] == *objB.object_ptr_list[i];
	for (auto& pair : objA.object_ptr_map)
	{
		auto ptrA = pair.second;
		auto ptrB = objB.object_ptr_map.at(pair.first);
		result = *ptrA == *ptrB && result;
	}

	return result;	
}
