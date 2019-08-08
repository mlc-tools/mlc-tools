import os
import re
import sys


root = os.path.abspath(os.path.dirname(__file__) + '/../..')


def has_python_version(number):
    result = os.system('python%d --version' % number)
    return result == 0


def run_mlc_build():
    if 0 != os.system('python  {}/tests/mlc_build.py'.format(root)):
        sys.exit(1)

    if has_python_version(3):
        if 0 != os.system('python3 {}/tests/mlc_build.py'.format(root)):
            sys.exit(1)


def run_unit_tests():
    if 0 != os.system('python -m unittest discover -s {0}/unit_tests'.format(root)):
        sys.exit(1)

    if has_python_version(3):
        if 0 != os.system('python3 -m unittest discover -s {0}/unit_tests'.format(root)):
            sys.exit(1)


def run_pylint():
    out = os.popen('pylint {0}/mlc_tools/*/*.py --rcfile {0}/mlc_tools/.pylintrc'.format(root)).read()
    print(out)
    pat = re.compile(r'Your code has been rated at ([\.\d\-\+]+)/10 \(previous run: ([\.\d\-\+]+)/10, ([\.\d\-\+]+)')
    groups = pat.findall(out)
    if not groups:
        return
    current, previuos, delta = groups[0]
    if float(current) < 9.95:
        print('Low rated')
        sys.exit(1)
    if float(delta) < 0.0:
        print('Low delta')
        sys.exit(1)
    if 'unused-import' in out:
        print('Please remove a unused-import warning. see pylint')
        sys.exit(1)
    if 'trailing - whitespace' in out:
        print('Please remove a trailing - whitespace warning. see pylint')
        sys.exit(1)
    if 'no-name-in-module' in out:
        print('Please check a imports. see pylint no-name-in-module warning')
        sys.exit(1)


if __name__ == '__main__':
    run_unit_tests()
    run_pylint()
    run_mlc_build()
