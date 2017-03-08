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


def random_int():
	max = 0;
	return random.randint(-max, max)
def random_bool():
	max = 0;
	return random.randint(0, max)
def random_float():
	max = 0;
	return random.randint(-max, max)

def convertType(type):
	types = {}
	types["cc.point"] = "cocos2d::Point"
	types["cc.point*"] = "cocos2d::Point*"
	types["list"] = "std::vector"
	types["map"] = "std::map"
	types["set"] = "std::set"
	types["string"] = "std::string"
	types["Observer"] = "Observer<std::function<void()>>"
	if type in types:
		return types[type]
	return type 

def convertArgumentType(type):
	if type == "string" or type == "std::string":
		return "const std::string&"
	return type

def autoReplaces(text):
	text = re.sub( "math.max", "std::max", text)
	text = re.sub( "math.min", "std::min", text)
	text = re.sub( "self.", "this->", text)
	#text = re.sub( ".append", ".push_back", text)
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
		self.create_serialization_patterns()
		
		self.tests = []
		Writer.__init__(self, outDirectory, parser)
		self._currentClass = None
		if self.createTests:
			self._createTests()
		return
	def create_serialization_patterns(self):
		pass

	def writeObject(self, object, tabs, flags):
		out = Writer.writeObject(self, object, tabs, flags)
		if object.side != 'both' and object.side != self.parser.side:
			return out

		if flags == FLAG_HPP:
			value = ""
			args = []
			for arg in object.template_args:
				type = arg.name if isinstance(arg, Class) else arg.type
				type = convertType(type)
				if arg.is_pointer:
					type = "IntrusivePtr<{}>".format(type)
				args.append(type)
			args = ", ".join(args)
			type = object.type
			if object.is_pointer:
				f = "{}*"
				cls = self.parser._findClass(object.type)
				if cls:
					for b in cls.behaviors:
						if b.name == "SerializedObject":
							f = "IntrusivePtr<{}>"
				type = f.format(convertType(type))
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
			out[flags] += fstr.format(convertType(type), object.name, args, modifiers, self.tabs(tabs))
		if flags == FLAG_CPP:
			if object.is_static:
				if object.initial_value == None:
					print "static object {} of class {} have not initial_value".format(object.name, self._currentClass.name)
					exit(-1)
				if len(object.template_args) > 0:
					#TODO:
					print "#TODO: static object {} of class {} have template arguments".format(object.name, self._currentClass.name)
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
		if cls.side != 'both' and cls.side != self.parser.side:
			return out
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
		destructor = self._createDestructorFunctionHpp(cls, tabs)
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
			fstr += "\n__begin__\npublic:\n{5}{6}" + F + O + "__end__;\n\n"
		else:
			fstr += "\n__begin__{5}" + O + F + "__end__;\n\n"

		fstr = "namespace {0}\n__begin__{2}\n\n{1}__end__//namespace {0}".format( self._getNamespace(cls), fstr, forward_declarations )
		fstr = "#ifndef __mg_{0}_h__\n#define __mg_{0}_h__\n{2}\n\n{1}\n\n#endif //#ifndef __{0}_h__".format( cls.name, fstr, includes )

		out[FLAG_HPP] += fstr.format( "class", cls.name, behaviors, objects[FLAG_HPP], functions[FLAG_HPP], constructor, destructor);
		out[FLAG_HPP] = re.sub("__begin__", "{", out[FLAG_HPP])
		out[FLAG_HPP] = re.sub("__end__", "}", out[FLAG_HPP])
		return out

	def _writeClassCpp(self, cls, tabs):
		out = Writer.writeClass(self, cls, tabs, FLAG_CPP)
		self._currentClass = cls
		objects = self.writeObjects(cls.members, 1, FLAG_CPP)
		functions = self.writeFunctions(cls.functions, 0, FLAG_CPP)
		constructor = self._createConstructorFunctionCpp(cls, tabs)
		destructor = self._createDestructorFunctionCpp(cls, tabs)
		includes, f = self._findIncludes(cls,FLAG_CPP)
		includes = self._findIncludesInFunctionOperation(cls, includes)

		self._currentClass = None
		if cls.type == "class":
			fstr = "#include \"{0}.h\"\n#include \"Generics.h\"\n#include \"DataStorage.h\"{4}\n\nnamespace {3}\n__begin__{5}{6}\n{2}\n{7}\n{1}__end__"
		else:
			fstr = "#include \"{0}.h\"\n#include \"Generics.h\"{4}\n\nnamespace {3}\n__begin__\n{5}\n{2}{7}\n{1}__end__"
		registration = "REGISTRATION_OBJECT( {0} );\n".format(cls.name)
		for func in cls.functions:
			if func.is_abstract: registration = ""
		if not cls.is_serialized:
			registration = ""
		if cls.is_abstract: registration = ""
		out[FLAG_CPP] += fstr.format( cls.name, functions[FLAG_CPP], constructor, self._getNamespace(cls), includes, objects[FLAG_CPP], registration, destructor )
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
	def _createDestructorFunctionHpp(self, cls, tabs):
		if cls.type == "enum":
			return ""
		fstr = "{1}virtual ~{0}()"
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
				str1 = "\nstatic {0} {1}_key = 0;".format(obj.type, obj.name)
				str2 = "\n{0} = ++{0}_key;".format(obj.name)
				initialize2 += str1 + str2
			elif obj.initial_value != None and not obj.is_static and (obj.side == self.parser.side or obj.side=='both'):
				fstr = "\n{2} {0}({1})"
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

	def _createDestructorFunctionCpp(self, cls, tabs):
		if cls.type == "enum":
			return ""
		fstr = "{0}::~{0}()\n__begin__\n__end__\n"
		str = fstr.format( cls.name )
		str = re.sub("__begin__", "{", str)
		str = re.sub("__end__", "}", str)
		return str
		
	def writeFunction(self, function, tabs, flags):
		out = {}
		if function.side != 'both' and function.side != self.parser.side:
			return out
		if flags & FLAG_HPP:
			if not self._currentClass.is_abstract and not function.is_abstract:
				fstr = "{3}{6}{0} {1}({2}){4}{5};\n"
			else:
				fstr = "{3}{6}{0} {1}({2}){4}{5} = 0;\n"
			args = []
			for arg in function.args:
				args.append(convertArgumentType(convertType(arg[1])) + " " + arg[0])
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
				fline = "{0}"
				line = "\n" + self.tabs(tabs+1) + fline.format(operation);
				body += line
			args = []
			for arg in function.args:
				args.append(convertArgumentType(convertType(arg[1])) + " " + arg[0])
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
			if len(dict) > 0:
				filename = cls.name + ".h"
				if cls.group:
					filename = cls.group + "/" + filename
				self.save( filename, dict[FLAG_HPP] )
				out = self._add( out, dict )
		for cls in classes: 
			if not cls.is_abstract:
				dict = self.writeClass(cls, tabs, FLAG_CPP)
				if len(dict) > 0:
					filename = cls.name + ".cpp"
					if cls.group:
						filename = cls.group + "/" + filename
					self.save( filename, dict[FLAG_CPP] )
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

	def getSerializationObjectArg(self, serialization_type):
		pass

	def getBehaviorCallFormat(self):
		pass

	def addSerialization(self, cls, serialization_type):
		function = Function()
		if serialization_type == SERIALIZATION:
			function.is_const = True
			function.name = "serialize"
			function.args.append(self.getSerializationObjectArg(serialization_type))
		if serialization_type == DESERIALIZATION:
			function.name = "deserialize"
			function.args.append(self.getSerializationObjectArg(serialization_type))
		function.return_type = "void"

		for behabior in cls.behaviors:
			if not behabior.is_serialized or behabior.is_abstract:
				continue
			str = self.getBehaviorCallFormat().format( behabior.name, function.name )
			function.operations.append(str)

		for obj in cls.members:
			if obj.is_runtime or obj.is_static or obj.is_const:
				continue
			str = self._buildSerializeObjectOperation(obj, serialization_type)
			function.operations.append(str)
		cls.functions.append(function)

	def _buildSerializeObjectOperation(self, obj, serialization_type):
		type = obj.name if isinstance(obj, Class) else obj.type
		return self._buildSerializeOperation(obj.name, type, obj.initial_value, obj.is_pointer, obj.template_args, serialization_type)

	def _buildSerializeOperationEnum(self, obj_name, obj_type, obj_value, obj_is_pointer, obj_template_args, serialization_type):
		pass
	def _buildSerializeOperation(self, obj_name, obj_type, obj_value, obj_is_pointer, obj_template_args, serialization_type):
		index = 0 
		if obj_value == None:
			index = 1
			
		type = obj_type
		if self.parser._findClass(type) and self.parser._findClass(type).type == 'enum':
			str = self._buildSerializeOperationEnum(obj_name, obj_type, obj_value, obj_is_pointer, obj_template_args, serialization_type)
		else:
			if obj_type not in self.simple_types and type != "list" and type != "map":
				if obj_is_pointer:
					type = "pointer"
				else:
					type = "serialized"
			template_args = []
			if len(obj_template_args) > 0:
				if type == "map":
					if len(obj_template_args) != 2:
						print "map should have 2 arguments"
						exit -1
					if serialization_type == SERIALIZATION:
						return self.buildMapSerialization(obj_name, obj_type, obj_value, obj_is_pointer, obj_template_args)
					if serialization_type == DESERIALIZATION:
						return  self.buildMapDeserialization(obj_name, obj_type, obj_value, obj_is_pointer, obj_template_args)
				else:
					arg = obj_template_args[0]
					arg_type = arg.name if isinstance(arg, Class) else arg.type
					template_args.append(convertType(arg_type))
					if arg_type in self.simple_types:
						type = "{0}<simple>".format( type )
					elif arg.is_pointer:
						type = "pointer_list"
					else:
						type = "{0}<serialized>".format( type )

			fstr = self.serialize_formats[serialization_type][type][index]
			str = fstr.format(obj_name, convertType(obj_type), obj_value, "{", "}", *template_args)
		return str
	
	def buildMapSerialization(self, obj_name, obj_type, obj_value, obj_is_pointer, obj_template_args):
		pass
	
	def buildMapDeserialization(self, obj_name, obj_type, obj_value, obj_is_pointer, obj_template_args):	
		pass

	def addAccept(self, cls):
		visitor = self.parser.getVisitorType(cls)
		if visitor == cls.name:
			return
		function = Function()
		function.name = "accept"
		function.return_type = "void"
		function.args.append(["visitor", visitor + "*"])
		function.operations.append("visitor->visit( this );")
		cls.functions.append(function)

	def addEquals(self, cls):
		function = Function()
		function.name = "operator =="
		function.return_type = "bool"
		function.args.append(["rhs", "const " + cls.name + "&"])
		function.is_const = True
		fbody_line = "result = result && {0} == rhs.{0};"
		function.operations.append( "bool result = true;");
		for m in cls.members:
			if m.is_static or m.is_const:
				continue
			function.operations.append( fbody_line.format(m.name) )
		function.operations.append( "return result;");
		cls.functions.append(function)

		function = Function()
		function.name = "operator !="
		function.return_type = "bool"
		function.args.append(["rhs", "const " + cls.name + "&"])
		function.is_const = True
		function.operations.append( "return !(*this == rhs);" )
		cls.functions.append(function)
		
	def addTests(self, cls):
		function = Function()
		function.name = TEST_FUNCTION_CREATE
		function.return_type = cls.name
		function.is_static = True

		fbody_line = "instance.{0} = {1};"
		function.operations.append( "{0} instance;".format(cls.name) );
		for m in cls.members:
			value = self._getTestValue(m)
			if value == None:
				continue
			if m.is_const or m.is_static:
				continue
			str = fbody_line.format(m.name, value)
			function.operations.append( str )
		function.operations.append( "return instance;");

		cls.functions.append(function)

	def _getTestValue(self, m):
		value = ""
		if m.is_runtime:
			return None
		if m.type == "list" or m.type == "map" or m.type == "set":
			return None
		if m.type == "int" or m.type == "float":
			value = str(random_int())
		if m.type == "bool":
			value = str(random_bool())
		if m.type == "cc.point":
			value = "cocos2d::Point({0},{1})".format(random_float(), random_float())
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
			if t.is_pointer:
				types["IntrusivePtr"] = 1
			for arg in t.template_args:
				type = arg.name if isinstance(arg, Class) else arg.type
				if arg.is_pointer:
					if flags == FLAG_CPP:
						types[type] = 1
					if flags == FLAG_HPP:
						types[type] = 1
					type = "IntrusivePtr"
				types[type] = 1

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
			if t == self._currentClass.name: continue
			if need_include(t):
				out += fstr.format( self.getIncludeFile(t) )
		
		for t in ftypes:
			if t == self._currentClass.name:
				continue
			type = convertType(t)
			if type.find( "::" ) == -1:
				forward_declarations += "\nclass {0};".format( type )
			else:
				continue
				ns = type[0:type.find( "::" )]
				type = type[type.find( "::" )+2:]
				str = "\nnamespace {1}\n__begin__\nclass {0};\n__end__".format( type, ns );
				forward_declarations += str

		if flags == FLAG_CPP:
			out += '\n#include "Factory.h"'
			out += '\n#include <algorithm>'
		
		out = out.split("\n")
		out.sort()
		out = "\n".join( out )
		
		forward_declarations = forward_declarations.split("\n")
		forward_declarations.sort()
		forward_declarations = "\n".join( forward_declarations )

		return out, forward_declarations

	def _findIncludesInFunctionOperation(self, cls, current_includes):
		includes = current_includes
		for function in cls.functions:
			for operation in function.operations:
				if operation == None:
					continue
				if 'throw Exception' in operation: includes += '\n#include "Exception.h"'
				if 'std::sqrt' in operation: includes += '\n#include <cmath>'
				for type in self.parser.classes:
					if (type.name) in operation:
						a = '"{}.h"'.format(type.name)
						b = '/{}.h"'.format(type.name)
						if a not in includes and b not in includes:
							includes += '\n#include {0}'.format(self.getIncludeFile(type.name))
		return includes

	def _createTests(self):
		fstr = "#include \"TestSerialization.h\"\n{0}\n\nvoid TestSerialization::build()\n__begin__\n{1}\n__end__\n"
		includes = ""
		tests = ""
		for cls in self.tests:
			finc = "#include \"../../../out/{}.cpp\"\n".format(cls.name)
			ftst = "_tests.push_back( new TestT<mg::{}> );\n".format(cls.name)
			includes += finc
			if self.createTests:
				tests += ftst
		fstr = fstr.format( includes, tests )
		fstr = re.sub("__begin__", "{", fstr)
		fstr = re.sub("__end__", "}", fstr)
		fileutils.write("tests/cpp/TestCpp/TestSerialization.cpp", fstr)

	def prepareFile(self, body):
		tabs = 0
		lines = body.split('\n')
		body = []
		ch = ''
		for line in lines:
			line = line.strip()

			if line and line[0] == "}":
				tabs-=1
			if "public:" in line:
				tabs -= 1
			line = self.tabs(tabs) + line
			if "public:" in line:
				tabs += 1
			if line.strip() and line.strip()[0] == "{":
				tabs+=1
			body.append(line)
		body = ('\n').join(body)
		return body

	def getIncludeFile(self, file):
		types = {}
		types["cc.point"] = "\"cocos2d.h\""
		types["list"] = "<vector>"
		types["map"] = "<map>"
		types["set"] = "<set>"
		types["string"] = "<string>"
		types["IntrusivePtr"] = '"IntrusivePtr.h"'
		types["pugi::xml_node"] = '"pugixml/pugixml.hpp"'
		types["Json::Value"] = '"jsoncpp/json.h"'
		types["pugi::xml_node"] = '"pugixml/pugixml.hpp"'
		types["Observer"] = '"Observer.h"'
		if file in types:
			return types[file]
		if 'std::map' in file:
			return '<map>'

		cls = self.parser._findClass(file)
		if cls and cls.name == file and self._currentClass.group != cls.group:
			back = ""
			backs = len(self._currentClass.group.split("/")) if self._currentClass.group else 0
			for i in range(backs):
				back += "../"
			f = '"{2}{1}/{0}.h"' if cls.group else '"{2}{0}.h"'
			return f.format(cls.name, cls.group, back)
		return '"{0}.h"'.format(file)

