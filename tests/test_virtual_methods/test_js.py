import os
import sys


def main(argv):
    path = os.path.dirname(os.path.abspath(__file__))
    os.system('node {}/{} {}'.format(path, 'test_js.js', ' '.join(argv[1:])))


if __name__ == '__main__':
    main(sys.argv)
