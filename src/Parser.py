from Object import Object
from Class import Class
from Function import Function
from  WriterCpp import WriterCpp

class Parser:
	def __init__(self):
		self.classes=[]
		self.objects=[]
		self.functions=[]
		return
	
	def parse(self, text):
		while len(text) > 0:
			text = text.strip()
			if self._is_class(text):
				text = self._createClass(text)
			elif self._is_functon(text):
				text = self._createFunction(text)
			else:
				text = self._createDeclaration(text)
	
	def _is_class(self,line):
		return line.strip().find("class") == 0
	def _is_functon(self,line):
		return line.strip().find("function") == 0
	
	def _findBody(self, text):
		text = text.strip()
		body = ""
		header = text[0:text.find("\n")]
		text = text[text.find("{"):]
		counter = 0
		index = 0
		for ch in text:
			index += 1
			if counter == 0 and ch == '{':
				counter += 1
				continue
			if ch == '{':
				counter += 1
			if ch == '}':
				counter -= 1
			if counter == 0:
				text = text[index:]
				break
			body += ch
		return body, header, text
	def _createClass(self, text):
		body, header, text = self._findBody(text)
		cls = Class()
		cls.parse(header)
		cls.parseBody( Parser(), body )
		self.classes.append(cls)
		return text

	def _createDeclaration(self, text):
		lines = text.split("\n")
		line = lines[0]
		if len(lines) > 1:
			text = text[text.find("\n")+1:]
		else:
			text = ""
		obj = Object()
		obj.parse(line)
		self.objects.append(obj)
		return text

	def _createFunction(self, text):
		body, header, text = self._findBody(text)
		function = Function()
		function.parse(header)
		function.parseBody(body)
		self.functions.append(function)
		return text



		


str = open("declaration.txt","r").read()

parser = Parser()
parser.parse(str)

writer = WriterCpp(parser)
print writer.out
