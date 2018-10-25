from .utils.Error import Log
from .utils import fileutils
from .base.Parser import Parser
from .base.Linker import Linker
from .base.Validator import Validator
from .base.DataParser import DataParser
import os
import sys
import importlib

class Mlc:
    def __init__(self, **kwargs):
        self.parser = None
        self.configs_directory = ''
        self.out_directory = ''
        self.data_directory = ''
        self.out_data_directory = ''
        self.language = 'py'
        self.only_data = False
        self.namespace = 'mg'
        self.side = 'both'
        self.php_validate = True
        self.test_script = ''
        self.test_script_args = ''
        self.generate_tests = False
        self.generate_intrusive = False
        self.generate_factory = True
        
        self.filter_code = None
        self.filter_data = None
        self.custom_generator = None
        self.additional_config_directories = []
        self.additional_data_directories = []

        Log.use_colors = kwargs.get('use_colors', False)
        Log.disable_logs = kwargs.get('disable_logs', False)
        self._parse_kwargs(**kwargs)
        
    def _parse_kwargs(self, **kwargs):
        self.configs_directory = kwargs.get('configs_directory', self.configs_directory)
        self.out_directory = kwargs.get('out_directory', self.out_directory)
        self.data_directory = kwargs.get('data_directory', self.data_directory)
        self.out_data_directory = kwargs.get('out_data_directory', self.out_data_directory)
        self.language = kwargs.get('language', self.language)
        self.only_data = kwargs.get('only_data', self.only_data)
        self.namespace = kwargs.get('namespace', self.namespace)
        self.side = kwargs.get('side', self.side)
        self.php_validate = kwargs.get('php_validate', self.php_validate)
        self.test_script = kwargs.get('test_script', self.test_script)
        self.test_script_args = kwargs.get('test_script_args', self.test_script_args)
        self.generate_tests = kwargs.get('generate_tests', self.generate_tests)
        self.generate_intrusive = kwargs.get('generate_intrusive', self.generate_intrusive)
        self.generate_factory = kwargs.get('generate_factory', self.generate_factory)
        
        self.out_directory = fileutils.normalize_path(self.out_directory)
        self.out_data_directory = fileutils.normalize_path(self.out_data_directory)
        
    def generate(self, **kwargs):
        self._parse_kwargs(**kwargs)
        
        def get_config_files():
            all_directories = [self.configs_directory]
            all_directories.extend(self.additional_config_directories)
            files = []
            for directory in all_directories:
                directory = fileutils.normalize_path(directory)
                add_files = fileutils.get_files_list(directory)
                add_files = [directory + f for f in add_files]
                files.extend(add_files)
    
            result_files = []
            for path in files:
                if path.endswith('.mlc'):
                    if self.filter_code is not None and not self.filter_code(path):
                        continue
                    result_files.append(path)
            return result_files

        all_files = get_config_files()
        parser = Parser(self.side)
        parser.parse_files(all_files)
        self.parser = parser

        # cpp
        # php
        language = self.build_language()
        language.get_generator().generate(parser, language.get_writer())

        Linker().link(parser)
        Validator().validate(parser)

        language.get_translator().translate(parser)
        language.get_serializer().generate_methods(parser)
        language.get_writer().save(parser)
        # module_python

    def generate_data(self, **kwargs):
        self._parse_kwargs(**kwargs)

        classes = []
        for class_ in self.parser.classes:
            if class_.is_storage:
                classes.append(class_)
        for class_ in self.parser.classes_for_data:
            if class_.is_storage:
                classes.append(class_)
        data_parser = DataParser(classes, self.data_directory, self.filter_data)
        data_parser.parse(self.additional_data_directories)
        data_parser.flush(self.out_data_directory)

    def run_test(self, **kwargs):
        self._parse_kwargs(**kwargs)

        if self.test_script and os.path.isfile(self.test_script):
            python = 'python3' if sys.version_info[0] == 3 else 'python'
            command = '{} {} {}'.format(python, self.test_script, self.test_script_args)
            Log.message('Run test (%s):' % command)
            if os.system(command) != 0:
                print('TODO: exit - 1. mlc_tools.py 1')
                exit(1)
        if not os.path.isfile(self.test_script):
            Log.warning('Test script (%s) not founded' % self.test_script)

    def build_language(self):
        from pydoc import locate
        module_name = 'module_%s' % (self.language if self.language != 'py' else 'python')
        print module_name
        module = locate('mlc_tools.%s.Language' % module_name)
        return module(self.out_directory)
        
    def run_user_generator(self, state):
        if self.custom_generator:
            self.custom_generator.execute(state)
