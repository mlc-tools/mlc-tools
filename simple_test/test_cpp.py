import os

if os.system('cd simple_test/build; cmake .. -DBUILD_XML=ON -DBUILD_JSON=OFF -DBUILD_SIDE=CLIENT; make -j8;') != 0:
    exit(1)
if os.system('./simple_test/build/test_mlc_xml ./simple_test/') != 0:
    exit(1)
