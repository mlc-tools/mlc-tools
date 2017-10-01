#include "enum.h"
#include "TestEnum.h"
#include <iostream>

bool test_switch()
{
	bool result = true;

	mg::TestEnum value = mg::TestEnum::value1;
	switch (value)
	{
	case mg::TestEnum::value1:
		result = result && true;
		break;
	case mg::TestEnum::value2:
		result = false;
		break;
	default:
		result = false;
	}

	value = mg::TestEnum::value2;
	switch (value)
	{
	case mg::TestEnum::value1:
		result = false;
		break;
	case mg::TestEnum::value2:
		result = result && true;
		break;
	default:
		result = false;
	}

	return result;
}


bool test_compare()
{
	mg::TestEnum foo;

	bool result = foo.value1 != foo.value2;
	result = result && foo.value1 == foo.value1;
	result = result && foo.value2 == foo.value2;

	if (!result)
		std::cout << "Test compare enum fields failed." << std::endl;
	else
		std::cout << "Test compare enum fields success." << std::endl;
	return result;
}

bool test_enum()
{
	bool result = true;
	result = test_switch() && result;
	result = test_compare() && result;
	return result;
}