import re
from Object import Object
from Function import Function

class Class(Object):
	def __init__(self):
		Object.__init__(self)
		self.behaviors = []
		self.members = []
		self.functions = []
		self.is_abstract = False
		self.is_serialized = False
		self.is_visitor = False

	def parse(self, line):
		str = line.strip()
		k = str.find("class")
		if k > -1:
			str = str[k+5:]
		str = self._findModifiers(str)

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

	def _findModifiers(self, str):
		self.is_abstract = self.is_abstract or str.find( ":abstract" ) != -1
		self.is_serialized = self.is_serialized or str.find( ":serialized" ) != -1
		self.is_visitor = self.is_visitor or str.find( ":visitor" ) != -1
		str = re.sub(":abstract", "", str)
		str = re.sub(":serialized", "", str)
		str = re.sub(":visitor", "", str)
		return str