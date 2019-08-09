#include "enum.h"
#include "TestEnum.h"
#include "TestEnumValue1.h"
#include "TestEnumValue2.h"
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
	if (!result)
		std::cout << "Test compare enum fields failed." << std::endl;
	return result;
}

int dispatch(const mg::TestEnum& msg)
{

//	switch (msg)
//	{
//	case mg::TestEnum::value1:
//	{
//		auto value = static_cast<const mg::TestEnumValue1*>(&msg);
//		return value->parameter;
//	}
//	case mg::TestEnum::value2:
//	{
//		auto value = static_cast<const mg::TestEnumValue2*>(&msg);
//		return value->parameter;
//	}
//	default:
//		return -1;
//	}
	return 0;
};

bool test_messages_system()
{
//	mg::TestEnumValue1 msg1 = mg::TestEnum::value1;
//	mg::TestEnumValue2 msg2 = mg::TestEnum::value2;
//
//	msg1.parameter = 10;
//	msg2.parameter = 20;

	bool result = true;
//	result = dispatch(msg1) == msg1.parameter && result;
//	result = dispatch(msg2) == msg2.parameter && result;
	return result;
}

bool test_enum()
{
	bool result = true;
	result = test_switch() && result;
	result = test_compare() && result;
	result = test_messages_system() && result;
	return result;
}