import os
import sys


def main(argv):
    path = os.path.dirname(os.path.abspath(__file__))
    print path
    os.system('php {}/{} {}'.format(path, 'test_php.php', ' '.join(argv[1:])))

if __name__ == '__main__':
    main(sys.argv)
