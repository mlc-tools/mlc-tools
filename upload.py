import os


def main():
    version = open('mlc_tools/version.py').read().strip()
    versions = version[version.find("'") + 1: version.rfind("'")].split('.')
    versions[2] = str(int(versions[2]) + 1)
    open('mlc_tools/version.py', 'w').write("__version__ = '{}'".format('.'.join(versions)))

    version = open('mlc_tools/version.py').read().strip()
    version = version[version.find("'") + 1:]
    version = version[:version.find("'")]

    if 0 != os.system('python setup.py test'):
        print 'Error: tests'
        exit(-1)
    if 0 != os.system('python setup.py sdist'):
        print 'Error: sdist'
        exit(-1)
    if 0 != os.system('python setup.py install'):
        print 'Error: install'
        exit(-1)
    if 0 != os.system('twine upload dist/mlc-tools-{}.tar.gz'.format(version)):
        print 'Error: twine upload'
        exit(-1)
    if 0 != os.system('pip install mlc_tools --upgrade --no-cache --user'):
        print 'Error: install mlc_tools by pip'
        exit(-1)


if __name__ == '__main__':
    main()
