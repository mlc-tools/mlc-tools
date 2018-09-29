from generated_py.Test import Test
import sys


def main(argv):
    test = Test()
    test.tests()
    test.tests_const()


if __name__ == '__main__':
    main(sys.argv)
