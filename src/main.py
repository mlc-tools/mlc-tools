import fileutils
from arguments_parser import get_arg
from Parser import Parser
from WriterCpp import WriterCpp
from WriterJava import WriterJava


configs_directory = get_arg( "-i", "config" )
if configs_directory[-1] != "/":
	configs_directory += "/"
	
out_directory = get_arg( "-o", "out" )
if out_directory[-1] != "/":
	out_directory += "/"

tests = get_arg( "-t", "False" )
tests = tests == "True" or tests == "true" or tests == "yes" or tests == "y"

str = ""
files = fileutils.getFilesList( configs_directory )
parser = Parser()
for file in files:
	if file.find( ".mlc" ) == len(file)-4:
		str = open(configs_directory + file,"r").read()
		parser.parse(str)

parser.link()

writer = WriterCpp(out_directory, parser, tests)

files = fileutils.getFilesList( out_directory )
for file in files:
	name = file[0:file.find(".")]
	if parser._findClass(name) == None:
		print "remove", out_directory + file
		fileutils.remove(out_directory + file)

#parser = Parser()
#parser.parse(str)
#writer = WriterJava("out", parser)
#removeOldFiles(parser)