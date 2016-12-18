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

	def parse(self, line):
		line = line.strip()
		line = self._findModifiers(line)
		k = line.find("function")
		if k > -1:
			line = line[k+8:].strip()
		args = line[line.find("(")+1:line.find(")")].split(",")
		if len(args) > 0 and args[0] != "":
			for arg in args:
				arg = arg.strip()
				if arg.find( "*" ) > -1:
					if not (len(arg.split("*")) == 2):
						print "args pair not pair";
						exit(-1)
					type = arg.split("*")[0].strip() + "*"
					name = arg.split("*")[1].strip()
					self.args.append( [name, type] )
				elif arg.find( "&" ) > -1:
					if not (len(arg.split("&")) == 2):
						print "args pair not pair";
						exit(-1)
					type = arg.split("&")[0].strip() + "&"
					name = arg.split("&")[1].strip()
					self.args.append( [name, type] )
				elif arg.find( " " ) > -1:
					if not (len(arg.split(" ")) == 2):
						print "args pair not pair";
						exit(-1)
					type = arg.split(" ")[0].strip()
					name = arg.split(" ")[1].strip()
					self.args.append( [name, type] )
				else:
					print "error parsing arguments"
					exit(-1)
		line = line[0:line.find("(")].strip()
		self.return_type = line.split(" ")[0]
		self.name = line.split(" ")[1]
		return
	def parseBody(self, body):
		operations = body.split(";")
		for operation in operations:
			operation = operation.strip()
			if len(operation) > 0:
				self.operations.append(operation)
		return
	
	def _findModifiers(self, str):
		self.is_external = str.find( ":external" ) != -1
		self.is_static = str.find( ":static" ) != -1
		self.is_const = str.find( ":const" ) != -1
		str = re.sub(":external", "", str)
		str = re.sub(":static", "", str)
		str = re.sub(":const", "", str)
		return str