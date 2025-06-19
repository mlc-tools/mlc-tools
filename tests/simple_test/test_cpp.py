import os
import sys
import os.path as fs


def main(argv):

    root = fs.abspath(fs.dirname(__file__)) + '/../'
    protocol = argv[1] if len(argv) > 1 else 'xml'
    if protocol == 'xml':
        if not os.path.isdir('{}simple_test/build_xml'.format(root)):
            os.makedirs('{}simple_test/build_xml'.format(root))
        if os.system('cd {}simple_test/build_xml; cmake .. -DBUILD_XML=ON -DBUILD_JSON=OFF -DBUILD_BINARY=OFF -DBUILD_SIDE=SERVER; make -j8;'.format(root)) != 0:
            sys.exit(1)
    elif protocol == 'json':
        if not os.path.isdir('{}simple_test/build_json'.format(root)):
            os.makedirs('{}simple_test/build_json'.format(root))
        if os.system('cd {}simple_test/build_json; cmake .. -DBUILD_XML=OFF -DBUILD_JSON=ON -DBUILD_BINARY=OFF -DBUILD_SIDE=SERVER; make -j8;'.format(root)) != 0:
            sys.exit(1)
    elif protocol == 'binary':
        if not os.path.isdir('{}simple_test/build_binary'.format(root)):
            os.makedirs('{}simple_test/build_binary'.format(root))
        if os.system('cd {}simple_test/build_binary; cmake .. -DBUILD_XML=OFF -DBUILD_JSON=OFF -DBUILD_BINARY=ON -DBUILD_SIDE=SERVER; make -j8;'.format(root)) != 0:
            sys.exit(1)

    if os.system('{0}simple_test/build_{1}/test_mlc_{1} {0}simple_test/'.format(root, protocol)) != 0:
        sys.exit(1)

if __name__ == '__main__':
    main(sys.argv)
