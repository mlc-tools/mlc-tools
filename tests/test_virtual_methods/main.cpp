#include "RunAllTests.h"
#include "Logger.h"
#include <iostream>
#include <sstream>

class Logger : public mg::Logger
{
public:
    virtual void message(const std::string& message) override
    {
        std::cout << message << std::endl;
    }
};

int main()
{
    Logger logger;
    mg::RunAllTests test;
    test.initialize(&logger);
    auto result = test.execute();

    return result ? 0 : 1;
}
