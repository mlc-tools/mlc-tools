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

    print('Sumary: {}/{} success'.format(logger.success_count, logger.tests_count))
    print('  Count of classes: {}'.format(logger.class_count))
    print('  Count of method: {}'.format(logger.methods_count))
    print('  Count of all methods: {}'.format(logger.all_methods_count))
    print('  Count of tested methods: {}'.format(logger.implemented_methods_count))
    print('  Percent of cover: ' + str(100.0 * logger.implemented_methods_count / logger.all_methods_count))

    exit(0 if result else -1)


if __name__ == '__main__':
    main(sys.argv)
