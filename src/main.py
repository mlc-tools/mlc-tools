import fileutils
import argparse
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
    parser = argparse.ArgumentParser()
    parser.add_argument('-i',  type=str, help='Path to classes configs', required=False, default='../config/')
    parser.add_argument('-o', type=str, help='Out Path for classes', required=False, default='../out/')
    parser.add_argument('-l', type=str, help='Used language. Supported cpp, py. Default: cpp', required=False, default='cpp')
    parser.add_argument('-f', type=str, help='Used serialized format. Supported xml, json. Default: xml', required=False, default='xml')
    parser.add_argument('-side', type=str, help='For different side generation - use both. server. client. Default: both', required=False, default='both')
    parser.add_argument('-data', type=str, help='Path to data configs', required=False, default='')
    parser.add_argument('-data_out', type=str, help='Out Path for data', required=False, default='')
    args = parser.parse_args()

    configs_directory = fileutils.normalize_path(args.i)
    out_directory = fileutils.normalize_path(args.o)
    data_directory = fileutils.normalize_path(args.data)
    out_data_directory = fileutils.normalize_path(args.data_out)
    language = args.l
    serialize_format = args.f
    side = args.side

    validate_arg_language(language)
    validate_arg_format(serialize_format)
    validate_arg_side(side)

    parser = Parser(side)
    parser.set_configs_directory(configs_directory)
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
        data_parser = DataParser(classes, serialize_format, data_directory)
        data_parser.flush(out_data_directory)
    writer.create_data_storage()

    writer.remove_non_actual_files()
    print 'mlc(lang: {}, format: {} side: {}) finished successful'.format(language, serialize_format, side)


if __name__ == '__main__':
    main()
