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
    test.execute();
    return 0;
}