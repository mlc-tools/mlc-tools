import fileutils
from arguments_parser import get_arg, get_bool, get_directory
from Parser import Parser
from DataParser import DataParser
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
    data_directory = get_directory('-data', '')
    out_data_directory = get_directory('-data_out', '')
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

    if data_directory:
        classes = []
        for class_ in parser.classes:
            if class_.is_storage:
                classes.append(class_)
        data_parser = DataParser(classes, data_directory)
        data_file = data_parser.flush(out_data_directory)
        writer.create_data_storage(data_file)

    writer.remove_non_actual_files()
    print 'mlc(lang: {}, format: {} side: {}) finished successful'.format(language, serialize_format, side)


if __name__ == '__main__':
    main()
