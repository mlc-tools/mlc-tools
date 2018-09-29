import os

if __name__ == '__main__':
    root = os.path.dirname(os.path.abspath(__file__)) + '/../..'

    if 0 != os.system('python  {}/tests/mlc_build.py'.format(root)):
        exit(1)
    if 0 != os.system('python3 {}/tests/mlc_build.py'.format(root)):
        exit(1)
    exit(0)
