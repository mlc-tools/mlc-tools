#include "RunAllTests.h"
#include "Logger.h"
#include <iostream>
#include <sstream>

class Logger : public mg::Logger
{
public:
    virtual void print_log(bool result, const std::string& message) override
    {
        std::cout << message << " " << (result? "Ok" : "Fail") << std::endl;
    }
};

int main()
{
    Logger logger;
    mg::RunAllTests test;
    test.initialize(&logger);
    auto result = test.execute();

    std::cout << "====================================" << std::endl;
    std::cout << "Sumary: " << std::endl;
    std::cout << "  Steps: " << logger.success_count << "/" << logger.tests_count << " success" << std::endl;
    std::cout << "  Count of classes: " << logger.class_count << std::endl;
    std::cout << "  Count of method: " << logger.methods_count << std::endl;
    std::cout << "  Count of all methods: " << logger.all_methods_count << std::endl;
    std::cout << "  Count of tested methods: " << logger.implemented_methods_count << std::endl;
    std::cout << "  Percent of cover: " << 100.f * logger.implemented_methods_count / logger.all_methods_count << "%" << std::endl;
    std::cout << "====================================" << std::endl;

    return result ? 0 : 1;
}
