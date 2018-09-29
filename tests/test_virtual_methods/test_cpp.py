import os
import sys
import os.path as fs


def main(argv):

    root = fs.abspath(fs.dirname(__file__)) + '/'
    protocol = argv[1] if len(argv) > 1 else 'xml'
    if protocol == 'xml':
        if not os.path.isdir('{}build_xml'.format(root)):
            os.mkdir('{}build_xml'.format(root))
        if os.system('cd {}build_xml; cmake .. -DBUILD_XML=ON -DBUILD_JSON=OFF; make -j8;'.format(root)) != 0:
            exit(1)
    else:
        if not os.path.isdir('{}build_json'.format(root)):
            os.mkdir('{}build_json'.format(root))
        if os.system('cd {}build_json; cmake .. -DBUILD_XML=OFF -DBUILD_JSON=ON; make -j8;'.format(root)) != 0:
            exit(1)

    if os.system('{0}build_{1}/test_mlc_{1}'.format(root, protocol)) != 0:
        exit(1)

if __name__ == '__main__':
    main(sys.argv)
