#include "DataBase.h"
#include "DataBasePostgreSql.h"
#include "DataBaseSqlite.h"
#include "RunAllTests.h"
#include "TestDataBase.h"
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
    mg::TestDataBase::db = mg::make_intrusive<DataBasePostgreSql>();

    Logger logger;
    mg::RunAllTests test;
    test.initialize(&logger);
    test.execute();
    // std::string r0 = test<DataBasePostgreSql>();
    // std::string r1 = test<DataBaseSqlite>();
    // bool result = r0 == r1 ? 0 : 1;
    // std::cout << (result == 0 ? "Success" : "Failed") << std::endl;
    return 0;
}