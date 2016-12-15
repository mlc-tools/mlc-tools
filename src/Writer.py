class Writer:
	def __init__(self, parser):
		self.out = ""
		
		self.out += self.writeObjects(parser.objects)
		self.out += self.writeFunctions(parser.functions,0)
		self.out += self.writeClasses(parser.classes)

		return
	
	def tabs(self, tabs):
		out = ""
		for i in range(tabs): out += "\t"
		return out
	
	def writeObject(self, object):
		out = ""
		return out
	
	def writeClass(self, cls):
		out = "\n"
		return out
	
	def writeFunction(self, function, tabs):
		out = ""
		return out

	def writeObjects(self, objects, tabs = 0):
		out = ""
		for object in objects: out += self.tabs(tabs) + self.writeObject(object)
		return out

	def writeClasses(self, classes):
		out = ""
		for cls in classes:
			out += self.writeClass(cls)
		out += "\n"
		return out;

	def writeFunctions(self, functions, tabs):
		out = ""
		for function in functions: out += self.tabs(tabs) + self.writeFunction(function, tabs)
		return out