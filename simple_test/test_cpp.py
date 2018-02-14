import os
import os.path as fs

root = fs.abspath(fs.dirname(__file__)) + '/../'
if os.system('cd {}simple_test/build; cmake .. -DBUILD_XML=ON -DBUILD_JSON=OFF -DBUILD_SIDE=CLIENT; make -j8;'.format(root)) != 0:
    exit(1)
if os.system('{0}simple_test/build/test_mlc_xml {0}simple_test/'.format(root)) != 0:
    exit(1)
