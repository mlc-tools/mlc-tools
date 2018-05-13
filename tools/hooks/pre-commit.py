import os

if __name__ == '__main__':
    root = os.path.dirname(os.path.abspath(__file__)) + '/../..'

    os.system('python  {}/tests/mlc_build.py'.format(root))
    os.system('python3 {}/tests/mlc_build.py'.format(root))
