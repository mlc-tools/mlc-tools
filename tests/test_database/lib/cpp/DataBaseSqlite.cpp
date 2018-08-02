#include "DataBaseSqlite.h"
#include <iostream>

std::vector<std::vector<std::string>> DataBaseSqlite::query_result;

DataBaseSqlite::DataBaseSqlite()
: _connection(nullptr)
{
}

DataBaseSqlite::~DataBaseSqlite()
{
    if(_connection)
    {
        sqlite3_close(_connection);
    }
}

void DataBaseSqlite::connect(const std::string& host,
                             const std::string& database,
                             const std::string& user,
                             const std::string& password)
{
    int rc;
    rc = sqlite3_open((database + ".db").c_str(), &_connection);
    if(rc)
    {
        std::cout << "Can't open database: " << database << " Error: " << sqlite3_errmsg(_connection);
        sqlite3_close(_connection);
        _connection = nullptr;
        return;
    }
}

std::vector<std::vector<std::string>> DataBaseSqlite::query_all(const std::string& query)
{
    std::unique_lock<std::mutex> lock(_query);
    query_result.clear();
    
    char *error = 0;
    int rc = sqlite3_exec(_connection, query.c_str(), callback, 0, &error);
    if(rc!=SQLITE_OK)
    {
        std::cout << "SQL error: " << error << std::endl;
        sqlite3_free(error);
    }

    return std::move(query_result);
}

std::vector<std::string> DataBaseSqlite::query_one(const std::string& query)
{
    std::unique_lock<std::mutex> lock(_query);
    query_result.clear();
    
    char *error = 0;
    int rc = sqlite3_exec(_connection, query.c_str(), callback, 0, &error);
    if(rc!=SQLITE_OK)
    {
        std::cout << "SQL error: " << error << std::endl;
        sqlite3_free(error);
    }

    return !query_result.empty() ? query_result[0] : std::vector<std::string>();
}

int DataBaseSqlite::callback(void *NotUsed, int argc, char **argv, char **azColName)
{
    std::vector<std::string> row(argc);
    for(int i=0; i<argc; ++i)
    {
        row[i] = argv[i] ? argv[i] : "NULL";
    }
    query_result.push_back(row);
    return 0;
}

