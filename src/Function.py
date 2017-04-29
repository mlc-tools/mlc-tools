import re
from Object import Object


class Function:
	def __init__(self):
		self.operations = []
		self.return_type = ''
		self.name = ''
		self.args = []
		self.is_const = False
		self.is_external = False
		self.is_static = False
		self.is_abstract = False
		self.side = 'both'

	def parse(self, line):
		line = line.strip()
		line = self._find_modifiers(line)
		k = line.find('function')
		if k == 0:
			line = line[k + 8:].strip()
		args_s = line[line.find('(') + 1:line.find(')')]
		args = []
		counter = 0
		k = 0
		i = 0
		for ch in args_s:
			if ch == '<': counter += 1
			if ch == '>': counter -= 1
			if counter == 0 and (ch == ',' or i == len(args_s) - 1):
				r = i if i < len(args_s) - 1 else i + 1
				args.append(args_s[k:r])
				k = i + 1
			i += 1

		if args and args[0]:
			for arg in args:
				arg = arg.strip()

				def p(ch, arg):
					k = -1
					counter = 0
					for i, c in enumerate(arg):
						if c == '<': counter += 1
						if c == '>': counter -= 1
						if counter == 0 and c == ch:
							k = i
							break
					if k == -1:
						return False

					type = (arg[:k].strip() + ch).strip()
					name = arg[k + 1:].strip()
					self.args.append([name, type])
					return True

				if not (p('*', arg) or p('&', arg) or p(' ', arg)):
					exit(-1)

		line = line[0:line.find('(')].strip()
		self.return_type, self.name = line.split(' ')
		return

	def parse_body(self, body):
		counters = {}
		dividers = ['{}', '()']
		operations = []
		operation = ''

		def counter():
			sum = 0
			for div in counters:
				sum += counters[div]
			return sum

		if self.name == 'compute_position':
			self.name = self.name

		for ch in body:
			for div in dividers:
				if ch in div:
					if div not in counters:
						counters[div] = 0
					counters[div] += 1 if ch == div[0] else -1
			if counter() < 0:
				print 'error parsing function "{}" body'.format(self.name)
				exit(-1)
			operation += ch
			if counter() == 0 and ch in ';}':
				operations.append(operation.strip())
				operation = ''
				continue
		operations.append(operation.strip())
		self.operations = [operation for operation in operations if operation]
		return

	def _find_modifiers(self, str):
		self.is_external = self.is_external or ':external' in str
		self.is_abstract = self.is_abstract or ':abstract' in str
		self.is_static = self.is_static or ':static' in str
		self.is_const = self.is_const or ':const' in str
		if ':server' in str: self.side = 'server'
		if ':client' in str: self.side = 'client'
		str = re.sub(':external', '', str)
		str = re.sub(':static', '', str)
		str = re.sub(':const', '', str)
		str = re.sub(':abstract', '', str)
		str = re.sub(':server', '', str)
		str = re.sub(':client', '', str)
		return str
