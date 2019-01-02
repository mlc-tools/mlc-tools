import os
import sys


def main():
    print sys.argv
    job_number = sys.argv[2] if len(sys.argv) > 2 else '1'
    if not job_number.endswith('1'):
        print 'skip'
        exit(0)

    version = open('../../mlc_tools/version.py').read().strip()
    versions = version[version.find("'") + 1: version.rfind("'")].split('.')
    versions[2] = sys.argv[1] if len(sys.argv) > 1 else '1'
    open('../../mlc_tools/version.py', 'w').write("__version__ = '{}'".format('.'.join(versions)))

    version = open('../../mlc_tools/version.py').read().strip()
    version = version[version.find("'") + 1:]
    version = version[:version.find("'")]

    print 'current version is', version

    if 0 != os.system('python setup.py sdist'):
        print 'Error: sdist'
        exit(-1)
    if 0 != os.system('twine upload dist/mlc-tools-{}.tar.gz -u $PYPI_USERNAME -p $PYPI_PASSWORD '.format(version)):
        print 'Error: twine upload'
        exit(-1)
    print 'Done'


if __name__ == '__main__':
    main()
