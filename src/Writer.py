import fileutils


class Writer:
	def __init__(self, outDirectory, parser):
		self.parser = parser
		self.buffers = {}
		self.out_directory = outDirectory
		self.created_files = []

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
		return {flags:""}

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
			dict = self.writeClass(cls, tabs, flags)
			self.save( self._getFilenameForClass(cls), dict[flags] )
			out = self._add( out, dict )
		return out

	def writeFunctions(self, functions, tabs, flags):
		out = ''
		for function in functions: out += self.tabs(tabs) + self.writeFunction(function, tabs, flags)
		return out

	def prepareFile(self, body):
		return body

	def save(self, filename, string):
		string = self.parser.copyright_text + self.prepareFile(string)
		filename = self.out_directory + filename
		self.created_files.append(filename)
		exist = fileutils.isfile(filename)
		writed = fileutils.write(filename, string)
		if writed:
			msg = 'create:' if not exist else 'rewrited'
			print msg, filename

	def removeOld(self):
		if not fileutils.isdir(self.out_directory):
			return
		files = fileutils.get_files_list(self.out_directory)
		for file in files:
			if self.out_directory + file not in self.created_files:
				if not file.endswith('.pyc'):
					print 'remove', file
				fileutils.remove(self.out_directory + file)

	def saveConfigFile(self, format):
		pattern = '#ifndef __mg_Config_h__\n#define __mg_Config_h__\n\n{}\n\n#endif //#ifndef __mg_Config_h__'
		configs = []
		configs.append('#define MG_JSON 1')
		configs.append('#define MG_XML 2')
		configs.append('\n#define MG_SERIALIZE_FORMAT MG_' + format.upper())
		configs = '\n'.join(configs)
		self.save('config.h', pattern.format(configs))

	def _getFilenameForClass(self, cls):
		return cls.name


