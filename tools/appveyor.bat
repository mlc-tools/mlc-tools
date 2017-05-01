python ../src/main.py -i ../simple_test/config -o ../simple_test/generated/xml -f xml -l cpp -side server
cd ../simple_test
mkdir build
cd build 
cmake .. -DBUILD_XML=ON -DBUILD_SIDE=SERVER
MSBuild test_mlc_xml.sln /p:Configuration=Release /p:Platform=win32
"Release/test_mlc_xml.exe"
cd ../../tools

python ../src/main.py -i ../simple_test/config -o ../simple_test/generated/xml -f json -l cpp -side client
cd ../simple_test
mkdir build
cd build 
cmake .. -DBUILD_XML=ON -DBUILD_SIDE=CLIENT
MSBuild test_mlc_xml.sln /p:Configuration=Release /p:Platform=win32
"Release/test_mlc_json.exe"

