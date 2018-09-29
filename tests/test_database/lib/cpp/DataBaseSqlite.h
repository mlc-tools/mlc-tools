#ifndef DATABASE_SQLITE_H
#define DATABASE_SQLITE_H

#include "DataBase.h"
#include "sqlite3/sqlite3.h"
#include <mutex>


class DataBaseSqlite : public mg::DataBase
{
public:
    DataBaseSqlite();
    virtual ~DataBaseSqlite();
    virtual void connect(const std::string& host,
                         const std::string& database,
                         const std::string& user,
                         const std::string& password) override;
    virtual std::vector<std::vector<std::string>> query_all(const std::string& query) override;
    virtual std::vector<std::string> query_one(const std::string& query) override;
    
protected:
    static std::vector<std::vector<std::string>> query_result;
    static int callback(void*, int, char**, char**);
private:
    std::mutex _query;
    sqlite3 *_connection;
};

#endif
