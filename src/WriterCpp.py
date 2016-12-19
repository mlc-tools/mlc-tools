import re
import random
import fileutils
from Writer import Writer
from Object import Object
from Class import Class
from Function import Function

FLAG_HPP = 2
FLAG_CPP = 4
SERIALIZATION = 0
DESERIALIZATION = 1
TEST_FUNCTION_CREATE = "__create_instance__"


def convertType(type):
	types = {}
	types["cc.point"] = "cocos2d::Point"
	types["cc.point*"] = "cocos2d::Point*"
	types["list"] = "std::vector"
	types["string"] = "std::string"
	if type in types:
		return types[type]
	return type 

def getIncludeFile(file):
	types = {}
	types["cc.point"] = "\"cocos2d.h\""
	types["list"] = "<vector>"
	types["string"] = "<string>"
	types["pugi::xml_node"] = "\"pugixml/pugixml.hpp\""
	types["Json::Value"] = "\"jsoncpp/json.h\""
	if file in types:
		return types[file]
	return "\"{0}.h\"".format(file)

def autoReplaces(text):
	text = re.sub( "math.max", "std::max", text)
	text = re.sub( "math.min", "std::min", text)
	text = re.sub( "self.", "this->", text)
	text = re.sub( ".append", ".push_back", text)
	text = re.sub( ".push_back_node", ".append_node", text)
	text = re.sub( ".push_back_array", ".append_array", text)
	return text

class WriterCpp(Writer):
	def __init__(self, outDirectory, parser, createTests):
		#{0} - field name
		#{1} - field type
		#{2} - field initialize value
		#{3} - {
		#{4} - }
		#{5}, {6}, ... - arguments of field type (list<int>)
		self.createTests = createTests
		self.serialize_formats = []
		self.serialize_formats.append({})
		self.serialize_formats.append({})
		
		self.serialize_formats[SERIALIZATION]["simple"] = []
		self.serialize_formats[SERIALIZATION]["simple"].append( "if({0} != {2}) \n\t\tset(json,\"{0}\",{0})" )
		self.serialize_formats[SERIALIZATION]["simple"].append( "set(json,\"{0}\",{0})" )
		self.serialize_formats[DESERIALIZATION]["simple"] = []
		self.serialize_formats[DESERIALIZATION]["simple"].append( "if(json.isMember(\"{0}\")) \n\t\t {0} = get<{1}>( json[\"{0}\"] );\n\telse \n\t\t{0} = {2}" )
		self.serialize_formats[DESERIALIZATION]["simple"].append( "{0} = get<{1}>( json[\"{0}\"] )" )
		
		self.serialize_formats[SERIALIZATION]["serialized"] = []
		self.serialize_formats[SERIALIZATION]["serialized"].append( "static_assert(0, \"field '{0}' not should have a initialize value\")" )
		self.serialize_formats[SERIALIZATION]["serialized"].append( "{0}.serialize(json[\"{0}\"])" )
		self.serialize_formats[DESERIALIZATION]["serialized"] = []
		self.serialize_formats[DESERIALIZATION]["serialized"].append( "static_assert(0, \"field '{0}' not should have a initialize value\")" )
		self.serialize_formats[DESERIALIZATION]["serialized"].append( "{0}.deserialize(json[\"{0}\"])" )
		
		self.serialize_formats[SERIALIZATION]["simple_list"] = []
		self.serialize_formats[SERIALIZATION]["simple_list"].append( "static_assert(0, \"list '{0}' not should have a initialize value\")" )
		self.serialize_formats[SERIALIZATION]["simple_list"].append( "__begin__auto& arr_{0} = json[\"{0}\"];\n\tsize_t i=0; for( auto& t : {0} )\n\t\tset(arr_{0}[i++], t);__end__" )
		self.serialize_formats[DESERIALIZATION]["simple_list"] = []
		self.serialize_formats[DESERIALIZATION]["simple_list"].append( "static_assert(0, \"list '{0}' not should have a initialize value\")" )
		self.serialize_formats[DESERIALIZATION]["simple_list"].append( "auto& arr_{0} = json[\"{0}\"];\n\tfor( size_t i = 0; i < arr_{0}.size(); ++i )\n\t{3}\n\t\t{0}.emplace_back();\n\t\t{0}.back() = get<{5}>(arr_{0}[i]);\n\t{4}" )
		
		self.serialize_formats[SERIALIZATION]["serialized_list"] = []
		self.serialize_formats[SERIALIZATION]["serialized_list"].append( "static_assert(0, \"list '{0}' not should have a initialize value\")" )
		self.serialize_formats[SERIALIZATION]["serialized_list"].append( "__begin__auto& arr_{0} = json[\"{0}\"];\n\tsize_t i=0; for( auto& t : {0} )\n\t\tt.serialize(arr_{0}[i++]);__end__" )
		self.serialize_formats[DESERIALIZATION]["serialized_list"] = []
		self.serialize_formats[DESERIALIZATION]["serialized_list"].append( "static_assert(0, \"list '{0}' not should have a initialize value\")" )
		self.serialize_formats[DESERIALIZATION]["serialized_list"].append( "auto& arr_{0} = json[\"{0}\"];\n\tfor( size_t i = 0; i < arr_{0}.size(); ++i )\n\t{3}\n\t\t{0}.emplace_back();\n\t\t{0}.back().deserialize(arr_{0}[i]);\n\t{4}" )

		self.simple_types = ["int", "float", "bool", "string", "cc.point"]
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

		self.tests = []
		Writer.__init__(self, outDirectory, parser)
		self._currentClass = None
		if self.createTests:
			self._createTests()
		return
	
	def writeObject(self, object, tabs, flags):
		out = Writer.writeObject(self, object, tabs, flags)
		if flags == FLAG_HPP:
			value = ""
			args = ", ".join(object.template_args)
			modifiers = ""
			if object.is_static:
				modifiers += "static "
			if object.is_const:
				modifiers += "const ";
			if len(object.template_args) > 0:
				fstr = "{4}{3}{0}<{2}> {1}"
			else:
				fstr = "{4}{3}{0} {1}"
			fstr += ";\n"
			out[flags] += fstr.format(convertType(object.type), object.name, args, modifiers, self.tabs(tabs))
		if flags == FLAG_CPP:
			if object.is_static:
				if object.initial_value == None:
					print "static object have not initial_value"
					exit(-1)
				if len(object.template_args) > 0:
					#TODO:
					exit(-1)
				value = ""
				fstr = "{4}{0} {2}::{1} = {3}"
				fstr += ";\n"
				modifier = ""
				if object.is_const:
					modifier = "const "
				out[flags] += fstr.format(convertType(object.type), object.name, self._currentClass.name, object.initial_value, modifier)
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
		behaviors = []
		for c in cls.behaviors:
			behaviors.append("public " + c.name)
		behaviors = ", ".join(behaviors)
		objects = self.writeObjects(cls.members, 1, FLAG_HPP)
		functions = self.writeFunctions(cls.functions, 1, FLAG_HPP)
		constructor = self._createConstructorFunctionHpp(cls, 1)
		includes, forward_declarations = self._findIncludes(cls,FLAG_HPP)
		self._currentClass = None

		fstr = ""
		if len(cls.behaviors) > 0: 
			fstr += "{0} {1} : {2}"
		else:
		    fstr += "{0} {1}"
		if functions[FLAG_HPP].strip() == "": 
			F = ""
		else:
		    F = "\n{4}"
		if objects[FLAG_HPP].strip() == "":
		    O = ""
		else:
		    O = "\npublic:{3}"

		if cls.type != "enum":
			fstr += "\n__begin__\npublic:\n{5}" + F + O + "__end__;\n\n"
		else:
			fstr += "\n__begin__{5}" + O + F + "__end__;\n\n"

		fstr = "namespace {0}\n__begin__\n{2}\n\n{1}__end__//namespace {0}".format( self._getNamespace(cls), fstr, forward_declarations )
		fstr = "#ifndef __{0}_h__\n#define __{0}_h__\n{2}\n\n{1}\n\n#endif //#ifndef __{0}_h__".format( cls.name, fstr, includes )

		out[FLAG_HPP] += fstr.format( "class", cls.name, behaviors, objects[FLAG_HPP], functions[FLAG_HPP], constructor);
		out[FLAG_HPP] = re.sub("__begin__", "{", out[FLAG_HPP])
		out[FLAG_HPP] = re.sub("__end__", "}", out[FLAG_HPP])
		return out

	def _writeClassCpp(self, cls, tabs):
		out = Writer.writeClass(self, cls, tabs, FLAG_CPP)
		self._currentClass = cls
		objects = self.writeObjects(cls.members, 1, FLAG_CPP)
		functions = self.writeFunctions(cls.functions, 0, FLAG_CPP)
		constructor = self._createConstructorFunctionCpp(cls, tabs)
		includes, f = self._findIncludes(cls,FLAG_CPP)
		self._currentClass = None
		if cls.type == "class":
			fstr = "#include \"{0}.h\"\n#include \"Generics.h\"{4}\n\nnamespace {3}\n__begin__\n{5}\nREGISTRATION_OBJECT( {0} );\n{2}\n{1}__end__"
		else:
			fstr = "#include \"{0}.h\"\n#include \"Generics.h\"{4}\n\nnamespace {3}\n__begin__\n{5}\n{2}\n{1}__end__"
		out[FLAG_CPP] += fstr.format( cls.name, functions[FLAG_CPP], constructor, self._getNamespace(cls), includes, objects[FLAG_CPP] )
		out[FLAG_CPP] = re.sub("__begin__", "{", out[FLAG_CPP])
		out[FLAG_CPP] = re.sub("__end__", "}", out[FLAG_CPP])
		return out
	
	def _createConstructorFunctionHpp(self, cls, tabs):
		if cls.type == "enum":
			return ""
		fstr = "{1}{0}()"
		fstr = fstr.format( cls.name, self.tabs(tabs) )
		if cls.is_abstract:
			fstr += "{}"
		fstr += ";\n"
		return fstr

	def _createConstructorFunctionCpp(self, cls, tabs):
		if cls.type == "enum":
			return ""
		initialize = ""
		initialize2 = ""
		for obj in cls.members:
			if obj.is_key:
				str1 = "\n\tstatic {0} {1}_key = 0;".format(obj.type, obj.name)
				str2 = "\n\t{0} = ++{0}_key;".format(obj.name)
				initialize2 += str1 + str2
			elif obj.initial_value != None and not obj.is_static:
				fstr = "\n\t{2} {0}({1})"
				s = ","
				if initialize == "": 
					s = ":"
				str = fstr.format(obj.name, obj.initial_value, s)
				initialize += str

		fstr = "{0}::{0}(){1}\n__begin__{2}\n{3}\n__end__\n"
		str = fstr.format( cls.name, initialize, initialize2, self.tabs(tabs) )
		str = re.sub("__begin__", "{", str)
		str = re.sub("__end__", "}", str)
		return str
		
	def writeFunction(self, function, tabs, flags):
		out = {}
		if flags & FLAG_HPP:
			if not self._currentClass.is_abstract and not function.is_abstract:
				fstr = "{3}{6}{0} {1}({2}){4}{5};\n"
			else:
				fstr = "{3}{6}{0} {1}({2}){4}{5} = 0;\n"
			args = []
			for arg in function.args:
				args.append(convertType(arg[1]) + " " + arg[0])
			args = ", ".join(args)
			modifier = "virtual "
			if function.is_static:
				modifier = "static "
			if function.name == self._currentClass.name or function.name.find("operator ") == 0:
				modifier = ""
			is_override = ""
			if self.parser.isFunctionOverride(self._currentClass, function):
				is_override = " override"
			is_const = ""
			if function.is_const:
				is_const = " const"

			out[FLAG_HPP] = fstr.format( convertType(function.return_type), function.name, args, self.tabs(tabs), is_const, is_override, modifier )
		if flags & FLAG_CPP and not function.is_external and not function.is_abstract:
			is_const = ""
			if function.is_const:
				is_const = "const"
			header = "{4}{0} {5}::{1}({2}) {6}\n"
			body = "{4}__begin__{3}\n{4}__end__\n\n"
			fstr = header + body
			body = ""
			for operation in function.operations:
				fline = "{0};"
				line = "\n" + self.tabs(tabs+1) + fline.format(operation);
				body += line
			args = []
			for arg in function.args:
				args.append(convertType(arg[1]) + " " + arg[0])
			args = ", ".join(args)
			out[FLAG_CPP] = fstr.format( convertType(function.return_type), function.name, args, body, self.tabs(tabs), self._currentClass.name, is_const )
			out[FLAG_CPP] = autoReplaces( out[FLAG_CPP] )

		return out

	def writeClasses(self, classes, tabs, flags):
		out = {FLAG_CPP : "", FLAG_HPP : ""}
		for cls in classes:
			if not cls.is_abstract:
				self.tests.append(cls)

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
		if cls.is_serialized or cls.type == "enum":
			have = False
			for function in cls.functions:
				if function.name == "serialize":
					have = True
					break
			if have == False:
				self.addSerialization(cls, SERIALIZATION)
				self.addSerialization(cls, DESERIALIZATION)
		if cls.is_visitor:
			have = False
			for function in cls.functions:
				if function.name == "accept":
					have = True
					break
			if have == False:
				self.addAccept(cls)
		if not cls.is_abstract:
			have = False
			for function in cls.functions:
				if function.name == "operator ==":
					have = True
					break
			if have == False:
				self.addEquals(cls)
		if self.createTests and not cls.is_abstract:
			have = False
			for function in cls.functions:
				if function.name == TEST_FUNCTION_CREATE:
					have = True
					break
			if have == False:
				self.addTests(cls)
			
		return cls

	def addSerialization(self, cls, serialization_type):

		function = Function()
		if serialization_type == SERIALIZATION:
			function.is_const = True
			function.name = "serialize"
			function.args.append(["json","Json::Value&"])
		if serialization_type == DESERIALIZATION:
			function.name = "deserialize"
			function.args.append(["json", "const Json::Value&"])
		function.return_type = "void"

		for behabior in cls.behaviors:
			if not behabior.is_serialized or behabior.is_abstract:
				continue
			str = "{0}::{1}(json)".format( behabior.name, function.name )
			function.operations.append(str)

		for obj in cls.members:
			if obj.is_runtime or obj.is_static or obj.is_const:
				continue
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
			str = fstr.format(obj.name, convertType(obj.type), obj.initial_value, "{", "}", *obj.template_args)
			function.operations.append(str)
		cls.functions.append(function)

	def addAccept(self, cls):
		visitor = self.parser.getVisitorType(cls)
		if visitor == cls.name:
			return
		function = Function()
		function.name = "accept"
		function.return_type = "void"
		function.args.append(["visitor", visitor + "*"])
		function.operations.append("visitor->visit( this )")
		cls.functions.append(function)

	def addEquals(self, cls):
		function = Function()
		function.name = "operator =="
		function.return_type = "bool"
		function.args.append(["rhs", "const " + cls.name + "&"])
		function.is_const = True
		fbody_line = "result = result && {0} == rhs.{0}"
		function.operations.append( "bool result = true");
		for m in cls.members:
			if m.is_static or m.is_const:
				continue
			function.operations.append( fbody_line.format(m.name) )
		function.operations.append( "return result");
		cls.functions.append(function)

	def addTests(self, cls):
		function = Function()
		function.name = TEST_FUNCTION_CREATE
		function.return_type = cls.name
		function.is_static = True

		fbody_line = "instance.{0} = {1}"
		function.operations.append( "{0} instance".format(cls.name) );
		for m in cls.members:
			value = self._getTestValue(m)
			if value == None:
				continue
			if m.is_const or m.is_static:
				continue
			str = fbody_line.format(m.name, value)
			function.operations.append( str )
		function.operations.append( "return instance");

		cls.functions.append(function)

	def _getTestValue(self, m):
		value = ""
		if m.is_runtime:
			return None
		if m.type == "list":
			return None
		if m.type == "int" or m.type == "float":
			value = str(random.randint(-99999, 99999))
		if m.type == "bool":
			value = str(random.randint(0, 1))
		if m.type == "cc.point":
			value = "cocos2d::Point({0},{1})".format(random.randint(-99999, 99999), random.randint(-99999, 99999))
		if self.parser._findClass(m.type):
			value = "{0}::{1}()".format(m.type,TEST_FUNCTION_CREATE)
		elif m.type == "string":
			value = "\"somestringvalue\""
		if value == "":
			value = "0"
		return value

	def _findIncludes(self, cls, flags):
		out = ""
		forward_declarations = ""

		fstr = "\n#include {0}"

		def need_include(type):
			if type == "":
				return False
			types = []
			types.append( "int" )
			types.append( "float" )
			types.append( "bool" )
			types.append( "void" )
			return not type in types

		types = {}
		ftypes = {}
		
		for t in cls.behaviors:
			types[t.name] = 1
		for t in cls.members:
			type = t.type
			type = re.sub( "const", "", type ).strip()
			type = re.sub( "\*", "", type ).strip()
			type = re.sub( "&", "", type ).strip()
			types[type] = 1
			for arg in t.template_args:
				types[arg] = 1
		for f in cls.functions:
			for t in f.args:
				type = re.sub("const", "", t[1]).strip()
				type = re.sub("\*", "", type).strip()
				type = re.sub("&", "", type).strip()
				if flags == FLAG_CPP or t[1] != type + "*":
					types[type] = 1
				if flags == FLAG_HPP and t[1] == type + "*":
					ftypes[type] = 1

			type = f.return_type
			type = re.sub( "const", "", type ).strip()
			type = re.sub( "\*", "", type ).strip()
			type = re.sub( "&", "", type ).strip()
			types[type] = 1

		for t in types:
			if need_include(t):
				out += fstr.format( getIncludeFile(t) )
		
		for t in ftypes:
			type = convertType(t)
			if type.find( "::" ) == -1:
				forward_declarations += "\nclass {0};".format( type )
			else:
				continue
				ns = type[0:type.find( "::" )]
				type = type[type.find( "::" )+2:]
				str = "\nnamespace {1}\n__begin__\n\tclass {0};\n__end__".format( type, ns );
				forward_declarations += str

		if flags == FLAG_CPP:
			out += "\n#include \"Factory.h\""
		return out, forward_declarations

	def _createTests(self):
		fstr = "#include \"TestSerialization.h\"\n{0}\n\nvoid TestSerialization::build()\n__begin__\n{1}\n__end__\n"
		includes = ""
		tests = ""
		for cls in self.tests:
			finc = "#include \"../../../out/{}.cpp\"\n".format(cls.name)
			ftst = "\t_tests.push_back( new TestT<mg::{}> );\n".format(cls.name)
			includes += finc
			if self.createTests:
				tests += ftst
		fstr = fstr.format( includes, tests )
		fstr = re.sub("__begin__", "{", fstr)
		fstr = re.sub("__end__", "}", fstr)
		fileutils.write("tests/cpp/TestCpp/TestSerialization.cpp", fstr)