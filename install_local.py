import os
import sys

def main():
    version = open('mlc_tools/version.py').read().strip()
    versions = version[version.find("'") + 1: version.rfind("'")].split('.')
    versions[2] = str(int(versions[2]) + 1)
    open('mlc_tools/version.py', 'w').write("__version__ = '{}'".format('.'.join(versions)))

    version = open('mlc_tools/version.py').read().strip()
    version = version[version.find("'") + 1:]
    version = version[:version.find("'")]

    if 0 != os.system('python setup.py install --user'):
        print 'Error: install'
        sys.exit(-1)


if __name__ == '__main__':
    main()
