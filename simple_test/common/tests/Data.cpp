#include "Data.h"
#include "DataStorage.h"

bool test_units()
{
	bool result = true;

	for (auto& pair : mg::DataStorage::shared().units)
	{
		auto name = pair.first;
		auto& unit = pair.second;
		auto pUnit = mg::DataStorage::shared().get<mg::DataUnit>(name);
		result = result && pUnit == &unit;
		result = result && name == unit.name;
	}
	return result;
}

bool test_links()
{
	bool result = true;

	auto unit1 = mg::DataStorage::shared().get<mg::DataUnit>("unitname1");
	auto unit2 = mg::DataStorage::shared().get<mg::DataUnit>("unitname2");

	result = result && unit1->link_to_data == unit2;
	result = result && unit2->link_to_data == unit1;
	result = result && unit1 != unit2;
	return result;
}

bool test_data()
{
    bool result = true;

	result = test_units() && result;
	result = test_links() && result;

    return result;
}

