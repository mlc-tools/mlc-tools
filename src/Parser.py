from Object import Object
from Class import Class
from Function import Function
from  WriterCpp import WriterCpp
from  WriterJava import WriterJava

def throw_error( msg ):
	print msg
	exit(-1)

class Parser:
	def __init__(self):
		self.classes=[]
		self.objects=[]
		self.functions=[]
		return
	
	def parse(self, text):
		text = text.strip()
		while len(text) > 0:
			text = text.strip()
			if self._is_class(text):
				text = self._createClass(text)
			elif self._is_functon(text):
				text = self._createFunction(text)
			else:
				text = self._createDeclaration(text)

		self._find_dependences()
	
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

	def _findClass(self, name):
		for cls in self.classes:
			if cls.name == name:
				return cls
		return None

	def _find_dependences(self):
		for cls in self.classes:
			behaviors = []
			for name in cls.behaviors:
				c = self._findClass(name)
				if c == None:
					throw_error( "cannot find behavior class: {0}<{1}>".format(cls.name, name) );
				behaviors.append( c )
			cls.behaviors = behaviors
			cls.is_serialized = self.isSerialised(cls)

	def isSerialised(self, cls):
		if cls.is_serialized:
			return True
		for c in cls.behaviors:
			return self.isSerialised(c)
		return False				
