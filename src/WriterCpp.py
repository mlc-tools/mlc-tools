import re
from Writer import Writer
from Object import Object
from Class import Class
from Function import Function

FLAG_HPP = 2
FLAG_CPP = 4

class WriterCpp(Writer):
	def __init__(self, parser):
		Writer.__init__(self, parser)
		self._currentClass = None
		return
	
	def writeObject(self, object, tabs, flags):
		out = Writer.writeObject(self, object, tabs, flags)
		value = ""
		args = ", ".join(object.template_args)
		if len(object.template_args) > 0:
			fstr = "{4}{0}<{3}> {1}"
		else:
			fstr = "{4}{0} {1}"
		if object.initial_value != None:
			fstr += " = {2}"
			value = object.initial_value
		fstr += ";\n"
		out[flags] += fstr.format(object.type, object.name, value, args, self.tabs(tabs))
		return out

	def writeClass(self, cls, tabs, flags):
		out = {}
		if flags & FLAG_HPP:
			out = Writer._add(self, out, self._writeClassHpp(cls, tabs))
		if flags & FLAG_CPP:
			out = Writer._add(self, out, self._writeClassCpp(cls, tabs))
		return out
	
	def _writeClassHpp(self, cls, tabs):
		out = Writer.writeClass(self, cls, tabs, FLAG_HPP)
		behaviors = ", ".join(cls.behaviors)
		objects = self.writeObjects(cls.members, 1, FLAG_HPP)
		functions = self.writeFunctions(cls.functions, 1, FLAG_HPP)
		constructor = self._createConstructorFunctionHpp(cls, 1)

		if len(cls.behaviors) > 0:
			fstr = "{0} {1} : public {2}"
		else:
			fstr = "{0} {1}"
		fstr += "\n__begin__\npublic:\n{5}\n{4}\nprotected:\n{3}__end__;\n\n"

		out[FLAG_HPP] += fstr.format( cls.type, cls.name, behaviors, objects[FLAG_HPP], functions[FLAG_HPP], constructor);
		out[FLAG_HPP] = re.sub("__begin__", "{", out[FLAG_HPP])
		out[FLAG_HPP] = re.sub("__end__", "}", out[FLAG_HPP])
		return out

	def _writeClassCpp(self, cls, tabs):
		out = Writer.writeClass(self, cls, tabs, FLAG_CPP)
		self._currentClass = cls
		functions = self.writeFunctions(cls.functions, 0, FLAG_CPP)
		constructor = self._createConstructorFunctionCpp(cls, tabs)
		self._currentClass = None
		fstr = "#include\"{0}.h\"\n\n{2}\n{1}"
		out[FLAG_CPP] += fstr.format( cls.name, functions[FLAG_CPP], constructor )
		out[FLAG_CPP] = re.sub("__begin__", "{", out[FLAG_CPP])
		out[FLAG_CPP] = re.sub("__end__", "}", out[FLAG_CPP])
		return out
	
	def _createConstructorFunctionHpp(self, cls, tabs):
		fstr = "{1}{0}();\n"
		return fstr.format( cls.name, self.tabs(tabs) )

	def _createConstructorFunctionCpp(self, cls, tabs):
		initialize = ""
		for obj in cls.members:
			if obj.initial_value != None:
				fstr = "\n{2} {0}({1})"
				s = ","
				if initialize == "": 
					s = ":"
				str = fstr.format(obj.name, obj.initial_value, s)
				initialize += str

		fstr = "{0}::{0}(){1}\n__begin__\n{2}\n__end__\n"
		str = fstr.format( cls.name, initialize, self.tabs(tabs) )
		str = re.sub("__begin__", "{", str)
		str = re.sub("__end__", "}", str)
		return str
	
	def writeFunction(self, function, tabs, flags):
		out = {}
		if flags & FLAG_HPP:
			fstr = "{3}{0} {1}({2});\n"
			args = []
			for arg in function.args:
				args.append(function.args[arg] + " " + arg)
			args = ", ".join(args)
			out[FLAG_HPP] = fstr.format( function.return_type, function.name, args, self.tabs(tabs) )
		if flags & FLAG_CPP:
			header = "{4}{0} {5}::{1}({2})\n"
			body = "{4}__begin__{3}\n{4}__end__\n"
			fstr = header + body
			body = ""
			for operation in function.operations:
				fline = "{0};"
				line = "\n" + self.tabs(tabs+1) + fline.format(operation);
				body += line
			args = []
			for arg in function.args:
				args.append(function.args[arg] + " " + arg)
			args = ", ".join(args)
			out[FLAG_CPP] = fstr.format( function.return_type, function.name, args, body, self.tabs(tabs), self._currentClass.name )
			out[FLAG_CPP] = re.sub("self.", "this->", out[FLAG_CPP])

		return out

	def writeClasses(self, classes, tabs, flags):
		out = {FLAG_CPP : "", FLAG_HPP : ""}
		for cls in classes:
			out = self._add( out, self.writeClass(cls, tabs, FLAG_HPP) )
		for cls in classes: 
			out = self._add( out, self.writeClass(cls, tabs, FLAG_CPP) )
		return out

	def writeFunctions(self, functions, tabs, flags):
		out = {}
		for function in functions: 
			out = self._add( out, self.writeFunction(function, tabs, flags) )
		return out

