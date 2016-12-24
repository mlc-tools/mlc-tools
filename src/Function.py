import re
from Object import Object

class Function:
	def __init__(self):
		self.operations = []
		self.return_type = ""
		self.name = ""
		self.args = []
		self.is_const = False
		self.is_external = False
		self.is_static = False
		self.is_abstract = False

	def parse(self, line):
		line = line.strip()
		line = self._findModifiers(line)
		k = line.find("function")
		if k == 0:
			line = line[k+8:].strip()
		args = line[line.find("(")+1:line.find(")")].split(",")
		if args and args[0]:
			for arg in args:
				arg = arg.strip()
				def p(ch, arg):
					if ch not in arg:
						return False
					if len(arg.split(ch)) != 2:
						print "args pair not pair";
						return False
					type = (arg.split(ch)[0].strip() + ch).strip()
					name = arg.split(ch)[1].strip()
					self.args.append( [name, type] )
					return True
				if not (p("*",arg) or p("&",arg) or p(" ",arg)):
					exit(-1)
					
		line = line[0:line.find("(")].strip()
		self.return_type, self.name = line.split(" ")
		return
	def parseBody(self, body):
		counters = {}
		dividers = ["{}", "()"]
		operations = []
		operation = ""
		
		def counter():
			sum = 0
			for div in counters:
				sum += counters[div]
			return sum

		if self.name == "compute_position":
			self.name = self.name

		for ch in body:
			for div in dividers:
				if ch in div: 
					if div not in counters:
						counters[div] = 0
					counters[div] += 1 if ch == div[0] else -1
			if counter() < 0:
				print "error parsing function '{}' body".format(self.name)
				exit(-1)
			operation += ch
			if counter() == 0 and ch in ';}':
				operations.append(operation.strip())
				operation = ""
				continue
		operations.append(operation.strip())
		self.operations = [operation for operation in operations if operation]
		return
	
	def _findModifiers(self, str):
		self.is_external = self.is_external or ":external" in str
		self.is_abstract = self.is_abstract or ":abstract" in str
		self.is_static = self.is_static or ":static" in str
		self.is_const = self.is_const or ":const" in str
		str = re.sub(":external", "", str)
		str = re.sub(":static", "", str)
		str = re.sub(":const", "", str)
		str = re.sub(":abstract", "", str)
		return str