#include "DataBasePostgreSql.h"
#include "pqxx/connection"
#include "pqxx/transaction"
#include <iostream>

DataBasePostgreSql::DataBasePostgreSql()
{
}

void DataBasePostgreSql::connect(const std::string& host,
                                 const std::string& database,
                                 const std::string& user,
                                 const std::string& password)
{
    std::ostringstream conn_string("");
    conn_string << "host=" << host << " user=" << user << " password=" << password << " dbname=" << database;
    auto string = conn_string.str();
    try
    {
        _connection = std::make_shared<pqxx::connection>(string);
    } catch (pqxx::broken_connection e) {
        std::cout << "Failed to establish connection." << std::endl;
    }
    return;
}

std::vector<std::vector<std::string>> DataBasePostgreSql::query_all(const std::string& query)
{
    std::vector<std::vector<std::string>> result;
    try {
        pqxx::work work(*_connection, "query");
        auto res = work.exec(query);
        work.commit();

        for (auto i = res.begin(), r_end = res.end(); i != r_end; ++i)
        {
            std::vector<std::string> row(i->size());
            size_t index = 0;
            for (auto f = i->begin(); f != i->end(); ++f)
            {
                row[index++] = f->as<std::string>();
            }
            result.push_back(row);
        }

    } catch (pqxx::sql_error e) {
        std::cout << ("DB exception:");
        std::cout << ("%s", e.what());
        std::cout << ("BD exception end.");
        std::cout << ("DB exception query:");
        std::cout << ("%s", query.c_str());
        std::cout << ("BD exception query end.");
    }
    return result;
}

std::vector<std::string> DataBasePostgreSql::query_one(const std::string& query)
{
    std::vector<std::string> result;
    try {
        pqxx::work work(*_connection, "query");
        auto res = work.exec(query);
        work.commit();

        for (auto i = res.begin(), r_end = res.end(); i != r_end; ++i)
        {
            result.resize(i->size());
            size_t index = 0;
            for (auto f = i->begin(); f != i->end(); ++f)
            {
                result[index++] = f->as<std::string>();
            }
            break;
        }

    } catch (pqxx::sql_error e) {
        std::cout << ("DB exception:");
        std::cout << ("%s", e.what());
        std::cout << ("BD exception end.");
        std::cout << ("DB exception query:");
        std::cout << ("%s", query.c_str());
        std::cout << ("BD exception query end.");
    }
    return result;
}
