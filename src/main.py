from Parser import Parser
from WriterCpp import WriterCpp
from WriterJava import WriterJava

str = open("declaration.txt","r").read()

parser = Parser()
parser.parse(str)
writer = WriterCpp("out", parser)

parser = Parser()
parser.parse(str)
writer = WriterJava("out", parser)
