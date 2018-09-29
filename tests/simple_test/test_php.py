import os
import sys


def main(argv):
    path = os.path.dirname(os.path.abspath(__file__))
    if 0 != os.system('php {}/{} {}'.format(path, 'test_php.php', ' '.join(argv[1:]))):
        exit(1)

if __name__ == '__main__':
    main(sys.argv)
