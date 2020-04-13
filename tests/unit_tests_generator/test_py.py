import sys
from generated_py.Logger import Logger
from generated_py.RunAllTests import RunAllTests


class LoggerImpl(Logger):

    def message(self, message):
        print(message)


def main(argv):
    logger = LoggerImpl()
    tests = RunAllTests()
    tests.initialize(logger)
    result = tests.execute()
    sys.exit(0 if result else -1)


if __name__ == '__main__':
    main(sys.argv)
