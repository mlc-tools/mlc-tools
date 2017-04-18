Simple using:

cd src
python main.py


configs directory - configs/
out directory - out/
python library src directory - src/


Confugured launch:

python src/main.py -o out -i config -incremental yes -t no -side both -f xml
Parameters:
	-o - path to out directory
	-i - path to configs directory
	-incremental - yes/no - rewrite/no rewrite not modified classes
	-side - both/client/server - used for different code
	-t - yes/no - generate tests (noot worked no :( )
	-f xml/json - serialization type
