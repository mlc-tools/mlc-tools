#include "Data.h"
#include "DataStorage.h"
#include <iostream>

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

bool test_enums()
{
	bool result = true;

	auto unit1 = mg::DataStorage::shared().get<mg::DataUnit>("unitname1");
	auto unit2 = mg::DataStorage::shared().get<mg::DataUnit>("unitname2");

	result = result && unit1->unit_type == mg::UnitType::attack;
	result = result && unit1->unit_type != mg::UnitType::defend;
	result = result && unit1->unit_type != mg::UnitType::support;
	
	result = result && unit2->unit_type == mg::UnitType::defend;
	result = result && unit2->unit_type != mg::UnitType::attack;
	result = result && unit2->unit_type != mg::UnitType::support;
	return result;
}

bool test_list_links()
{
	bool result = true;

	auto unit1 = mg::DataStorage::shared().get<mg::DataUnit>("unitname1");
	auto unit2 = mg::DataStorage::shared().get<mg::DataUnit>("unitname2");

	result = result && unit1->all_units.size() == 2;
	result = result && unit2->all_units.size() == 2;
	for (auto unit : unit1->all_units)
	{
		result = result && (unit == unit1 || unit == unit2);
	}
	for (auto unit : unit2->all_units)
	{
		result = result && (unit == unit1 || unit == unit2);
	}

	return result;
}

bool test_map_links()
{
	bool result = true;

	auto unit1 = mg::DataStorage::shared().get<mg::DataUnit>("unitname1");
	auto unit2 = mg::DataStorage::shared().get<mg::DataUnit>("unitname2");

	result = result && unit1->map_units.size() == 2;
	result = result && unit2->map_units.size() == 2;

	for (auto pair : unit1->map_units)
	{
		result = result && (pair.first == unit1->name || pair.first == unit2->name);
		result = result && (pair.second == 1 || pair.second == 2);
	}
	for (auto pair : unit2->map_units)
	{
		result = result && (pair.first == unit1->name || pair.first == unit2->name);
		result = result && (pair.second == 1 || pair.second == 2);
	}

	return result;
}

bool test_data()
{
    bool result = true;

	result = test_units() && result;
	result = test_links() && result;
	result = test_list_links() && result;
	result = test_map_links() && result;
	result = test_enums() && result;

	if(!result)
	    std::cout << "Test data failed." << std::endl;
    else
        std::cout << "Test data success." << std::endl;

    return result;
}

