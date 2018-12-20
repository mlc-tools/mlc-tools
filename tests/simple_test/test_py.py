from generated_py.AllTests import AllTests
from generated_py.DataStorage import DataStorage
from generated_py.Logger import Logger
from generated_py.RunAllTests import RunAllTests
import os.path as fs
import sys


class LoggerImpl(Logger):

    def print_log(self, result, message):
        print('{}: {}'.format(message, result))


def initialize_data_storage(protocol):
    filepath = fs.abspath(fs.dirname(__file__)) + '/assets/data.' + protocol
    content = open(filepath).read()
    if protocol == 'json':
        DataStorage.shared().initialize_json(content)
    elif protocol == 'xml':
        DataStorage.shared().initialize_xml(content)


def main(argv):
    initialize_data_storage(argv[1] if len(argv) > 1 else 'xml')

    logger = LoggerImpl()
    result = AllTests.run(logger)

    tests = RunAllTests()
    tests.initialize(logger)
    result = tests.execute() and result

    exit(0 if result else -1)


if __name__ == '__main__':
    main(sys.argv)
