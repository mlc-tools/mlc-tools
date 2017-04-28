from Object import Object
from Class import Class
from Function import Function


def throw_error(msg):
	print msg
	exit(-1)


def is_class(line):
	return line.strip().find('class') == 0


def is_functon(line):
	return line.strip().find('function') == 0


def is_enum(line):
	return line.strip().find('enum') == 0


def find_body(text):
	text = text.strip()
	body = ""
	if text.find("\n") != -1:
		header = text[0:text.find("\n")]
	else:
		header = text
	if header.find(':external') == -1 and header.find(':abstract') == -1:
		text = text[text.find("{"):]
		counter = 0
		index = 0
		for ch in text:
			index += 1
			if counter == 0 and ch == '{':
				counter += 1
				continue
			if ch == '{':
				counter += 1
			if ch == '}':
				counter -= 1
			if counter == 0:
				text = text[index:]
				break
			body += ch
	else:
		text = text[len(header):].strip()
	return body, header, text


class Parser:
	def __init__(self, side):
		self.classes = []
		self.objects = []
		self.functions = []
		self.side = side
		return

	def parse(self, text):
		text = text.strip()
		l = text.find('/*')
		while l != -1:
			r = text.find('*/')
			if r != -1:
				text = text[:l] + text[r + 2:]
			l = text.find('/*')
		lines = text.split('\n')
		for i, line in enumerate(lines):
			if '//' in line:
				lines[i] = line[0:line.find('//')]
		text = '\n'.join(lines)
		while len(text) > 0:
			text = text.strip()
			if is_class(text):
				text = self._create_class(text)
			elif is_enum(text):
				text = self._create_enum_class(text)
			elif is_functon(text):
				text = self._create_function(text)
			else:
				text = self._create_declaration(text)

	def link(self):
		for cls in self.classes:
			if cls.type == 'class':
				cls.addGetTypeFunction()

		for cls in self.classes:
			if cls.is_visitor and self.get_type_of_visitor(cls) != cls.name:
				if cls.name.find('IVisitor') != 0:
					self.create_visitor_class(cls)

		for cls in self.classes:
			behaviors = []
			for name in cls.behaviors:
				c = self.find_class(name)
				if c is None:
					throw_error('cannot find behavior class: {0}<{1}>'.format(cls.name, name))
				behaviors.append(c)
			cls.behaviors = behaviors

		for cls in self.classes:
			cls.is_serialized = self.is_serialised(cls)
			cls.is_visitor = self.is_visitor(cls)
			if cls.is_visitor and cls.name != self.get_type_of_visitor(cls):
				self._append_visit_function(cls)

		for cls in self.classes:
			for member in cls.members:
				args = []
				for arg in member.template_args:
					args.append(self._get_object_type(arg))
				member.template_args = args

		for cls in self.classes:
			cls.onLinked()

	def _create_class(self, text):
		body, header, text = find_body(text)
		cls = Class()
		cls.parse(header)
		cls.parseBody(Parser(self.side), body)
		if self.find_class(cls.name):
			throw_error('Error: duplicate classes [{}]'.format(cls.name))
		self.classes.append(cls)
		return text

	def is_serialised(self, cls):
		if cls.is_serialized:
			return True
		result = False
		for c in cls.behaviors:
			result = result or self.is_serialised(c)
		return result

	def is_visitor(self, cls):
		if cls.is_visitor:
			return True
		result = False
		for c in cls.behaviors:
			result = result or self.is_visitor(c)
		return result

	def is_function_override(self, cls, function):
		if function.name == 'serialize' or function.name == 'deserialize':
			return len(cls.behaviors) > 0

		for c in cls.behaviors:
			for f in c.functions:
				if f.name == function.name and f.return_type == function.return_type and f.args == function.args:
					return True
		is_override = False
		for c in cls.behaviors:
			is_override = is_override or self.is_function_override(c, function)
		return is_override

	def get_type_of_visitor(self, cls):
		if not cls.is_visitor:
			return None

		if cls.name.find('IVisitor') == 0:
			return cls.name

		for c in cls.behaviors:
			if not isinstance(c, Class):
				return 'IVisitor' + cls.name
			if c.is_visitor:
				return self.get_type_of_visitor(c)
		return 'IVisitor' + cls.name

	def _append_visit_function(self, cls):
		visitor_name = self.get_type_of_visitor(cls)
		visitor = self.find_class(visitor_name)
		function = Function()
		function.name = 'visit'
		function.return_type = 'void'
		function.args.append(['ctx', cls.name + '*'])
		visitor.functions.append(function)

		def comparator(func):
			return func.name
		visitor.functions.sort(key=comparator)

	def _get_object_type(self, type_name):
		cls = self.find_class(type_name)
		if cls:
			return cls
		obj = Object()
		type_name = obj.find_modifiers(type_name)
		obj.type = type_name
		obj.parce_type()
		obj.name = ""
		return obj

	def find_class(self, name):
		for cls in self.classes:
			if cls.name == name:
				return cls
		return None

	def _create_enum_class(self, text):
		body, header, text = find_body(text)
		cls = Class()
		cls.type = 'enum'
		cls.parse(header)
		cls.parseBody(Parser(self.side), body)
		self.classes.append(cls)
		return text

	def create_visitor_class(self, cls):
		visitor_name = self.get_type_of_visitor(cls)
		visitor = self.find_class(visitor_name)
		if visitor is None:
			visitor = Class()
			visitor.name = visitor_name
			visitor.group = cls.group
			visitor.type = "class"
			visitor.is_abstract = True
			visitor.is_visitor = True
			self.classes.append(visitor)

	def _create_declaration(self, text):
		lines = text.split("\n")
		line = lines[0]
		if len(lines) > 1:
			text = text[text.find("\n") + 1:]
		else:
			text = ""
		obj = Object()
		obj.parse(line)
		self.objects.append(obj)
		return text

	def _create_function(self, text):
		body, header, text = find_body(text)
		function = Function()
		function.parse(header)
		function.parseBody(body)
		self.functions.append(function)
		return text





