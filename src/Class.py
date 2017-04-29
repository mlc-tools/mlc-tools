import re
from Object import Object
from Function import Function
import constants

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
		self.type = 'class'
		self.group = ''
		self.side = 'both'

	def parse(self, line):
		line = line.strip()
		if self.type in line:
			line = line[len(self.type):]
		line = self.find_modifiers(line)
		type_ = self.type
		self.type = ''
		Object.parse(self, line)
		self.name = self.type
		self.type = type_
		self.behaviors = self.template_args
		self.template_args = []
		if '/' in self.name:
			k = self.name.rindex('/')
			self.group = self.name[0:k]
			self.name = self.name[k + 1:]

	def parse_body(self, parser, body):
		parser.parse(body)
		if len(parser.classes) > 0:
			print 'Not supported inbody classes'
		self.members = parser.objects
		self.functions = parser.functions
		if self.type == 'enum':
			self._convert_to_enum()
		return

	def on_linked(self):
		if self.generate_set_function:
			self._generate_setters_function()
			self._generate_getters_function()

	def find_modifiers(self, string):
		self.is_abstract = self.is_abstract or ':abstract' in string
		self.is_serialized = self.is_serialized or ':serialized' in string
		self.is_visitor = self.is_visitor or ':visitor' in string
		self.generate_set_function = self.generate_set_function or ':set_function' in string
		if ':server' in string:
			self.side = 'server'
		if ':client' in string:
			self.side = 'client'

		string = re.sub(':abstract', '', string)
		string = re.sub(':serialized', '', string)
		string = re.sub(':visitor', '', string)
		string = re.sub(':set_function', '', string)
		string = re.sub(':server', '', string)
		string = re.sub(':client', '', string)
		return string

	def _generate_setters_function(self):
		function = Function()
		function.name = constants.CLASS_FUNCTION_SET_PROPERTY
		function.return_type = 'void'
		function.args.append(['name', 'string'])
		function.args.append(['value', 'string'])

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
			supported_types = {'string': 'std::string', 'int': 0, 'float': 0, 'bool': 0}
			if member.type in supported_types:
				type_ = member.type
				type_ = type_ if supported_types[type_] == 0 else supported_types[type_]
				op = 'if(name == "{0}") \n{2}\n{0} = strTo<{1}>(value);\n{3}'
				if i > 0:
					op = 'else ' + op
				function.operations.append(op.format(member.name, type_, '{', '}'))
				add_function = True

		override = False
		if self.behaviors:
			for class_ in self.behaviors:
				if class_.is_abstract:
					continue
				for func in class_.functions:
					equal = func.name == function.name and func.return_type == function.return_type
					for i, arg in enumerate(func.args):
						equal = equal and func.args[i][1] == function.args[i][1]
					if equal:
						override = True
						if len(function.operations):
							op = 'else \n{1}\n{0}::{3}(name, value);\n{2}'
						else:
							op = '{0}::{3}(name, value);'
						function.operations.append(op.format(class_.name, '{', '}', constants.CLASS_FUNCTION_SET_PROPERTY))
						break

		if add_function or not override:
			self.functions.append(function)

	def _generate_getters_function(self):
		function = Function()
		function.name = constants.CLASS_FUNCTION_GET_PROPERTY
		function.return_type = 'string'
		function.args.append(['name', 'string'])

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
			supported_types = ['string', 'int', 'float', 'bool']
			if member.type in supported_types:
				type_ = member.type
				getter = 'if(name == "{0}")\n{2}\nreturn toStr({0});\n{3}'
				if i > 0:
					getter = 'else ' + getter
				function.operations.append(getter.format(member.name, type_, '{', '}'))
				add_function = True

		parent_class = ''
		if self.behaviors:
			for class_ in self.behaviors:
				if class_.is_abstract:
					continue
				for func in class_.functions:
					equal = func.name == function.name and func.return_type == function.return_type
					for i, arg in enumerate(func.args):
						equal = equal and func.args[i][1] == function.args[i][1]
					if equal:
						parent_class = class_.name
						break

		op = ''
		if not parent_class:
			op = 'return "";'
		elif function.operations:
			op = 'else \n{1}\n return {0}::{3}(name);\n{2}'.format(parent_class, '{', '}', constants.CLASS_FUNCTION_GET_PROPERTY)
		else:
			op = 'return {0}::{1}(name, value);'.format(parent_class, constants.CLASS_FUNCTION_GET_PROPERTY)
		function.operations.append(op)

		if add_function or not parent_class:
			self.functions.append(function)

	def _convert_to_enum(self):
		shift = 0
		if len(self.behaviors) == 0:
			self.behaviors.append('int')
		cast = self.behaviors[0]
		values = []
		for m in self.members:
			m.name = m.type
			m.type = cast
			m.is_static = True
			m.is_const = True
			if m.initial_value is None:
				if cast == 'int':
					m.initial_value = '(1 << {})'.format(shift)
					values.append(1 << shift)
				else:
					print 'Enum with cast to not "int" not supported now. Please contact me'
					exit(-1)
			shift += 1
		self.behaviors = []

		def add_function(type_, name, args, const):
			function = Function()
			function.return_type = type_
			function.name = name
			function.args = args
			function.is_const = const
			self.functions.append(function)
			return function

		add_function(
			'',
			self.name,
			[],
			False).\
			operations = ['_value = {};'.format(self.members[0].name)]
		add_function(
			'',
			self.name,
			[['value', cast]],
			False).\
			operations = ['_value = value;']
		add_function(
			'',
			self.name,
			[['rhs', 'const {0}&'.format(self.name)]],
			False).\
			operations = ['_value = rhs._value;']
		add_function(
			'',
			'operator int',
			[],
			True).\
			operations = ['return _value;']
		add_function(
			'const {0}&'.format(self.name),
			'operator =',
			[['rhs', 'const {0}&'.format(self.name)]],
			False).\
			operations = ['_value = rhs._value;', 'return *this;']
		add_function(
			'bool',
			'operator ==',
			[['rhs', 'const {0}&'.format(self.name)]],
			True).\
			operations = ['return _value == rhs._value;']
		add_function(
			'bool',
			'operator ==',
			[['rhs', 'int']],
			True).\
			operations = ['return _value == rhs;']
		add_function('bool', 'operator <', [['rhs', 'const {0}&'.format(self.name)]], True).\
			operations = ['return _value < rhs._value;']

		function1 = add_function('', self.name, [['value', 'string']], False)
		function2 = add_function('const {0}&'.format(self.name), 'operator =', [['value', 'string']], False)
		function3 = add_function('', 'operator std::string', [], True)
		function4 = add_function('string', 'str', [], True)
		index = 0
		for m in self.members:
			function1.operations.append('if(value == "{0}") {1}_value = {0}; return; {2};'.format(m.name, '{', '}'))
			function1.operations.append('if(value == "{0}") {1}_value = {0}; return; {2};'.format(values[index], '{', '}'))
			function2.operations.append('if(value == "{0}") {1}_value = {0}; return *this; {2};'.format(m.name, '{', '}'))
			function2.operations.append('if(value == "{0}") {1}_value = {0}; return *this; {2};'.format(values[index], '{', '}'))
			function3.operations.append('if(_value == {0}) return "{0}";'.format(m.name))
			function4.operations.append('if(_value == {0}) return "{0}";'.format(m.name))
			index += 1
		function1.operations.append('_value = 0;')
		function2.operations.append('return *this;')
		function3.operations.append('return "";')
		function4.operations.append('return "";')

		value = Object()
		value.initial_value = self.members[0].name
		value.name = '_value'
		value.type = cast
		self.members.append(value)

	def add_get_type_function(self):
		if not self.is_abstract:
			member = Object()
			member.is_static = True
			member.is_const = True
			member.type = 'string'
			member.name = '__type__'
			member.initial_value = '"{}"'.format(self.name)
			self.members.append(member)

		function = Function()
		function.name = constants.CLASS_FUNCTION_GET_TYPE
		function.return_type = 'string'
		function.is_const = True
		function.operations.append('return {}::__type__;'.format(self.name))
		self.functions.append(function)
