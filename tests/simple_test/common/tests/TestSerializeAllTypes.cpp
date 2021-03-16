#include "TestSerializeAllTypes.h"
#include "AllTypes.h"
#include <stdlib.h>
#include <iostream>
#include <cmath>
#include "mg_extensions.h"
#include "mg_Factory.h"
#include "tests/Logger.h"

std::string rand_str()
{
    return "1231asfsdgsrhy4t5243dasfkhgpuhq34gphw9FH072HG}";
}

bool test_all_types(mg::Logger* logger)
{
	mg::AllTypes objA;

    objA.int_value0 = 1234;
    objA.int_value1= 6346363;
    objA.float_value0 = 100.f;
    objA.float_value1 = 1000.f;
    objA.bool_value0 = true;
    objA.bool_value1 = false;
    objA.str_value0 = rand_str();
    objA.str_value1 = rand_str();

    int count = 10;
    for(int i=0; i<count;++i)
        objA.int_list.push_back(i * 13);
    for(int i=0; i<count;++i)
        objA.float_list.push_back(i * 7.5f);
    for(int i=0; i<count;++i)
        objA.bool_list.push_back(i % 2 == 1);
    for(int i=0; i<count;++i)
        objA.string_list.push_back(rand_str());

    for (int i = 0; i < count; ++i)
        objA.int_string_map[i] = rand_str();
    for (int i = 0; i < count; ++i)
        objA.float_string_map[static_cast<float>(i)] = rand_str();
    for (int i = 0; i < 2; ++i)
        objA.bool_string_map[static_cast<bool>(i)] = rand_str();
    for (int i = 0; i < count; ++i)
        objA.string_string_map[mg::toStr(i)] = rand_str();
    for (int i = 0; i < count; ++i)
        objA.string_int_map[mg::toStr(i)] = i;
    for (int i = 0; i < count; ++i)
        objA.string_float_map[mg::toStr(i)] = static_cast<float>(i);
    for (int i = 0; i < 2; ++i)
        objA.string_bool_map[mg::toStr(i)] = static_cast<bool>(i);

    objA.object.value = 487998;

    objA.object_ptr = mg::make_intrusive<mg::AllTypesChildren>();
    objA.object_ptr->value = 243525235;

    for (int i = 0; i < count; ++i)
    {
        mg::AllTypesChildren object;
        object.value = 132123123;
        objA.object_list.push_back(object);
    }
    for (int i = 0; i < count; ++i)
    {
        auto object_ptr = mg::make_intrusive<mg::AllTypesChildren>();
        object_ptr->value = 234234;
        objA.object_ptr_list.push_back(object_ptr);
    }
    for (int i = 0; i < count; ++i)
    {
        mg::AllTypesChildren object;
        object.value = 547987;
        objA.object_map[mg::toStr(i)] = object;
    }
	for (int i = 0; i < count; ++i)
	{
		auto object_ptr = mg::make_intrusive<mg::AllTypesChildren>();
		object_ptr->value = 6879;
		objA.object_ptr_map[mg::toStr(i)] = object_ptr;
	}

#if SERIALIZE_FORMAT == JSON
    auto str = mg::serialize_command_to_json<mg::AllTypes>(&objA);
	auto objB = mg::create_command_from_json<mg::AllTypes>(str);
#endif
#if SERIALIZE_FORMAT == XML
    auto str = mg::serialize_command_to_xml<mg::AllTypes>(&objA);
	auto objB = mg::create_command_from_xml<mg::AllTypes>(str);
#endif

	auto result = true;
	result = result && objA.int_value0 == objB->int_value0;
    result = result && objA.int_value1 == objB->int_value1;
    result = result && std::fabs(objA.float_value0 - objB->float_value0) < 0.0001f;
    result = result && std::fabs(objA.float_value1 - objB->float_value1) < 0.0001f;
    result = result && objA.bool_value0 == objB->bool_value0;
    result = result && objA.bool_value1 == objB->bool_value1;
    result = result && objA.str_value0 == objB->str_value0;
    result = result && objA.str_value1 == objB->str_value1;
    result = result && objA.int_list == objB->int_list;
    result = result && objA.float_list == objB->float_list;
    result = result && objA.bool_list == objB->bool_list;
    result = result && objA.string_list == objB->string_list;
    result = result && objA.int_string_map == objB->int_string_map;
    result = result && objA.float_string_map == objB->float_string_map;
    result = result && objA.bool_string_map == objB->bool_string_map;
    result = result && objA.string_string_map == objB->string_string_map;
    result = result && objA.string_int_map == objB->string_int_map;
    result = result && objA.string_float_map == objB->string_float_map;
    result = result && objA.string_bool_map == objB->string_bool_map;
    result = result && objA.object == objB->object;
    result = result && *objA.object_ptr == *objB->object_ptr;
    result = result && objA.object_list == objB->object_list;
    result = result && objA.object_map == objB->object_map;
    result = result && objA.object_ptr_list.size() == objB->object_ptr_list.size();

	for(size_t i=0; i<objA.object_ptr_list.size(); ++i)
		result = result && *objA.object_ptr_list[i] == *objB->object_ptr_list[i];
	for (auto& pair : objA.object_ptr_map)
	{
		auto ptrA = pair.second;
		auto ptrB = objB->object_ptr_map.at(pair.first);
        result = result && *ptrA == *ptrB;
	}

	return result;
}
