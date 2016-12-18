import fileutils
from Parser import Parser
from WriterCpp import WriterCpp
from WriterJava import WriterJava


def removeOldFiles(parser):
	files = fileutils.getFilesList( "out/" )
	for file in files:
		name = file[0:file.find(".")]
		if parser._findClass(name) == None:
			print "remove", "out/" + file
			fileutils.remove("out/" + file)
	return
	

str = open("declaration.txt","r").read()

parser = Parser()
parser.parse(str)
writer = WriterCpp("out", parser, False)
removeOldFiles(parser)

#parser = Parser()
#parser.parse(str)
#writer = WriterJava("out", parser)
