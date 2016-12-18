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
		self.type = "class"

	def parse(self, line):
		str = line.strip()
		k = str.find(self.type)
		if k > -1:
			str = str[len(self.type):]
		str = self._findModifiers(str)
		
		type = self.type
		self.type = ""
		Object.parse(self, str)
		self.name = self.type
		self.type = type
		self.behaviors = self.template_args
		self.template_args = []
	def parseBody(self, parser, body):
		parser.parse(body)
		if len(parser.classes) > 0:
			print "Not supported inbody classes"
		self.members = parser.objects;
		self.functions = parser.functions;
		if self.type == "enum":
			self.convertToEnum()
		return

	def _findModifiers(self, str):
		self.is_abstract = self.is_abstract or str.find( ":abstract" ) != -1
		self.is_serialized = self.is_serialized or str.find( ":serialized" ) != -1
		self.is_visitor = self.is_visitor or str.find( ":visitor" ) != -1
		str = re.sub(":abstract", "", str)
		str = re.sub(":serialized", "", str)
		str = re.sub(":visitor", "", str)
		return str

	def convertToEnum(self):
		shift = 0
		if len(self.behaviors) == 0:
			self.behaviors.append("int")
		cast = self.behaviors[0]
		for m in self.members:
			m.name = m.type
			m.type = cast
			m.is_static = True
			m.is_const = True
			if cast == "int":
				m.initial_value = str(1 << shift)
			else:
				#TODO
				exit(-1)
			shift += 1
		self.behaviors = []

		value = Object()
		value.initial_value = self.members[0].name;
		value.name = "_value";
		value.type = cast;
		self.members.append( value )

		def createFunction(type, name, args, const):
			function = Function()
			function.return_type = type;
			function.name = name;
			function.args = args;
			function.is_const = const;
			self.functions.append( function )
			return function;
		
		function = createFunction("", self.name, [], False).operations = ["_value = " + self.members[0].name];
		function = createFunction("", self.name, [["value",cast]], False).operations = ["_value = value"];
		function = createFunction("", self.name, [["rhs","const EquipmentItemType&"]], False).operations = ["_value = rhs._value"];
		function = createFunction("", "operator int", [], True).operations = ["return _value"];
		function = createFunction("const EquipmentItemType&", "operator =", [["rhs","const EquipmentItemType&"]], False).operations = ["_value = rhs._value", "return *this"];
		function = createFunction("bool", "operator ==", [["rhs","const EquipmentItemType&"]], True).operations = ["return _value == rhs._value"];
		function = createFunction("bool", "operator <", [["rhs","const EquipmentItemType&"]], True).operations = ["return _value < rhs._value"];
		
		function1 = createFunction("", self.name, [["value", "const string&"]], False)
		function2 = createFunction("const EquipmentItemType&", "operator =", [["value", "const string&"]], False)
		function3 = createFunction("", "operator string", [], True)
		for m in self.members:
			function1.operations.append( re.sub("__e__","}", re.sub("__b__","{", "if( value == \"{0}\" ) __b__ _value = {0}; return; __e__".format( m.name ) ) ) )
			function2.operations.append( re.sub("__e__","}", re.sub("__b__","{", "if( value == \"{0}\" ) __b__ _value = {0}; return *this; __e__".format( m.name ) ) ) )
			function3.operations.append( "if( _value == {0} ) return \"{0}\"".format( m.name ) )
		function1.operations.append( "_value = 0" )
		function2.operations.append( "return *this" )
		function3.operations.append( "return \"\"" )


		
		
