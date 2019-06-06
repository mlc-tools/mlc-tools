import os
import sys


def main(argv):
    path = os.path.dirname(os.path.abspath(__file__))
    if 0 != os.system('node {}/{}'.format(path, 'test_js.js')):
        exit(1)


if __name__ == '__main__':
    main(sys.argv)
