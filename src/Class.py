from Object import Object
from Function import Function

class Class(Object):
	def __init__(self):
		Object.__init__(self)
		self.behaviors = []
		self.members = []
		self.functions = []

	def parse(self, line):
		str = line.strip()
		k = str.find("class")
		if k > -1:
			str = str[k+5:]
		Object.parse(self, str)
		self.name = self.type
		self.type = "class"
		self.behaviors = self.template_args
		self.template_args = []
	def parseBody(self, parser, body):
		parser.parse(body)
		if len(parser.classes) > 0:
			print "Not supported inbody classes"
		self.members = parser.objects;
		self.functions = parser.functions;
		return
