import sys
from generated_py.Logger import Logger
from generated_py.RunAllTests import RunAllTests
from generated_py.TestDataBase import TestDataBase
from lib.py.db import DataBaseMysql
from lib.py.db import DataBaseSqlite
from lib.py.db import DataBasePostgreSql


class LoggerImpl(Logger):

    def message(self, message):
        print(message)


def run_test(class_):
    TestDataBase.db = class_()

    logger = LoggerImpl()
    tests = RunAllTests()
    tests.initialize(logger)
    result = tests.execute()
    return result


def main(argv):
    result = True
    result = run_test(DataBaseMysql) and result
    result = run_test(DataBaseSqlite) and result
    result = run_test(DataBasePostgreSql) and result
    exit(0 if result else -1)


if __name__ == '__main__':
    main(sys.argv)
