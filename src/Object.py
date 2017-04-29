import re


class Object:
	def __init__(self):
		self.type = ''
		self.template_args = []
		self.name = ''
		self.initial_value = None
		self.is_pointer = False
		self.is_runtime = False
		self.is_static = False
		self.is_const = False
		self.is_key = False
		self.is_link = ''
		self.side = 'both'

	def parse(self, line):
		line = line.strip()
		line = self.find_modifiers(line)
		line = re.sub(';', '', line)
		line = re.sub(', ', ',', line)
		line = re.sub(' ,', ',', line)
		expression = ''
		if '=' in line:
			k = line.find('=')
			expression = line[k + 1:].strip()
			line = line[0:k].strip()
		args = line.split(' ')
		for arg in args:
			arg = arg.strip()
			if not arg:
				continue
			if not self.type:
				self.type = arg
			elif not self.name:
				self.name = arg
		if expression:
			self.initial_value = expression
		self.parse_type()

	def parse_type(self):
		l = self.type.find('<')
		r = self.type.rindex('>', l) if l != -1 else -1
		if l > -1 and r > -1:
			args = self.type[l + 1:r].split(',')
			self.type = self.type[0:l]
			for arg in args:
				arg = arg.strip()
				self.template_args.append(arg)
		self.is_pointer = self.check_pointer()

	def check_pointer(self):
		result = '*' in self.type
		self.type = re.sub('\*', '', self.type)
		return result

	def find_modifiers(self, line):
		args = ''
		l = line.find('<')
		r = line.rfind('>')
		if l != -1 and r != -1:
			args = line[l:r + 1]
			line = line[0:l] + line[r + 1:]

		self.is_runtime = self.is_runtime or ':runtime' in line
		self.is_static = self.is_static or ':static' in line
		self.is_const = self.is_const or ':const' in line
		self.is_key = self.is_key or ':key' in line
		self.is_link = self.is_link or ':link' in line

		self.is_const = self.is_const or self.is_link

		if ':server' in line:
			self.side = 'server'
		if ':client' in line:
			self.side = 'client'
		line = re.sub(':runtime', '', line)
		line = re.sub(':const', '', line)
		line = re.sub(':static', '', line)
		line = re.sub(':key', '', line)
		line = re.sub(':server', '', line)
		line = re.sub(':client', '', line)
		line = re.sub(':link', '', line)
		if args:
			line = line[0:l] + args + line[l:]

		return line
