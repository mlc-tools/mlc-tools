import os

if __name__ == '__main__':
	os.system('python ../src/main.py -i ../simple_test/config -o ../simple_test/out -f xml -l cpp -t no')
	os.system('cd ../simple_test; mkdir build; cd build; cmake ..; make')