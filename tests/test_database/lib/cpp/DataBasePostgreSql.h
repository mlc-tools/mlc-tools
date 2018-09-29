#ifndef DATABASE_POSTGRESQL_H
#define DATABASE_POSTGRESQL_H

#include "DataBase.h"
#include "pqxx/connection"

class DataBasePostgreSql : public mg::DataBase
{
public:
    DataBasePostgreSql();
    virtual void connect(const std::string& host,
                         const std::string& database,
                         const std::string& user,
                         const std::string& password) override;
    virtual std::vector<std::vector<std::string>> query_all(const std::string& query) override;
    virtual std::vector<std::string> query_one(const std::string& query) override;
private:
    std::shared_ptr<pqxx::connection> _connection;
};

#endif
