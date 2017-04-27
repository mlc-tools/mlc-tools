import sys

def get_arg(name, default=''):
	index = 0
	for arg in sys.argv:
		if arg == name and index +1 < len(sys.argv):
			return sys.argv[index+1]
		index += 1
	return default


def get_bool(name, default = False):
	arg = get_arg(name, str(default)).lower()
	return (arg[0] == 't' or arg[0] == 'y') if arg else False


def get_directory(name, default=''):
	arg = get_arg(name, default)
	if arg and arg[-1] != '/':
		arg += '/'
	return arg

