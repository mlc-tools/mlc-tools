import os
from os.path import isdir
import sys


ROOT = ''


def _generate():
    result = os.system('python {0}src/main.py -i {0}simple_test/config -o {0}simple_test/generated/xml -f xml -l cpp -side client'.format(ROOT))
    result = os.system('python {0}src/main.py -i {0}simple_test/config -o {0}simple_test/generated/json -f json -l cpp -side server'.format(ROOT)) and result
    if result != 0:
        print 'Test: Generation fail'
        exit(-1)
    print 'Test: Generation Ok'


def _make():
    if not isdir('{}simple_test/build'.format(ROOT)):
        os.system('cd {}simple_test; mkdir build'.format(ROOT))

    result = os.system('cd {}simple_test/build; cmake .. -DBUILD_XML=ON -DBUILD_JSON=OFF -DBUILD_SIDE=CLIENT; make -j 8'.format(ROOT))
    result = os.system('cd {}simple_test/build; cmake .. -DBUILD_XML=OFF -DBUILD_JSON=ON -DBUILD_SIDE=SERVER; make -j 8'.format(ROOT)) and result
    if result != 0:
        print 'Test: Make fail'
        exit(-1)
    print 'Test: Make Ok'


def _execute():
    result = os.system('cd {}simple_test/build; ./test_mlc_xml'.format(ROOT))
    result = os.system('cd {}simple_test/build; ./test_mlc_json'.format(ROOT))
    if result != 0:
        print 'Test: Execute fail'
        exit(-1)
    print 'Test: Execute Ok'


if __name__ == '__main__':
    if len(sys.argv) > 1:
        ROOT = sys.argv[1]

    print '--------------------------------------------------'
    _generate()
    _make()
    _execute()
    print '--------------------------------------------------'
    print 'All Tests: Ok'
