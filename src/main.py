import fileutils
from arguments_parser import get_arg, get_bool, get_directory
from Parser import Parser
from WriterCppSerializatorJson import WriterCppSerializatorJson
from WriterCppSerializatorXml import WriterCppSerializatorXml
from WriterPySerializationJson import WriterPySerializationJson
from WriterPySerializationXml import WriterPySerializationXml


def validate_arg_language(language):
	if language not in ['cpp', 'py']:
		print 'Unknown language (-l :', language, ')'
		print 'Please use any from [cpp, py]'
		exit(-1)


def validate_arg_format(format):
	if format not in ['xml', 'json']:
		print 'Unknown language (-l :', format, ')'
		print 'Please use any from [xml, json]'
		exit(-1)


def validate_arg_side(side):
	if side not in ['both', 'server', 'client']:
		print 'Unknown side (-side :', side, ')'
		print 'Please use any from [both, server, client]'
		exit(-1)


def main():
	configs_directory = get_directory('-i', '../config/')
	out_directory = get_directory('-0', '../out/')
	tests = get_bool('-t', False)
	language = get_arg('-l', 'cpp')
	format = get_arg('-f', 'xml')
	side = get_arg('-side', 'both')

	validate_arg_language(language)
	validate_arg_format(format)
	validate_arg_side(side)

	parser = Parser(side)
	files = fileutils.getFilesList(configs_directory)
	for file in files:
		if file.find('.mlc') == len(file) - 4:
			text = open(configs_directory + file).read()
			parser.parse(text)
	parser.link()

	writer = None
	if language == 'py':
		if format == 'xml':
			writer = WriterPySerializationXml(out_directory, parser, tests, configs_directory)
		else:
			writer = WriterPySerializationJson(out_directory, parser, tests, configs_directory)
	elif language == 'cpp':
		if format == 'xml':
			writer = WriterCppSerializatorXml(out_directory, parser, tests)
		else:
			writer = WriterCppSerializatorJson(out_directory, parser, tests)
	writer.removeOld()

	print 'mlc(lang: {}, side: {}) finished successful in silent mode'.format(language, side)


if __name__ == '__main__':
	main()
