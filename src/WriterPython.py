import re
from Writer import Writer
from Function import Function
from Class import Class
from Object import Object
import fileutils


SERIALIZATION = 0
DESERIALIZATION = 1

def convertInitializeValue(value):
	if value == 'true': return 'True'
	if value == 'false': return 'False'
	return value

class WriterPython(Writer):
	def __init__(self, outDirectory, parser, generateTests, configsDirectory):
		
		self.loaded_functions = {}
		self.load_functions(configsDirectory + 'python_external.mlc_py')

		self.create_serialization_patterns()
		self.current_class = None

		Writer.__init__(self, outDirectory, parser)

		self.createFactory()
		self.createRequestHandler()

	def create_serialization_patterns(self):
		pass

	def writeObject(self, object, tabs, flags):
		out = ""
		return {flags:out}

	def getPatternFile(self):
		pass
	
	def writeClass(self, cls, tabs, flags):
		out = ""
		pattern = self.getPatternFile()
		self.current_class = cls

		if cls.type == 'enum':
			for member in cls.members:
				if member.initial_value != None and member.name == '_value':
					member.initial_value = 'self.' + member.initial_value


		initialize_list = ''
		for object in cls.members:
			initialize_list += '\t\t' + self.writeObject(object) + '\n'

		self.createSerializationFunction(cls,SERIALIZATION)
		self.createSerializationFunction(cls,DESERIALIZATION)
		functions = ''
		for function in cls.functions:
			f = self.writeFunction(cls, function)
			functions += f

		imports = ''
		init_behavior = ''
		name = cls.name
		if cls.behaviors:
			name += '(' + cls.behaviors[0].name + ')'
			imports += 'from {0} import {0}'.format(cls.behaviors[0].name)
			init_behavior = '\t\t{0}.__init__(self)'.format(cls.behaviors[0].name)
		for obj in cls.members:
			if self.parser._findClass(obj.type):
				imports += '\nfrom {0} import {0}'.format(obj.type)
			elif obj.type == 'list' or obj.type == 'map':
				for arg in obj.template_args:
					if isinstance(arg, Class):
						imports += '\nfrom {0} import {0}'.format(arg.name)

		out = pattern.format(name, initialize_list, functions, imports, init_behavior)
		self.current_class = None
		return {flags:out}
	
	def writeFunction(self, cls, function):
		out = ""
		key = cls.name + '.' + function.name
		if key in self.loaded_functions:
			body = self.loaded_functions[key]
			out += '\tdef {0}{1}\n\n'.format(function.name, body)
		return out

	def writeObject(self, object):
		value = object.initial_value
		if value == None:
			type = object.type
			if type == "string": value = '""'
			if type == "int": value = "0"
			if type == "float": value = "0.f"
			if type == "uint": value = "0"
			if type == "bool": value = "False"
			if type == "list": value = "[]"
			if type == "map": value = "{}"
		
		out = 'self.{0} = {1}'.format(object.name, convertInitializeValue(value))
		return out

	def _getImports(self, cls):
		return ""

	def _getFilenameForClass(self, cls):
		return cls.name + ".py"

	def load_functions(self, path):
		buffer = open(path).read()
		functions = buffer.split('function:')
		for func in functions:
			k = func.find('(')
			if k == -1:
				continue
			name = func[0:k]
			rawbody = func[k:].split('\n')
			body = [rawbody[0]]
			for line in rawbody[1:]:
				if line:
					body.append('\t' + line)
			body = '\n'.join(body)
			self.loaded_functions[name] =  body

	def getSerialiationFunctionArgs(self):
		pass
	def createSerializationFunction(self, cls, serialize_type):
		function = Function()
		function.name = 'serialize' if serialize_type == SERIALIZATION else 'deserialize'
		for func in cls.functions:
			if func.name == function.name:
				return

		body = self.getSerialiationFunctionArgs() + ':\n'
		if cls.behaviors:
			body += ('\t\t{0}.{1}' + self.getSerialiationFunctionArgs() + '\n').format(cls.behaviors[0].name, function.name)
		for obj in cls.members:
			if obj.is_runtime:continue
			if obj.is_static:continue
			if obj.is_const:continue

			body += self._buildSerializeOperation(obj.name, obj.type, convertInitializeValue(obj.initial_value), serialize_type, obj.template_args, obj.is_pointer)
		body += '\t\treturn'
		self.loaded_functions[cls.name + '.' + function.name] = body
		cls.functions.append(function)
	
	def getPatternSerializationMap(self):
		pass

	def getPatternDeserializationMap(self):
		pass

	def buildMapSerialization(self, obj_name, obj_type, obj_value, obj_is_pointer, obj_template_args):
		key = obj_template_args[0]
		value = obj_template_args[1]
		key_type = key.name if isinstance(key, Class) else key.type
		value_type = value.name if isinstance(value, Class) else value.type
		str = self.getPatternSerializationMap()
		_value_is_pointer = value.is_pointer
		a0 = obj_name
		a1 = self._buildSerializeOperation('key', key_type, None, SERIALIZATION, [], False, '')
		a2 = self._buildSerializeOperation("value", value_type, None, SERIALIZATION, [], _value_is_pointer, '')
		a1 = a1.split('\n')
		for index, a in enumerate(a1):
			a1[index] = '\t' + a
		a1 = '\n'.join(a1)
		a2 = a2.split('\n')
		for index, a in enumerate(a2):
			a2[index] = '\t' + a
		a2 = '\n'.join(a2)
		return str.format( a0, a1, a2, '{}')
		#a1 = serialize key /simple, serialized
		#a2 = serialize value /simple, serialized, pointer,
	
	def buildMapDeserialization(self, obj_name, obj_type, obj_value, obj_is_pointer, obj_template_args):	
		key = obj_template_args[0]
		value = obj_template_args[1]
		key_type = key.name if isinstance(key, Class) else key.type
		value_type = value.name if isinstance(value, Class) else value.type
		str = self.getPatternDeserializationMap()
		_value_is_pointer = value.is_pointer
		a0 = obj_name
		a1 = self._buildSerializeOperation('key', key_type, None, DESERIALIZATION, [], False, '')
		a2 = self._buildSerializeOperation("value", value_type, None, DESERIALIZATION, [], _value_is_pointer, '_')
		a1 = a1.split('\n')
		for index, a in enumerate(a1):
			a1[index] = '\t' + a
		a1 = '\n'.join(a1)
		a2 = a2.split('\n')
		for index, a in enumerate(a2):
			a2[index] = '\t' + a
		a2 = '\n'.join(a2)
		return str.format( a0, a1, a2, '{}')

	def _buildSerializeOperation(self, obj_name, obj_type, obj_value, serialization_type, obj_template_args, obj_is_pointer, owner = 'self.'):
		index = 0 
		if obj_value == None:
			index = 1
		

		type = obj_type
		if self.parser._findClass(type) and self.parser._findClass(type).type == 'enum':
			type = 'simple'
		elif obj_type not in self.simple_types and type != "list" and type != "map":
			if obj_is_pointer:
				type = "pointer"
			else:
				type = "serialized"
		elif obj_type in self.simple_types:
			type = 'simple'
		else:
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
					if arg_type in self.simple_types:
						type = "list<simple>"
						obj_type = arg_type
					elif arg.is_pointer:
						type = "pointer_list"
					else:
						type = "list<serialized>"
						obj_type = arg_type

		fstr = self.serialize_formats[serialization_type][type][index]
		str = fstr.format(obj_name, obj_type, obj_value, '{}', owner, obj_template_args[0].type if len(obj_template_args) > 0 else 'unknown_arg')
		return '\t\t' + str + '\n'

	def getPatternFactoryFile(self):
		pass
	def createFactory(self):
		pattern = self.getPatternFactoryFile()
		line = '\t\tif type == "{0}": return {0}.{0}()\n'
		line_import = 'import {0}\n'
		creates = ''
		imports = ''
		for cls in self.parser.classes:
			creates += line.format(cls.name)
			imports += line_import.format(cls.name)
		factory = pattern.format(imports, creates)
		file = self.out_directory + 'Factory.py'
		if fileutils.isFileChanges(file):
			fileutils.write(file, factory)
		self.created_files.append(file)

	def createRequestHandler(self):
		pattern = '''
{0}

class IRequestHandler:
	def __init__(self):
		self.response = None

	def visit(self, ctx):
		if ctx == None: return
{1}		

{2}	
'''
		line = '\t\telif ctx.__class__ == {0}: self.visit_{1}(ctx)\n'
		line_import = 'from {0} import {0}\n'
		line_visit = '''
	def visit_{0}(self, ctx):
		return
'''
		lines = ''
		visits = ''
		imports = ''
		for cls in self.parser.classes:
			if self.parser.isVisitor(cls):
				func_name = cls.name
				func_name = func_name[0].lower() + func_name[1:]

				lines += line.format(cls.name, func_name)
				imports += line_import.format(cls.name)
				visits += line_visit.format(func_name)
		factory = pattern.format(imports, lines, visits)
		file = self.out_directory + 'IRequestHandler.py'
		if fileutils.isFileChanges(file):
			fileutils.write(file, factory)
		self.created_files.append(file)

