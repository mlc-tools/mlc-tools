import sys
from generated_py.Logger import Logger
from generated_py.RunAllTests import RunAllTests


class LoggerImpl(Logger):

    def print_log(self, result, message):
        print('{}: {}'.format(message, result))


def main(argv):
    logger = LoggerImpl()
    tests = RunAllTests()
    tests.initialize(logger)
    result = tests.execute()
    exit(0 if result else -1)


if __name__ == '__main__':
    main(sys.argv)
