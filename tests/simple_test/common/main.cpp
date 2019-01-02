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
#include "tests/Side.h"
#include "tests/enum.h"
#include "tests/TestSerializeAllTypes.h"
#include <iostream>
#include "DataStorage.h"
#include <fstream>
#include "config.h"
#include "mg_Factory.h"
#include "AllTests.h"
#include "tests/Logger.h"
#include "tests/RunAllTests.h"

extern mg::intrusive_ptr<mg::CommandBase> createCommand(const std::string& payload);
std::string root = "../../";
void initialize_data_storage()
{
#if SUPPORT_XML_PROTOCOL
	std::fstream stream(root + "assets/data.xml", std::ios::in);
    std::cout << "SERIALIZE_FORMAT == XML\n";
	std::string str((std::istreambuf_iterator<char>(stream)), std::istreambuf_iterator<char>());
	mg::DataStorage::shared().initialize_xml(str);
#elif SUPPORT_JSON_PROTOCOL
	std::fstream stream(root + "assets/data.json", std::ios::in);
    std::cout << "SERIALIZE_FORMAT == JSON\n";
	std::string str((std::istreambuf_iterator<char>(stream)), std::istreambuf_iterator<char>());
	mg::DataStorage::shared().initialize_json(str);
#endif
}


class Logger : public mg::Logger
{
public:
    virtual void print_log(bool result, const std::string& message) override
    {
        std::cout << message << " " << (result? "Ok" : "Fail") << std::endl;
    }
};


int main(int argc, char ** args)
{
    if(argc > 1)
    {
        root = args[1];
    }

	auto result = true;

	initialize_data_storage();

	Logger logger;

	result = logger.push(test_enum(), "test_enum");
    result = logger.push(test_side(), "test_side");
    result = logger.push(test_all_types(&logger), "test_all_types");
	result = mg::AllTests::run(&logger) && result;

    mg::RunAllTests test;
    test.initialize(&logger);
    result = test.execute() && result;

    std::cout << "====================================" << std::endl;
    std::cout << "Sumary: " << std::endl;
    std::cout << "  Steps: " << logger.success_count << "/" << logger.tests_count << " success" << std::endl;
    std::cout << "  Count of classes: " << logger.class_count << std::endl;
    std::cout << "  Count of method: " << logger.methods_count << std::endl;
    std::cout << "  Count of all methods: " << logger.all_methods_count << std::endl;
    std::cout << "  Count of tested methods: " << logger.implemented_methods_count << std::endl;
    std::cout << "  Percent of cover: " << 100.f * logger.implemented_methods_count / logger.all_methods_count << "%" << std::endl;
    std::cout << "====================================" << std::endl;


	std::cout << "Execute results = " << (result ? "Ok" : "Fail") << std::endl;
	return result ? 0 : -1;
}
