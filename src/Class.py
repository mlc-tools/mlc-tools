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
		self.generate_set_function = False
		self.type = "class"
		self.group = ""

	def parse(self, line):
		str = line.strip()
		if self.type in str:
		   str = str[len(self.type):]
		str = self._findModifiers(str)
		type = self.type
		self.type = ""
		Object.parse(self, str)
		self.name = self.type
		self.type = type
		self.behaviors = self.template_args
		self.template_args = []
		if "/" in self.name:
			k = self.name.rindex("/")
			self.group = self.name[0:k]
			self.name = self.name[k+1:]

	def parseBody(self, parser, body):
		parser.parse(body)
		if len(parser.classes) > 0:
			print "Not supported inbody classes"
		self.members = parser.objects;
		self.functions = parser.functions;
		if self.type == "enum":
			self.convertToEnum()
		return

	def onLinked(self):
		if self.generate_set_function:
			self._generateSettersFunction()
			self._generateGettersFunction()

	def _findModifiers(self, str):
		self.is_abstract = self.is_abstract or ":abstract" in str
		self.is_serialized = self.is_serialized or ":serialized" in str
		self.is_visitor = self.is_visitor or ":visitor" in str
		self.generate_set_function = self.generate_set_function or ":set_function" in str
		str = re.sub(":abstract", "", str)
		str = re.sub(":serialized", "", str)
		str = re.sub(":visitor", "", str)
		str = re.sub(":set_function", "", str)
		return str

	def _generateSettersFunction(self):
		function = Function();
		function.name = "set"
		function.return_type = "void"
		function.args.append(["name", "string"])
		function.args.append(["value", "string"])

		add_function = False
		for i, member in enumerate(self.members):
			if member.is_pointer:
				continue
			if member.is_runtime:
				continue
			if member.is_static:
				continue
			if member.is_const:
				continue
			supported_types = { "string":"std::string", "int":0, "float":0, "bool":0 }
			if member.type in supported_types:
				type = member.type
				type = type if supported_types[type] == 0 else supported_types[type] 
				if i == 0:
					op = 'if( name == "{0}" ) \n{2}\n{0} = strTo<{1}>(value);\n{3}'.format( member.name, type, '{', '}' )
				else:
					op = 'else if( name == "{0}" )\n{2}\n{0} = strTo<{1}>(value);\n{3}'.format( member.name, type, '{', '}' )
				function.operations.append(op)
				add_function = True
		
		override = False
		if self.behaviors:
			for cls in self.behaviors:
				for func in cls.functions:
					equal = func.name == function.name and func.return_type == function.return_type
					for i, arg in enumerate(func.args):
						equal = equal and func.args[i][1] == function.args[i][1]
					if equal:
						override = True
						if len(function.operations):
							op = "else \n{1}\n{0}::set(name, value);\n{2}".format(cls.name, '{', '}')
						else:
							op = "{0}::set(name, value);".format(cls.name)
						function.operations.append(op)
						break;
		
		if add_function or not override:
			self.functions.append(function)


	def _generateGettersFunction(self):
		function = Function();
		function.name = "get"
		function.return_type = "string"
		function.args.append(["name", "string"])

		add_function = False
		for i, member in enumerate(self.members):
			if member.is_pointer:
				continue
			if member.is_runtime:
				continue
			if member.is_static:
				continue
			if member.is_const:
				continue
			supported_types = [ "string", "int", "float", "bool" ]
			if member.type in supported_types:
				type = member.type
				if i == 0:
					op = 'if( name == "{0}" ) \n{2}\n return toStr({0});\n{3}'.format( member.name, type, '{', '}' )
				else:
					op = 'else if( name == "{0}" ) \n{2}\n return toStr({0});\n{3}'.format( member.name, type, '{', '}' )
				function.operations.append(op)
				add_function = True
		
		override = False
		if self.behaviors:
			for cls in self.behaviors:
				for func in cls.functions:
					equal = func.name == function.name and func.return_type == function.return_type
					for i, arg in enumerate(func.args):
						equal = equal and func.args[i][1] == function.args[i][1]
					if equal:
						override = True
						if len(function.operations):
							op = "else \n{1}\n return {0}::get(name);\n{2}".format(cls.name, '{', '}')
						else:
							op = "return {0}::get(name, value);".format(cls.name)
						function.operations.append(op)
						break;
		if not override:
			function.operations.append('return "";')
		
		if add_function or not override:
			self.functions.append(function)

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
			if m.initial_value == None:
				if cast == "int":
					m.initial_value = "(1 << {})".format( shift )
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
		
		function = createFunction("", self.name, [], False).operations = ["_value = {};".format(self.members[0].name)];
		function = createFunction("", self.name, [["value",cast]], False).operations = ["_value = value;"];
		function = createFunction("", self.name, [["rhs","const {0}&".format(self.name)]], False).operations = ["_value = rhs._value;"];
		function = createFunction("", "operator int", [], True).operations = ["return _value;"];
		function = createFunction("const {0}&".format(self.name), "operator =", [["rhs","const {0}&".format(self.name)]], False).operations = ["_value = rhs._value;", "return *this;"];
		function = createFunction("bool", "operator ==", [["rhs","const {0}&".format(self.name)]], True).operations = ["return _value == rhs._value;"];
		function = createFunction("bool", "operator ==", [["rhs","int"]], True).operations = ["return _value == rhs;"];
		function = createFunction("bool", "operator <", [["rhs","const {0}&".format(self.name)]], True).operations = ["return _value < rhs._value;"];
		
		function1 = createFunction("", self.name, [["value", "string"]], False)
		function2 = createFunction("const {0}&".format(self.name), "operator =", [["value", "string"]], False)
		function3 = createFunction("", "operator std::string", [], True)
		for m in self.members:
			function1.operations.append( re.sub("__e__","}", re.sub("__b__","{", "if( value == \"{0}\" ) __b__ _value = {0}; return; __e__;".format( m.name ) ) ) )
			function2.operations.append( re.sub("__e__","}", re.sub("__b__","{", "if( value == \"{0}\" ) __b__ _value = {0}; return *this; __e__;".format( m.name ) ) ) )
			function3.operations.append( "if( _value == {0} ) return \"{0}\";".format( m.name ) )
		function1.operations.append( "_value = 0;" )
		function2.operations.append( "return *this;" )
		function3.operations.append( "return \"\";" )


		
		
