import os.path as fs
import sys

try:
    from generated_py.AllTests import AllTests
    from generated_py.DataStorage import DataStorage
    from generated_py.RunAllTests import RunAllTests
    from generated_py.Logger import Logger
except ImportError:
    from generated_py.mg import *


class LoggerImpl(Logger):

    def message(self, message):
        print(message)


def initialize_data_storage(protocol):
    filepath = fs.abspath(fs.dirname(__file__)) + '/assets/data.' + protocol
    with open(filepath) as f:
        content = f.read()
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
    result = result and tests.execute()

    exit(0 if result else -1)


if __name__ == '__main__':
    main(sys.argv)
