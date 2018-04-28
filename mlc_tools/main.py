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
from version import __version__


class Generator:

    def __init__(self, configs_directory='', **kwargs):

        def get(arg, default=None):
            return kwargs[arg] if arg in kwargs else default

        def get_bool(arg, default='yes'):
            return get(arg) == 'yes'

        Log.use_colors = get_bool('use_colors', 'no')
        Log.disable_logs = get_bool('disable_logs', 'no')

        self.configs_directory = configs_directory
        self.out_directory = get('out_directory')
        self.data_directory = get('data_directory')
        self.out_data_directory = get('out_data_directory')
        self.path_to_protocols = get('path_to_protocols')
        self.language = get('language')
        self.serialize_format = get('serialize_format')
        self.only_data = get_bool('only_data', 'no')
        self.namespace = get('namespace', 'mg')
        self.side = get('side', 'both')
        self.php_validate = get_bool('php_validate')
        self.test_script = get('test_script')
        self.test_script_args = get('test_script_args')
        self.generate_tests = get_bool('generate_tests')

    @staticmethod
    def check_version(requere):
        v = __version__.split('.')
        r = requere.split('.')
        for i in xrange(3):
            if len(r) >= i + 1:
                if r[i] != v[i]:
                    rr = int(r[i])
                    vv = int(v[i])
                    return -1 if vv < rr else 1
        return 0

    def parse_args(self):
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
        parser.add_argument('-namespace', type=str, help='Used namespace on generate cpp code. Default = mg',
                            required=False, default='mg')
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
        parser.add_argument('-generate_tests', type=str, help='Generate classes marked as :test',
                            required=False, default='yes')
        args = parser.parse_args()

        self.configs_directory = fileutils.normalize_path(args.i)
        self.out_directory = fileutils.normalize_path(args.o)
        self.data_directory = fileutils.normalize_path(args.data)
        self.out_data_directory = fileutils.normalize_path(args.data_out)
        self.path_to_protocols = fileutils.normalize_path(args.protocols, False)
        self.language = args.l
        self.serialize_format = args.f
        self.only_data = args.only_data.lower() == 'yes'
        self.namespace = args.namespace
        self.side = args.side
        self.php_validate = args.php_validate.lower() == 'yes'
        self.test_script = args.test_script
        self.test_script_args = args.test_script_args
        self.generate_tests = args.generate_tests
        Log.use_colors = args.use_colors.lower() == 'yes'
        Log.disable_logs = args.disable_logs.lower() == 'yes'

    def _parse(self):
        self.parser = Parser(self.side, self.generate_tests)
        self.parser.set_configs_directory(self.configs_directory)
        self.parser.generate_patterns()
        files = fileutils.get_files_list(self.configs_directory)
        for file in files:
            if file.endswith('.mlc'):
                text = open(self.configs_directory + file).read()
                self.parser.parse(text)
        self.parser.link()
        if self.php_validate:
            self.parser.validate_php_features()
        self.parser.copyright_text = Copyright(self.configs_directory).text

    def generate(self,
                 language=None,
                 serialize_format=None,
                 out_directory=None,
                 side=None,
                 namespace=None,
                 validate_php=False,
                 path_to_protocols=None,
                 only_data=None,
                 gen_data_storage=True
                 ):
        if path_to_protocols is not None:
            self.path_to_protocols = path_to_protocols
        if language is not None:
            self.language = language
        if serialize_format is not None:
            self.serialize_format = serialize_format
        if namespace is not None:
            self.namespace = namespace
        if out_directory is not None:
            self.out_directory = out_directory
        if only_data is not None:
            self.only_data = only_data
        if side is not None:
            self.side = side
        if validate_php is not None:
            self.validate_php = validate_php
        self.configs_directory = fileutils.normalize_path(self.configs_directory)
        self.out_directory = fileutils.normalize_path(self.out_directory)

        self.validate_arg_language()
        self.validate_arg_format()
        self.validate_arg_side()

        self._parse()

        if self.path_to_protocols:
            self.parser.parse_serialize_protocol(self.path_to_protocols)
        else:
            self.parser.load_default_serialize_protocol(self.language, self.serialize_format)

        self.writer = None
        if self.language == 'cpp':
            self.writer = WriterCpp(self.parser, self.serialize_format, namespace=self.namespace)
        elif self.language == 'py':
            self.writer = WriterPython(self.parser, self.serialize_format)
        elif self.language == 'php':
            self.writer = WriterPhp(self.parser, self.serialize_format)
        if not self.only_data:
            self.writer.generate()
        self.writer.save_generated_classes(self.out_directory)
        if not self.only_data:
            self.writer.save_config_file()

        if gen_data_storage:
            self.writer.create_data_storage()

        self.parser.save_patterns(self.writer, self.language)
        self.writer.remove_non_actual_files()
        Log.message('mlc(lang: {}, format: {} side: {}) generate successful'.format(self.language, self.serialize_format, self.side))

    def generate_data(self,
                      data_directory=None,
                      out_data_directory=None,
                      serialize_format=None,
                      only_data=None,
                      ):
        if data_directory is not None:
            self.data_directory = data_directory
        if out_data_directory is not None:
            self.out_data_directory = out_data_directory
        if only_data is not None:
            self.only_data = only_data
        self.data_directory = fileutils.normalize_path(self.data_directory)
        self.out_data_directory = fileutils.normalize_path(self.out_data_directory)

        self.validate_arg_format()
        self.validate_arg_side()

        if self.data_directory:
            classes = []
            for class_ in self.parser.classes:
                if class_.is_storage:
                    classes.append(class_)
            for class_ in self.parser.classes_for_data:
                if class_.is_storage:
                    classes.append(class_)
            self.data_parser = DataParser(classes, self.serialize_format, self.data_directory)
            self.data_parser.flush(self.out_data_directory)

    def run_test(self, test_script=None, test_script_args=None):
        if test_script is not None:
            self.test_script = test_script
        if test_script_args is not None:
            self.test_script_args = test_script_args
        if self.test_script and os.path.isfile(self.test_script):
            Log.message('Run test (%s):' % self.test_script)
            if os.system('python {} {}'.format(self.test_script, self.test_script_args)) != 0:
                exit(1)

    def validate_arg_language(self):
        if self.language not in ['cpp', 'py', 'php']:
            Log.error('Unknown language (-l : %s)' % self.language)
            Log.error('Please use any from [cpp, py, php]')
            exit(-1)

    def validate_arg_format(self):
        if self.serialize_format not in ['xml', 'json']:
            Log.error('Unknown format (-l : %s)' % self.serialize_format)
            Log.error('Please use any from [xml, json]')
            exit(-1)

    def validate_arg_side(self):
        if self.side not in ['both', 'server', 'client']:
            Log.error('Unknown side (-side :' % self.side)
            Log.error('Please use any from [both, server, client]')
            exit(-1)


def main():
    gen = Generator()
    gen.parse_args()
    gen.generate()
    gen.generate_data()


def test_game_s():
    game_root = '/work/survival_2d/'
    generator = Generator(game_root + 'config', generate_tests='yes')
    generator.generate('cpp', 'xml', game_root + 'client/generated/web', 'client')


def test():
    gen = Generator('../simple_test/config', validate_php=False)
    gen.generate('py', 'xml', '../test/gen_xml_py/')
    gen.generate('py', 'json', '../test/gen_json_py/')
    gen.generate('cpp', 'xml', '../test/gen_xml_cpp/')
    gen.generate('cpp', 'json', '../test/gen_json_cpp/')
    gen.generate('php', 'xml', '../test/gen_xml_php/')
    gen.generate('php', 'json', '../test/gen_json_php/')

    gen.generate_data('../simple_test/data_xml', '../test/assets', 'xml')
    gen.generate_data('../simple_test/data_xml', '../test/assets', 'json')

if __name__ == '__main__':
    main()
    # test()
    # test_game_s()
