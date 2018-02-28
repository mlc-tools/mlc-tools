import fileutils
import argparse
from Parser import Parser
from DataParser import DataParser
from WriterCpp import WriterCpp
from WriterPython import WriterPython
from WriterPhp import WriterPhp
from Copyright import Copyright
from Error import Log
import os


def validate_arg_language(language):
    if language not in ['cpp', 'py', 'php']:
        Log.error('Unknown language (-l : %s)' % language)
        Log.error('Please use any from [cpp, py, php]')
        exit(-1)


def validate_arg_format(format):
    if format not in ['xml', 'json']:
        Log.error('Unknown format (-l : %s)' % format)
        Log.error('Please use any from [xml, json]')
        exit(-1)


def validate_arg_side(side):
    if side not in ['both', 'server', 'client']:
        Log.error('Unknown side (-side :' % side)
        Log.error('Please use any from [both, server, client]')
        exit(-1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i',  type=str, help='Path to classes configs. Default = ./config/',
                        required=False, default='./config/')
    parser.add_argument('-o', type=str, help='Out Path for classes. Default = ./out/',
                        required=False, default='./out/')
    parser.add_argument('-l', type=str, help='Used language. Supported cpp, py, php. Default = cpp',
                        required=False, default='cpp')
    parser.add_argument('-f', type=str, help='Used serialized format. Supported xml, json. Default = xml',
                        required=False, default='xml')
    parser.add_argument('-side', type=str,
                        help='To different side generation, used both, server, client. Default = both',
                        required=False, default='both')
    parser.add_argument('-data', type=str, help='Path to static data configs. Default = empty, conversion is not used',
                        required=False, default='')
    parser.add_argument('-data_out', type=str, help='Out path for static data config. Default = empty',
                        required=False, default='')
    parser.add_argument('-only_data', type=str, help='Flag for build only data xml. Default = no',
                        required=False, default='no')
    parser.add_argument('-protocols', type=str,
                        help='Path to file with serialization protocols. Default = empty, default protocol is used',
                        required=False, default='')
    parser.add_argument('-php_validate', type=str,
                        help='Check PHP features on generate other languages. Default = yes',
                        required=False, default='yes')
    parser.add_argument('-use_colors', type=str, help='Using colors on outputting to the console',
                        required=False, default='yes')
    parser.add_argument('-test_script', type=str, help='The path to the script to run the tests',
                        required=False, default='')
    parser.add_argument('-test_script_args', type=str, help='The arg to pass to test script',
                        required=False, default='')
    parser.add_argument('-disable_logs', type=str, help='Disabling logs to output',
                        required=False, default='no')
    args = parser.parse_args()

    configs_directory = fileutils.normalize_path(args.i)
    out_directory = fileutils.normalize_path(args.o)
    data_directory = fileutils.normalize_path(args.data)
    out_data_directory = fileutils.normalize_path(args.data_out)
    path_to_protocols = fileutils.normalize_path(args.protocols, False)
    language = args.l
    serialize_format = args.f
    only_data = args.only_data.lower() == 'yes'
    side = args.side
    php_validate = args.php_validate.lower() == 'yes'
    use_colors = args.use_colors.lower() == 'yes'
    disable_logs = args.disable_logs.lower() == 'yes'

    validate_arg_language(language)
    validate_arg_format(serialize_format)
    validate_arg_side(side)

    Log.use_colors = use_colors
    Log.disable_logs = disable_logs
    parser = Parser(side, language == 'cpp')
    parser.set_configs_directory(configs_directory)
    files = fileutils.get_files_list(configs_directory)
    for file in files:
        if file.endswith('.mlc'):
            text = open(configs_directory + file).read()
            parser.parse(text)
    parser.link()
    if php_validate:
        parser.validate_php_features()
    parser.copyright_text = Copyright(configs_directory).text
    if path_to_protocols:
        parser.parse_serialize_protocol(path_to_protocols)
    else:
        parser.load_default_serialize_protocol(language, serialize_format)

    writer = None
    if language == 'cpp':
        writer = WriterCpp(parser, serialize_format)
    elif language == 'py':
        writer = WriterPython(parser, serialize_format)
    elif language == 'php':
        writer = WriterPhp(parser, serialize_format)
    if not only_data:
        writer.generate()
    writer.save_generated_classes(out_directory)
    if not only_data:
        writer.save_config_file()

    if data_directory:
        classes = []
        for class_ in parser.classes:
            if class_.is_storage:
                classes.append(class_)
        for class_ in parser.classes_for_data:
            if class_.is_storage:
                classes.append(class_)
        data_parser = DataParser(classes, serialize_format, data_directory)
        data_parser.flush(out_data_directory)
        if not only_data:
            writer.create_data_storage()

    if not only_data:
        writer.remove_non_actual_files()
    Log.message('mlc(lang: {}, format: {} side: {}) finished successful'.format(language, serialize_format, side))

    if args.test_script and os.path.isfile(args.test_script):
        Log.message('Run test (%s):' % args.test_script)
        if os.system('python {} {}'.format(args.test_script, args.test_script_args)) != 0:
            exit(1)


if __name__ == '__main__':
    main()
