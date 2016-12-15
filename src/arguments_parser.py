import sys

def get_arg(name, default):
	index = 0
	for arg in sys.argv:
		if arg == name and index +1 < len(sys.argv):
			return sys.argv[index+1]
		index += 1
	return default
