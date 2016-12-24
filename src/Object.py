import re

#void main()
#{
#	return 0;
#}


class Object:
	def __init__(self):
		self.type = ""
		self.template_args = []
		self.name = ""
		self.initial_value = None
		self.is_pointer = False
		self.is_runtime = False
		self.is_static = False
		self.is_const = False
		self.is_key = False

	#float value;
	#float value = 0;
	#int value = func();
	#int value = 1 + 3;
	def parse(self,line):
		str = line.strip();
		str = self._findModifiers(str)
		str = re.sub(";", "", str)
		str = re.sub(", ", ",", str)
		str = re.sub(" ,", ",", str)
		expresion = ""
		if "=" in str:
			k = str.find("=")
			expresion = str[k+1:].strip()
			str = str[0:k].strip()
		args = str.split(" ")
		for arg in args:
			arg = arg.strip()
			if  not arg: 
				continue
			if not self.type:
				self.type = arg
			elif not self.name:
				self.name = arg
		if expresion:
			self.initial_value = expresion
		self._parceType()

	def _parceType(self):
		l = self.type.find("<")
		r = self.type.rindex(">", l) if l != -1 else -1
		if l > -1 and r > -1:
			args = self.type[l+1:r].split(",")
			self.type = self.type[0:l]
			for arg in args:
				arg = arg.strip()
				self.template_args.append(arg)
		self.is_pointer = self.check_pointer()

	def check_pointer(self):
		result = "*" in self.type
		self.type = re.sub("\*", "", self.type)
		return result

	def _findModifiers(self, str):
		self.is_runtime = self.is_runtime or ":runtime" in str
		self.is_static = self.is_static or ":static" in str
		self.is_const = self.is_const or ":const" in str
		self.is_key = self.is_key or ":key" in str
		str = re.sub(":runtime", "", str)
		str = re.sub(":const", "", str)
		str = re.sub(":static", "", str)
		str = re.sub(":key", "", str)
		return str