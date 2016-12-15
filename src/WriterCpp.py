import re
from Writer import Writer
from Object import Object
from Class import Class
from Function import Function

class WriterCpp(Writer):
	def __init__(self, parser):
		Writer.__init__(self, parser)
		return
	
	def writeObject(self, object):
		out = Writer.writeObject(self, object)
		value = ""
		args = ", ".join(object.template_args)
		if len(object.template_args) > 0:
			fstr = "{0}<{3}> {1}"
		else:
			fstr = "{0} {1}"
		if object.initial_value != None:
			fstr += " = {2}"
			value = object.initial_value
		fstr += ";\n"
		out += fstr.format(object.type, object.name, value, args)
		return out
	
	def writeClass(self, cls):
		out = Writer.writeClass(self, cls)
		if len(cls.behaviors) > 0:
			fstr = "{0} {1} : public {2}"
		else:
			fstr = "{0} {1}"
		fstr += "\n__begin__\npublic:\n{4}\nprotected:\n{3}__end__;\n\n"
		behaviors = ", ".join(cls.behaviors)
		objects = self.writeObjects(cls.members, 1)
		functions = self.writeFunctions(cls.functions, 1)
		out += fstr.format( cls.type, cls.name, behaviors, objects, functions)
		out = re.sub("__begin__", "{", out)
		out = re.sub("__end__", "}", out)
		return out
	
	def writeFunction(self, function, tabs):
		out = Writer.writeFunction(self, function, tabs)
		header = "{0} {1}({2})\n"
		body = "{4}__begin__\n{3}\n{4}__end__\n"
		fstr = header + body
		body = ""
		for operation in function.operations:
			fline = "{0};"
			line = self.tabs(tabs+1) + fline.format(operation);
			body += line
		args = ", ".join(function.args)
		out += fstr.format( function.return_type, function.name, args, body, self.tabs(tabs) )

		return out


