import os
from os.path import isdir
import sys


ROOT = ''


def _generate():
	result = os.system('python {0}src/main.py -i {0}simple_test/config -o {0}simple_test/out -f xml -l cpp -t no'.format(ROOT))
	if result != 0:
		print 'Test: Generation fail'
		exit(-1)
	print 'Test: Generation Ok'


def _make():
	command = 'cd {}simple_test; mkdir build; cd build; cmake ..; make'.format(ROOT)
	if isdir('{}simple_test/build'.format(ROOT)):
		command = 'cd {}simple_test/build; cmake ..; make'.format(ROOT)
	result = os.system(command)
	if result != 0:
		print 'Test: Make fail'
		exit(-1)
	print 'Test: Make Ok'


def _execute():
	result = os.system('cd {}simple_test/build; ./test_mlc'.format(ROOT))
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
