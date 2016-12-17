import re
from Writer import Writer
from Object import Object
from Class import Class
from Function import Function

FLAG_HPP = 2
FLAG_CPP = 4
SERIALIZATION = 0
DESERIALIZATION = 1

class WriterCpp(Writer):
	def __init__(self, outDirectory, parser):
		#{0} - field name
		#{1} - field type
		#{2} - field initialize value
		#{3} - {
		#{4} - }
		#{5}, {6}, ... - arguments of field type (list<int>)
		self.serialize_formats = []
		self.serialize_formats.append({})
		self.serialize_formats.append({})
		
		self.serialize_formats[SERIALIZATION]["simple"] = []
		self.serialize_formats[SERIALIZATION]["simple"].append( "if({0} != {2}) \n\t\t  json.append_node( \"{0}\" ).set<{1}>( {0} )" )
		self.serialize_formats[SERIALIZATION]["simple"].append( "json.append_node( \"{0}\" ).set<{1}>( {0} )" )
		self.serialize_formats[DESERIALIZATION]["simple"] = []
		self.serialize_formats[DESERIALIZATION]["simple"].append( "if(json.is_exist(\"{0}\")) \n\t\t {0} = json.get<{1}>( \"{0}\" );\n\telse \n\t\t{0} = {2}" )
		self.serialize_formats[DESERIALIZATION]["simple"].append( "{0} = json.get<{1}>( \"{0}\" )" )
		
		self.serialize_formats[SERIALIZATION]["serialized"] = []
		self.serialize_formats[SERIALIZATION]["serialized"].append( "static_assert(0, \"field '{0}' not should have a initialize value\")" )
		self.serialize_formats[SERIALIZATION]["serialized"].append( "{0}.serialize(json.append_node(\"{0}\"))" )
		self.serialize_formats[DESERIALIZATION]["serialized"] = []
		self.serialize_formats[DESERIALIZATION]["serialized"].append( "static_assert(0, \"field '{0}' not should have a initialize value\")" )
		self.serialize_formats[DESERIALIZATION]["serialized"].append( "{0}.deserialize(json.append_node(\"{0}\"))" )
		
		self.serialize_formats[SERIALIZATION]["simple_list"] = []
		self.serialize_formats[SERIALIZATION]["simple_list"].append( "static_assert(0, \"list '{0}' not should have a initialize value\")" )
		self.serialize_formats[SERIALIZATION]["simple_list"].append( "auto arr_{0} = json.append_array( \"{0}\" );\n\tfor( auto& t : {0} )\n\t\tarr_{0}.push_back().set<{5}>( t )" )
		self.serialize_formats[DESERIALIZATION]["simple_list"] = []
		self.serialize_formats[DESERIALIZATION]["simple_list"].append( "static_assert(0, \"list '{0}' not should have a initialize value\")" )
		self.serialize_formats[DESERIALIZATION]["simple_list"].append( "auto arr_{0} = json.node( \"{0}\" );\n\tfor( size_t i = 0; i < arr_{0}.size(); ++i )\n\t{3}\n\t\t{0}.emplace_back();\n\t\t{0}.back() = arr_{0}.get<{5}>(i);\n\t{4}" )
		
		self.serialize_formats[SERIALIZATION]["serialized_list"] = []
		self.serialize_formats[SERIALIZATION]["serialized_list"].append( "static_assert(0, \"list '{0}' not should have a initialize value\")" )
		self.serialize_formats[SERIALIZATION]["serialized_list"].append( "auto arr_{0} = json.append_array( \"{0}\" );\n\tfor( auto& t : {0} )\n\t\tt.serialize(arr_{0}.push_back());" )
		self.serialize_formats[DESERIALIZATION]["serialized_list"] = []
		self.serialize_formats[DESERIALIZATION]["serialized_list"].append( "static_assert(0, \"list '{0}' not should have a initialize value\")" )
		self.serialize_formats[DESERIALIZATION]["serialized_list"].append( "auto arr_{0} = json.node( \"{0}\" );\n\tfor( size_t i = 0; i < arr_{0}.size(); ++i )\n\t{3}\n\t\t{0}.emplace_back();\n\t\t{0}.back().deserialize(arr_{0}.at(i));\n\t{4}" )

		self.simple_types = ["int", "float", "bool", "string"]
		for i in range(2):
			for type in self.simple_types:
				self.serialize_formats[i][type] = []
				self.serialize_formats[i][type].append( self.serialize_formats[i]["simple"][0] )
				self.serialize_formats[i][type].append( self.serialize_formats[i]["simple"][1] )
				list_type = "list<{0}>".format(type)
				self.serialize_formats[i][list_type] = []
				self.serialize_formats[i][list_type].append( self.serialize_formats[i]["simple_list"][0] )
				self.serialize_formats[i][list_type].append( self.serialize_formats[i]["simple_list"][1] )

			self.serialize_formats[i]["list<serialized>"] = []
			self.serialize_formats[i]["list<serialized>"].append( self.serialize_formats[i]["serialized_list"][0] )
			self.serialize_formats[i]["list<serialized>"].append( self.serialize_formats[i]["serialized_list"][1] )

		Writer.__init__(self, outDirectory, parser)
		self._currentClass = None
		return
	
	def writeObject(self, object, tabs, flags):
		out = Writer.writeObject(self, object, tabs, flags)
		value = ""
		args = ", ".join(object.template_args)
		if len(object.template_args) > 0:
			fstr = "{3}{0}<{2}> {1}"
		else:
			fstr = "{3}{0} {1}"
		fstr += ";\n"
		out[flags] += fstr.format(object.type, object.name, args, self.tabs(tabs))
		return out

	def writeClass(self, cls, tabs, flags):
		out = {}
		cls = self.addMethods(cls);

		if flags & FLAG_HPP:
			out = Writer._add(self, out, self._writeClassHpp(cls, tabs))
		if flags & FLAG_CPP:
			out = Writer._add(self, out, self._writeClassCpp(cls, tabs))
		return out
	
	def _writeClassHpp(self, cls, tabs):
		out = Writer.writeClass(self, cls, tabs, FLAG_HPP)
		self._currentClass = cls
		behaviors = ", ".join(cls.behaviors)
		objects = self.writeObjects(cls.members, 1, FLAG_HPP)
		functions = self.writeFunctions(cls.functions, 1, FLAG_HPP)
		constructor = self._createConstructorFunctionHpp(cls, 1)
		self._currentClass = None

		fstr = ""
		if len(cls.behaviors) > 0: fstr += "{0} {1} : public {2}"
		else: fstr += "{0} {1}"
		if functions[FLAG_HPP].strip() == "": F = ""
		else: F = "\n{4}"
		if objects[FLAG_HPP].strip() == "": O = ""
		else: O = "\nprotected:\n{3}"

		fstr += "\n__begin__\npublic:\n{5}" + F + O + "__end__;\n\n"

		fstr = "namespace {0}\n__begin__\n\n{1}__end__//namespace {0}".format( self._getNamespace(cls), fstr )
		fstr = "#ifndef __{0}_h__\n#define __{0}_h__\n\n{1}\n\n#endif //#ifndef __{0}_h__".format( cls.name, fstr )

		out[FLAG_HPP] += fstr.format( cls.type, cls.name, behaviors, objects[FLAG_HPP], functions[FLAG_HPP], constructor);
		out[FLAG_HPP] = re.sub("__begin__", "{", out[FLAG_HPP])
		out[FLAG_HPP] = re.sub("__end__", "}", out[FLAG_HPP])
		return out

	def _writeClassCpp(self, cls, tabs):
		out = Writer.writeClass(self, cls, tabs, FLAG_CPP)
		self._currentClass = cls
		functions = self.writeFunctions(cls.functions, 0, FLAG_CPP)
		constructor = self._createConstructorFunctionCpp(cls, tabs)
		self._currentClass = None
		fstr = "#include\"{0}.h\"\n\nnamespace {3}\n__begin__\n\n{2}\n{1}__end__"
		out[FLAG_CPP] += fstr.format( cls.name, functions[FLAG_CPP], constructor, self._getNamespace(cls) )
		out[FLAG_CPP] = re.sub("__begin__", "{", out[FLAG_CPP])
		out[FLAG_CPP] = re.sub("__end__", "}", out[FLAG_CPP])
		return out
	
	def _createConstructorFunctionHpp(self, cls, tabs):
		fstr = "{1}{0}();\n"
		return fstr.format( cls.name, self.tabs(tabs) )

	def _createConstructorFunctionCpp(self, cls, tabs):
		initialize = ""
		for obj in cls.members:
			if obj.initial_value != None:
				fstr = "\n\t{2} {0}({1})"
				s = ","
				if initialize == "": 
					s = ":"
				str = fstr.format(obj.name, obj.initial_value, s)
				initialize += str

		fstr = "{0}::{0}(){1}\n__begin__\n{2}\n__end__\n"
		str = fstr.format( cls.name, initialize, self.tabs(tabs) )
		str = re.sub("__begin__", "{", str)
		str = re.sub("__end__", "}", str)
		return str
	
	def writeFunction(self, function, tabs, flags):
		out = {}
		if flags & FLAG_HPP:
			if not self._currentClass.is_abstract:
				fstr = "{3}virtual {0} {1}({2}) {4};\n"
			else:
				fstr = "{3}virtual {0} {1}({2}) = 0;\n"
			args = []
			for arg in function.args:
				args.append(function.args[arg] + " " + arg)
			args = ", ".join(args)
			#TODO: find function in behavior classes
			is_override = "" # "override"
			out[FLAG_HPP] = fstr.format( function.return_type, function.name, args, self.tabs(tabs), is_override )
		if flags & FLAG_CPP:
			header = "{4}{0} {5}::{1}({2})\n"
			body = "{4}__begin__{3}\n{4}__end__\n\n"
			fstr = header + body
			body = ""
			for operation in function.operations:
				fline = "{0};"
				line = "\n" + self.tabs(tabs+1) + fline.format(operation);
				body += line
			args = []
			for arg in function.args:
				args.append(function.args[arg] + " " + arg)
			args = ", ".join(args)
			out[FLAG_CPP] = fstr.format( function.return_type, function.name, args, body, self.tabs(tabs), self._currentClass.name )
			out[FLAG_CPP] = re.sub("self.", "this->", out[FLAG_CPP])

		return out

	def writeClasses(self, classes, tabs, flags):
		out = {FLAG_CPP : "", FLAG_HPP : ""}
		for cls in classes:
			dict = self.writeClass(cls, tabs, FLAG_HPP)
			self.save( cls.name + ".h", dict[FLAG_HPP] )
			out = self._add( out, dict )
		for cls in classes: 
			if not cls.is_abstract:
				dict = self.writeClass(cls, tabs, FLAG_CPP)
				self.save( cls.name + ".cpp", dict[FLAG_CPP] )
				out = self._add( out, dict )
		return out

	def writeFunctions(self, functions, tabs, flags):
		out = {FLAG_CPP : "", FLAG_HPP : ""}
		for function in functions: 
			out = self._add( out, self.writeFunction(function, tabs, flags) )
		return out

	def _getNamespace(self, cls):
		return "mg"

	def addMethods(self, cls):
		if self.isSerialised(cls):
			have = False
			for function in cls.functions:
				if function.name == "serialize":
					have = True
					break
			if have == False:
				self.addSerialization(cls, SERIALIZATION)
				self.addSerialization(cls, DESERIALIZATION)
			
		return cls

	def isSerialised(self, cls):
		return cls.is_serialized or "SerializedObject" in cls.behaviors

	def addSerialization(self, cls, serialization_type):

		function = Function()
		if serialization_type == SERIALIZATION:
			function.name = "serialize";
			function.args["json"] = "RapidJsonNode&";
		if serialization_type == DESERIALIZATION:
			function.name = "deserialize";
			function.args["json"] = "const RapidJsonNode&";
		function.return_type = "void";
		for obj in cls.members:
			index = 0 
			if obj.initial_value == None:
				index = 1
			
			type = obj.type
			if not type in self.simple_types and type != "list":
				type = "serialized"
			if len(obj.template_args) > 0:
				if obj.template_args[0] in self.simple_types:
					type = "{0}<{1}>".format( type, obj.template_args[0] )
				else:
					type = "{0}<serialized>".format( type )

			fstr = self.serialize_formats[serialization_type][type][index]
			str = fstr.format(obj.name, obj.type, obj.initial_value, "{", "}", *obj.template_args)
			function.operations.append(str)
		cls.functions.append(function)
