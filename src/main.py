import fileutils
from arguments_parser import get_arg, get_bool, get_directory
from Parser import Parser
from WriterCppSerializatorJson import WriterCppSerializatorJson
from WriterCppSerializationXml import WriterCppSerializationXml
from WriterPySerializationJson import WriterPySerializationJson
from WriterPySerializationXml import WriterPySerializationXml
from Copyright import Copyright


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
    out_directory = get_directory('-o', '../out/')
    language = get_arg('-l', 'cpp')
    serialize_format = get_arg('-f', 'xml')
    side = get_arg('-side', 'both')

    validate_arg_language(language)
    validate_arg_format(serialize_format)
    validate_arg_side(side)

    parser = Parser(side)
    parser.copyright_text = Copyright(configs_directory).text
    files = fileutils.get_files_list(configs_directory)
    for file in files:
        if file.find('.mlc') == len(file) - 4:
            text = open(configs_directory + file).read()
            parser.parse(text)
    parser.link()

    writer = None
    if language == 'py':
        if serialize_format == 'xml':
            writer = WriterPySerializationXml(out_directory, parser, configs_directory)
        else:
            writer = WriterPySerializationJson(out_directory, parser, configs_directory)
    elif language == 'cpp':
        if serialize_format == 'xml':
            writer = WriterCppSerializationXml(out_directory, parser)
        else:
            writer = WriterCppSerializatorJson(out_directory, parser)
    writer.save_config_file(serialize_format)
    writer.remove_non_actual_files()

    print 'mlc(lang: {}, format: {} side: {}) finished successful'.format(language, serialize_format, side)


if __name__ == '__main__':
    main()
