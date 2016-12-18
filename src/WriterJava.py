import re
from Writer import Writer

class WriterJava(Writer):
	def __init__(self, outDirectory, parser):
		Writer.__init__(self, outDirectory, parser)

	def writeObject(self, object, tabs, flags):
		out = ""
		if object.initial_value != None:
			out += "\tprivate {0} {1} = {2};\n".format( object.type, object.name, object.initial_value)
		else:
			out += "\tprivate {0} {1};\n".format( object.type, object.name)
		return {flags:out}
	
	def writeClass(self, cls, tabs, flags):
		out = ""
		out += "{0}\n\n".format( self._getPackage() )
		out += "{0}\n\n".format( self._getImports(cls) )
		if len(cls.behaviors) > 0:
			behaviors = []
			for c in cls.behaviors:
				behaviors.append(c.name)
			behaviors = ", ".join(behaviors)
			out += "public class {0} extends {1}__begin__\n".format( cls.name, behaviors )
		else:
			out += "public class {0}__begin__\n".format( cls.name )
		
		for obj in cls.members:
			out += self.writeObject(obj, tabs+1, flags)[flags]
		
		for function in cls.functions:
			out += self.writeFunction( function, 1, flags )[flags]
		out += "\n__end__"
		out = re.sub("__begin__", "{", out)
		out = re.sub("__end__", "}", out)
		out = re.sub("self.", "", out)
		return {flags:out}
	
	def writeFunction(self, function, tabs, flags):
		out = ""
		isOverride = False
		if isOverride:
			fstr = "\n{0}@Override\n".format(self.tabs())
		else:
			fstr = "\n"
		fstr += "{0}public {2} {1}({3}) __begin__{4}\n{0}__end__\n"
		
		args = []
		for arg in function.args:
			args.append(arg[1] + " " + arg[0])
		args = ", ".join(args)
		
		body = ""
		for operation in function.operations:
			fline = "\n{1}{0};"
			line = fline.format(operation, self.tabs(tabs+1));
			body += line

		out = fstr.format( self.tabs(tabs), function.name, function.return_type, args, body );
		return {flags:out}

	def _getPackage(self):
		return "package com.mg;"

	def _getImports(self, cls):
		return ""

	def _getFilenameForClass(self, class_name):
		return class_name + ".java"