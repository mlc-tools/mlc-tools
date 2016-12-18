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
		self.is_runtime = False
		self.is_static = False
		self.is_const = False

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
		k = str.find("=")
		if k > -1:
			expresion = str[k+1:].strip()
			str = str[0:k].strip()
		args = str.split(" ")
		for arg in args:
			arg = arg.strip()
			if len(arg) == 0: 
				continue
			if self.type == "":
				self.type = arg
			elif self.name == "":
				self.name = arg
		if not expresion == "":
			self.initial_value = expresion
		self.__parceType()
	
	def __parceType(self):
		l = self.type.find("<")
		r = self.type.find(">")
		if l > -1 and r > -1:
			args = self.type[l+1:r].split(",")
			for arg in args:
				arg = arg.strip()
				self.template_args.append(arg)
			self.type = self.type[0:l]


	def _findModifiers(self, str):
		self.is_runtime = str.find( ":runtime" ) != -1
		self.is_const = str.find( ":const" ) != -1
		self.is_static = str.find( ":static" ) != -1
		str = re.sub(":runtime", "", str)
		str = re.sub(":const", "", str)
		str = re.sub(":static", "", str)
		return str