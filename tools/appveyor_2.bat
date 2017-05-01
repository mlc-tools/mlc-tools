python src/main.py -i simple_test/config -o simple_test/generated/json -f json -l cpp -side client
cd simple_test
mkdir build
cd build 
cmake .. -DBUILD_XML=OFF -DBUILD_JSON=ON -DBUILD_SIDE=CLIENT
MSBuild test_mlc_json.sln /p:Configuration=Release /p:Platform=win32
"Release/test_mlc_json.exe"
