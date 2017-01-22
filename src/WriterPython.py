import re
from Writer import Writer
from Function import Function

SERIALIZATION = 0
DESERIALIZATION = 1

class WriterPython(Writer):
	def __init__(self, outDirectory, parser, generateTests, configsDirectory):
		self.loaded_functions = {}
		self.load_functions(configsDirectory + 'python_external.mlc_py')

		self.simple_types = ["int", "float", "bool", "string", "cc.point"]

		self.serialize_formats = []
		self.serialize_formats.append({})
		self.serialize_formats.append({})
		
		self.serialize_formats[SERIALIZATION]['simple'] = []
		self.serialize_formats[SERIALIZATION]['simple'].append( 'if self.{0} != {2}: dictionary["{0}"] = self.{0}' )
		self.serialize_formats[SERIALIZATION]['simple'].append( 'dictionary["{0}"] = self.{0}' )
		self.serialize_formats[DESERIALIZATION]['simple'] = []
		self.serialize_formats[DESERIALIZATION]['simple'].append( 'if "{0}" in dictionary: self.{0} = dictionary["{0}"]' )
		self.serialize_formats[DESERIALIZATION]['simple'].append( 'self.{0} = dictionary["{0}"]' )

		Writer.__init__(self, outDirectory, parser)

	def writeObject(self, object, tabs, flags):
		out = ""
		return {flags:out}
	
	def writeClass(self, cls, tabs, flags):
		out = ""
		pattern = '''import json
{3}

class {0}:
	def __init__(self):
{4}
{1}
		return

	def get_type(self):
		return self.__type__

{2}	
'''
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

		out = pattern.format(name, initialize_list, functions, imports, init_behavior)
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
			if type == "bool": value = "false"
			if type == "list": value = "[]"
			if type == "map": value = "{}"
		
		out = 'self.{0} = {1}'.format(object.name, value)
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

	def createSerializationFunction(self, cls, serialize_type):
		function = Function()
		function.name = 'serialize' if serialize_type == SERIALIZATION else 'deserialize'
		body = '(self, dictionary):\n'
		if cls.behaviors:
			body += '\t\t{0}.{1}(self, dictionary)\n'.format(cls.behaviors[0].name, function.name)
		for obj in cls.members:
			if obj.is_runtime:continue
			if obj.is_static:continue
			if obj.is_const:continue

			body += self._buildSerializeOperation(obj.name, obj.type, obj.initial_value, serialize_type)
		body += '\t\treturn'
		self.loaded_functions[cls.name + '.' + function.name] = body
		cls.functions.append(function)
	
	def _buildSerializeOperation(self, obj_name, obj_type, obj_value, serialization_type):
		index = 0 
		if obj_value == None:
			index = 1
			
		type = obj_type
		if obj_type not in self.simple_types and type != "list" and type != "map":
			type = "serialized"
		elif obj_type in self.simple_types:
			type = 'simple'
		else:
			print 'not supported type', type
			return ''
		fstr = self.serialize_formats[serialization_type][type][index]
		str = fstr.format(obj_name, obj_type, obj_value)
		return '\t\t' + str + '\n'
