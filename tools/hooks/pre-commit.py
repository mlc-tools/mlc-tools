import os
import re


root = os.path.abspath(os.path.dirname(__file__) + '/../..')


def run_mlc_build():
    if 0 != os.system('python  {}/tests/mlc_build.py'.format(root)):
        exit(1)
    if 0 != os.system('python3 {}/tests/mlc_build.py'.format(root)):
        exit(1)


def run_unit_tests():
    if 0 != os.system('python -m unittest discover -s {0}/unit_tests'.format(root)):
        exit(1)
    if 0 != os.system('python3 -m unittest discover -s {0}/unit_tests'.format(root)):
        exit(1)


def run_pylint():
    out = os.popen('pylint {0}/mlc_tools/*/*.py --rcfile {0}/mlc_tools/.pylintrc'.format(root)).read()
    print out
    pat = re.compile(r'Your code has been rated at ([\.\d\-\+]+)/10 \(previous run: ([\.\d\-\+]+)/10, ([\.\d\-\+]+)')
    groups = pat.findall(out)
    if not groups:
        return
    current, previuos, delta = groups[0]
    if float(current) < 9.9:
        print 'Low rated'
        exit(1)
    if float(delta) < -0.1:
        print 'Low delta'
        exit(1)
    if 'unused-import' in out:
        print 'Please remove a unused-import warning. see pylint'
        exit(1)


if __name__ == '__main__':
    run_unit_tests()
    run_pylint()
    run_mlc_build()
