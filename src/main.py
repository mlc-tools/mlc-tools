from arguments_parser import get_arg
import fileutils
import os, sys

_includes = {"void":"","int":"","uint":"","uint32_t":"","int32_t":"","bool":"","float":"","list":"<vector>","cc.point":"\"cocos2d.h\"","cocos2d::Point":"\"cocos2d.h\"","cc.sprite":"\"cocos2d.h\"", "string":"<string>","UnitLayer":"\"UnitLayer.h\"","SerializedObject":"\"online/SerializedObject.h\"","NodeExt":"\"ml/NodeExt.h\"","CommandBase":"\"online/CommandBase.h\"","MoverModel":"\"online/MoverModel.h\"", "xml_node":"\"ml/pugixml/pugixml.hpp\""}
_types={"list":"std::vector","string":"std::string","cc.point":"cocos2d::Point","cc.sprite":"cocos2d::Sprite","int":"int32_t","uint":"uint32_t","ml.nodeext":"cocos2d::NodeExt", "xml_node":"pugi::xml_node"}
template_file = "templates.txt"
__serialized_types = ["CommandBase"]

def addSerializedType(name):
	__serialized_types.append(name)
def isSerialized(name):
	return name in __serialized_types


class Method:
	@staticmethod
	def is_method(line):
		return line[0] == "+" or line[0] == "-"
	def __init__(self,line):
		self.is_static = False
		self.return_type = "void"
		self.name = ""
		self.args = []
		self.body = []
		self.__counter = 0
		
		desc = line
		self.is_static = desc[0] == '+'
		desc = desc[1:]
		self.return_type = desc.split("/")[0]
		desc = desc.split("/")[1]
		self.name = desc.split("(")[0]
		desc = desc.split("(")[1]
		self.is_external = self.name.find(":external") != -1
		if self.is_external:
			self.name = self.name[0:self.name.find(":external")]
		desc = desc[0:-1]
		self.args = desc.split(",")
	def pushBodyLine(self, line):
		if len(line) > 0 and line[0]=='}':
			self.__counter -= 1
			if self.__counter <= 0:
				return False
		if len(line) > 0 and line[0]=='{':
			self.__counter += 1
			if len(self.body) == 0:
				return True
		self.body.append(line)
		return True

class Field:

	def __init__(self, line):
		args = line.split(" ")
		self.type = ""
		self.arguments = []
		self.name = ""
		self.initialize_value = ""
		self.is_runtime = False
		self.is_pointer = False
		self.parents = []
		self.fields = []
		self.methods = []

		if len(line) == 0:
			return

		self.type = args[0]
		self.name = args[1]
		if len(self.name.split("=")) == 2:
			self.initialize_value = self.name.split("=")[1]
			self.name = self.name.split("=")[0]

		if len(args) > 3 and args[2] == "parent":
			self.parents = args[3].split(",")

		if self.type.find(":runtime") != -1:
			self.type = self.type[0:self.type.find(":runtime")]
			self.is_runtime = True
		if self.type.find("*") != -1:
			self.type = self.type[0:self.type.find("*")]
			self.is_pointer = True
		if self.type.find("<") < self.type.find(">"):
			args_str = self.type[self.type.find("<")+1:self.type.find(">")]
			self.type = self.type[0:self.type.find("<")]
			self.arguments = args_str.split(",")
			for i in range(len(self.arguments)):
				self.arguments[i] = self.arguments[i].strip()
				if self.arguments[i] in _types:
					self.arguments[i] = _types[self.arguments[i]]

		if self.type == "class":
			_includes[self.name] = "\"" + self.name + ".h\""
		if 0:
			print ""
			print "\ttype:", self.type, self.arguments
			print "\tname:", self.name
			print "\tparents:", self.parents
			print "\truntime:", self.is_runtime


	def parseField(self, line):
		args = line.split(" ")
		if len(args) < 2:
			return -1
		else:
			self.fields.append(Field(line))

	def getFinalType(self):
		type = self.type
		if type in _types:
			type = _types[type]
		if len(self.arguments) > 0:
			type += "<" + ", ".join(self.arguments) + ">"
		if self.is_pointer:
			type += "*"
		return type

	def is_serializable(self):
		return isSerialized(self.type)

def readDeclarationBody(declaration_file):
	classInfo = None
	read_method_body = False
	for rawline in declaration_file:
		line = rawline.strip()
		if( line == "" and classInfo == None):
			continue
		if( line == "" and classInfo != None):
			break
		if classInfo == None:
			classInfo = Field(line)
			continue
		if classInfo != None:
			if read_method_body:
				read_method_body = classInfo.methods[-1].pushBodyLine(rawline[0:-1])
			if read_method_body == False:
				if Method.is_method(line):
					classInfo.methods.append(Method(line))
					read_method_body = not classInfo.methods[-1].is_external
				else:
					classInfo.parseField(line)
	return classInfo

def buildIncludes(fields):
	result = []
	for field in fields:
		if field == "":
			continue
		if field in _includes:
			if _includes[field] != "":
				result.append(_includes[field])
		else:
			print "Error: unknow type", field
			exit(-1)
	return result

def readTemplate( name ):
	result = ""
	file = open( template_file, "r")
	inbody = False
	for line in file:
		if line.find( "===== "+name+" begin =====" ) == 0:
			inbody = True
			continue
		if line.find( "===== "+name+" end =====" ) == 0:
			inbody = False
			break
		if inbody == True:
			result += line
	if inbody == False:
		return result
	exit(-1)


def replace_all(src, frm, to):
	l = 0
	while l < len(src):
		r = src.find(frm,l)
		if r == -1:
			break
		src = src[0:r] + to + src[r+len(frm):]
		l = r + len(to)
	return src

def incrementalWriteToFile( buffer, fileName ):
	content = ""
	try:
		content = open(fileName,"r").read()
	except IOError:
		content = ""
	if content != buffer:
		print "create file:", fileName
		open(fileName,"w").write(buffer)
	#print buffer

def getFieldSerializeLine(fieldinfo, opp):
	simple_serialization_pattern = readTemplate("simple_" + opp)
	serialized_serialization_pattern = readTemplate("serialized_" + opp)
	if fieldinfo.is_serializable() == False:
		result = simple_serialization_pattern
	else:
		result = serialized_serialization_pattern
	result = replace_all(result, "type", fieldinfo.getFinalType())
	result = replace_all(result, "name", fieldinfo.name)
	return result

def getFieldSerializeLineArray(type, name, is_serialized, opp):
	simple_serialization_pattern = readTemplate("simple_item_" + opp)
	serialized_serialization_pattern = readTemplate("serialized_item_" + opp)
	if is_serialized == False:
		result = simple_serialization_pattern
	else:
		result = serialized_serialization_pattern
	result = replace_all(result, "type", type)
	result = replace_all(result, "name", name)
	return result

def getFieldSerializeList(fieldinfo, opp):
	if len(fieldinfo.arguments) != 1:
		print "not supported serialization type:", fieldinfo.getFinalType()
	is_serialized = isSerialized(fieldinfo.arguments[0])
	list_serialization_pattern = readTemplate("list_" + opp)
	line = getFieldSerializeLineArray(fieldinfo.arguments[0], fieldinfo.name, is_serialized, opp)
	result = list_serialization_pattern
	result = replace_all(result, "name", fieldinfo.name)
	result = replace_all(result, "__serialize_line__", line)
	return result

def generateFile(classinfo, template):
	header_pattern = readTemplate(template)
	#C++ header
	field_pattern = readTemplate("field")
	method_declaration_pattern = readTemplate("method_declaration")
	method_defination_pattern = readTemplate("method_defination")
	method_body_line_pattern = readTemplate("method_body_line")
	include_pattern = readTemplate("include")
	fdeclaration_pattern = readTemplate("forward declaration")
	parent_declaration = readTemplate("parent class")
	parent_next_declaration = readTemplate("parent class next")
	initialization_pattern = readTemplate("initialization")
	#C++ source
	
	parent_serialization_pattern = readTemplate("parent_serialization")
	parent_deserialization_pattern = readTemplate("parent_deserialization")
	accept_header = readTemplate("commanddelegate accept header")
	accept_source = readTemplate("commanddelegate accept source")

	includes = ""
	fields = []
	current_includes = []
	for parent in classinfo.parents:
		fields.append( parent )
	for arg in classinfo.arguments:
		fields.append( arg )
	for field in classinfo.fields:
		fields.append( field.type )
		for arg in field.arguments:
			fields.append( arg )
	for method in classinfo.methods:
		fields.append( method.return_type )
		for arg in method.args:
			fields.append( arg.split(" ")[0].split("*")[0].split("&")[0] )
	for file in buildIncludes(fields):
		if file in current_includes:
			continue
		current_includes.append(file)
		includes += replace_all(include_pattern, "file", file)

	#serialization
	fields = ""
	initializations = ""
	serialization = ""
	deserialization = ""
	for fieldinfo in classinfo.fields:
		field_str = field_pattern
		field_str = replace_all(field_str, "type", fieldinfo.getFinalType())
		field_str = replace_all(field_str, "name", fieldinfo.name)
		fields += field_str

		if fieldinfo.initialize_value != "":
			init_str = initialization_pattern
			init_str = replace_all(init_str, "name", fieldinfo.name)
			init_str = replace_all(init_str, "value", fieldinfo.initialize_value)
			initializations += init_str

		if fieldinfo.is_runtime:
			continue
		if fieldinfo.type != "list":
			serialization += getFieldSerializeLine(fieldinfo, "serialization")
			deserialization += getFieldSerializeLine(fieldinfo, "deserialization")
		else:
			serialization += getFieldSerializeList(fieldinfo, "serialization")
			deserialization += getFieldSerializeList(fieldinfo, "deserialization")
	
	methods = ""
	methods_def = ""
	for method in classinfo.methods:
		#declaration
		method_str = method_declaration_pattern;
		type = method.return_type
		if type in _types:
			type = _types[type]
		method_str = replace_all(method_str, "type", type)
		method_str = replace_all(method_str, "name", method.name)
		args = []
		for arg in method.args:
			name = ""
			if len(arg.split(" ")) > 1:
				name = arg.split(" ")[1]
				arg = arg.split(" ")[0]
			type = arg
			is_pointer = type.find("*") != -1
			is_ref = type.find("&") != -1
			is_const = type.find("const ") != -1
			if is_pointer: type = replace_all(type, "*", "")
			if is_ref: type = replace_all(type, "&", "")
			if is_const: type = replace_all(type, "const ", "")
			if type in _types:
				type = _types[type]
			if is_pointer: type = type + "*"
			if is_ref: type = type + "&"
			if is_const: type = "const " + type
			args.append( type + " " + name)
		method_str = replace_all(method_str, "args", ",".join(args))
		if method.is_static == False: 
			method_str = replace_all(method_str, "static", "")
		methods += method_str
		
		#defination
		if method.is_external == False:
			method_body = ""
			method_str = method_defination_pattern
			for line in method.body:
				method_body += replace_all(method_body_line_pattern, "line", line)
			type = method.return_type
			if type in _types:
				type = _types[type]
			method_str = replace_all(method_str, "type", type)
			method_str = replace_all(method_str, "name", method.name)
			method_str = replace_all(method_str, "method_body", method_body)

			method_str = replace_all(method_str, "args", ",".join(args))
			methods_def += method_str
	
	if len(classinfo.parents)> 0 and classinfo.parents[0] == "CommandBase":
		accept_header = replace_all(accept_header, "__ClassName__", classinfo.name)
		accept_source = replace_all(accept_source, "__ClassName__", classinfo.name)
	else:
		accept_header = "\n"
		accept_source = "\n"

	fdeclarations = ""
	#TODO: build forward declarations list

	body = header_pattern
	body = replace_all(body, "__namespace__", "mg")
	body = replace_all(body, "__fields_section__", fields)
	body = replace_all(body, "__initialization_section__", initializations)
	body = replace_all(body, "__methods_section__", methods)
	body = replace_all(body, "__methods_defination_section__", methods_def)
	body = replace_all(body, "__includes_section__", includes)
	body = replace_all(body, "__forward_declaration_section__", fdeclarations)
	body = replace_all(body, "__serialize_fields_section__", serialization)
	body = replace_all(body, "__deserialize_fields_section__", deserialization)
	body = replace_all(body, "__commanddelegate_header_accept__", accept_header)
	body = replace_all(body, "__commanddelegate_source_accept__", accept_source)
	body = replace_all(body, "__ClassName__", classinfo.name)

	index = 0
	parents = ""
	for parent_name in classinfo.parents:
		if parent_name in _types:
			parent_name = _types[parent_name]
		if index == 0:
			pattern = parent_declaration
		else:
			pattern = parent_next_declaration
		index += 1
		parents += replace_all(pattern, "parent", parent_name)
	
	if len(classinfo.parents) > 0:
		body = replace_all(body, "__ParentClassName__", classinfo.parents[0])
	body = replace_all(body, "__ParentSection__", parents)

	if isSerialized(classinfo.name):
		index = __serialized_types.index(classinfo.name)
		#TODO: activate this line on production
		#TODO: use arguments
		#type = str(index)
		#body = replace_all(body, "__ClassFactoryName__", type)
		body = replace_all(body, "__ClassFactoryName__", classinfo.name)
	if len(classinfo.parents)> 0 and isSerialized(classinfo.parents[0]):
		body = replace_all(body, "__serialize_parent_section__", replace_all(parent_serialization_pattern, "parent", classinfo.parents[0]))
		body = replace_all(body, "__deserialize_parent_section__", replace_all(parent_deserialization_pattern, "parent", classinfo.parents[0]))
	else:
		body = replace_all(body, "__serialize_parent_section__", "")
		body = replace_all(body, "__deserialize_parent_section__", "")

	common_replaces = readTemplate("common_replaces").strip()
	cmn_v = common_replaces.split(" ")
	if len(cmn_v)>1:
		index = 0
		while index < len(cmn_v)-1:
			body = replace_all(body, cmn_v[index], cmn_v[index+1])
			index += 2

	#print body
	return body

def isCommand(type):
	temp = type
	break_search = False
	while not break_search:
		if temp == "CommandBase":
			return True
		break_search = True
		for classdef in all_classes:
			if classdef.name == temp:
				temp = classdef.parents[0]
				break_search = False
				break

def generateCommandDelegate(classes):
	header_pattern = readTemplate("commanddelegate cpp")
	fdeclaration_pattern = readTemplate("commanddelegate fd")
	method_declaration = readTemplate("commanddelegate method")
	
	fdeclarations = ""
	methods = ""
	for command in classes:
		if not isCommand(command.name):
			continue
		fdeclarations += replace_all(fdeclaration_pattern, "__ClassName__", command.name)
		methods += replace_all(method_declaration, "__ClassName__", command.name)
	
	body = header_pattern
	body = replace_all(body, "__namespace__", "mg")
	body = replace_all(body, "__forward_declarations_section__", fdeclarations)
	body = replace_all(body, "__methods_section__", methods)
	#print body
	return body

def removeUnactualFiles(dir, all_classes):
	files = fileutils.getFilesList(dir)
	for file in files:
		name = file.split(".")[0]
		remove = True
		for class_info in all_classes:
			if class_info.name == name:
				remove = False
				break
		if remove:
			print "remove", file
			fileutils.remove( dir + file )


path_to_generate = get_arg("-dir", "out/")
file_declaration = get_arg("-declaration", "declaration.txt")
template_file = get_arg("-templates", "templates.txt")

try: os.stat(path_to_generate)
except: os.mkdir(path_to_generate)
try: os.stat(file_declaration)
except: print "File with declarations not fount.", file_declaration
try: os.stat(template_file)
except: print "File with template not fount.", template_file

def checkChanges():
	return True
	if fileutils.isFileChanges(file_declaration):
		return True
	if fileutils.isFileChanges(template_file):
		return True
	if fileutils.isFileChanges(sys.argv[0]):
		return True
	return False

def saveChangesCache():
	fileutils.saveMd5ToCache(file_declaration)
	fileutils.saveMd5ToCache(template_file)
	fileutils.saveMd5ToCache(sys.argv[0])

all_classes = []

if checkChanges():
	print "generate..."
	declaration_file = open(file_declaration)
	while True:
		classinfo = readDeclarationBody(declaration_file)
		if classinfo == None:
			break
		all_classes.append(classinfo)
		addSerializedType(classinfo.name)

	declaration_file = open(file_declaration)
	while True:
		classinfo = readDeclarationBody(declaration_file)
		if classinfo == None:
			break
		incrementalWriteToFile( generateFile( classinfo, "header" ), path_to_generate + classinfo.name + ".h" )
		incrementalWriteToFile( generateFile( classinfo, "source" ), path_to_generate + classinfo.name + ".cpp" )
		
		#generateFile( classinfo, "java" )

	incrementalWriteToFile( generateCommandDelegate( all_classes ), path_to_generate + "CommandDelegate.h" )
	saveChangesCache()
		
	delegate = Field("")
	delegate.name = "CommandDelegate"
	all_classes.append(delegate)
	removeUnactualFiles(path_to_generate, all_classes)
else:
	print "havent changes"
