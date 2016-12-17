class Writer:
	def __init__(self, parser):
		self.buffers = {}
		
		self.buffers = self._add(self.buffers, self.writeObjects(parser.objects, 0, 0))
		self.buffers = self._add(self.buffers, self.writeFunctions(parser.functions, 0, 0))
		self.buffers = self._add(self.buffers, self.writeClasses(parser.classes, 0, 0))

		return
	
	def _add(self, inDict, toDict ):
		for key in toDict:
			if key in inDict:
				inDict[key] += toDict[key]
			else:
				inDict[key] = toDict[key]
		return inDict

	def tabs(self, tabs):
		out = ""
		for i in range(tabs): out += "\t"
		return out
	
	def writeObject(self, object, tabs, flags):
		return {flags:""}
	
	def writeClass(self, cls, tabs, flags):
		return {flags:"\n"}
	
	def writeFunction(self, function, tabs, flags):
		return {flags:""}

	def writeObjects(self, objects, tabs, flags):
		out = {flags:"\n"}
		for object in objects: 
			out = self._add(out, self.writeObject(object, tabs, flags))
		return out

	def writeClasses(self, classes, tabs, flags):
		out = {flags:"\n"}
		for cls in classes:
			out = self._add(out, self.writeClass(cls, tabs, flags))
		return out;

	def writeFunctions(self, functions, tabs, flags):
		out = ""
		for function in functions: out += self.tabs(tabs) + self.writeFunction(function, tabs, flags)
		return out