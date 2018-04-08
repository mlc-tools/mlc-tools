from generated_py.AllTests import AllTests
from generated_py.DataStorage import DataStorage
import os.path as fs
import sys


class Loger:

    def add_result(self, result, message):
        print '{}: {}'.format(message, result)
        return result


def initialize_data_storage(protocol):
    file = fs.abspath(fs.dirname(__file__)) + '/assets/data.' + protocol
    content = open(file).read()
    DataStorage.shared().initialize(content)


def main(argv):
    initialize_data_storage(argv[1] if len(argv) > 1 else 'xml')

    loger = Loger()
    result = AllTests.run(loger)
    exit(0 if result else -1)


if __name__ == '__main__':
    main(sys.argv)
