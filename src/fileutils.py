import os
import hashlib
from os.path import isfile, join, isdir

def _getFilesList(path, prefix):
	list = os.listdir(path)
	listFiles = []
	for i in list:
		if isdir(path + i):
			result = _getFilesList( path + i + "/", prefix + i + "/" )
			for r in result:
				listFiles.append(r)
		if isfile(path + i):
			listFiles.append( prefix + i )
	return listFiles;

def getFilesList(path):
	return _getFilesList(path, "");

def createDirForFile(file):
	dir = file;
	k = dir.rindex('/')
	dir = dir[:k]
	if not os.path.exists(dir):
		os.makedirs(dir)

def remove(file):
	if os.path.exists(file):
		os.remove(file)

def loadDictFromFile(path):
	dict = {}
	try:
		file = open(path,"r")
		for line in file:
			str = line.strip();
			args = str.split(" ")
			if len(args) == 2:
				key = str.split(" ")[0]
				value = str.split(" ")[1]
				dict[key] = value
		return dict
	except:
		return dict
	return dict

def saveDictToFile(path, dict):
	try:
		_dict = loadDictFromFile(path)
		for key in dict:
			_dict[key] = dict[key]
		file = open(path,"w")
		for key in _dict:
			value = _dict[key]
			str = key + " " + _dict[key] + "\n"
			file.write(str)
	except:
		return False
	return True

def write( path, buffer ):
	rewrite = True
	if os.path.exists(path):
		rewrite = open(path).read() != buffer			
	if rewrite:
		createDirForFile( path )
		open(path,"w").write(buffer)	
			
cacheFile = "bin/cache.tmp"
def isFileChanges(file):
	dict = loadDictFromFile(cacheFile)
	if file in dict:
		cache = dict[file]

		m = hashlib.md5()
		m.update(open(file).read())
		return not cache == str(m.hexdigest())
	return True

def saveMd5ToCache(file):
	createDirForFile(cacheFile)
	m = hashlib.md5()
	m.update(open(file).read())
	saveDictToFile( cacheFile, {file:m.hexdigest()} )
