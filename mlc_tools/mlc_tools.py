from .utils.Error import Log
from .utils import fileutils
from .base import Parser
from .base import Linker
from .base import Validator
from .base import DataParser
from .base import Language
from .base.Model import Model
import os
import sys


class Mlc:

    def __init__(self, **kwargs):
        self.model = Model()

        Log.use_colors = kwargs.get('use_colors', False)
        Log.disable_logs = kwargs.get('disable_logs', False)
        self._parse_kwargs(**kwargs)

    def _parse_kwargs(self, **kwargs):
        self.model.configs_directory = kwargs.get('configs_directory', self.model.configs_directory)
        self.model.out_directory = kwargs.get('out_directory', self.model.out_directory)
        self.model.data_directory = kwargs.get('data_directory', self.model.data_directory)
        self.model.out_data_directory = kwargs.get('out_data_directory', self.model.out_data_directory)
        self.model.language = kwargs.get('language', self.model.language)
        self.model.only_data = kwargs.get('only_data', self.model.only_data)
        self.model.namespace = kwargs.get('namespace', self.model.namespace)
        self.model.side = kwargs.get('side', self.model.side)
        self.model.php_validate = kwargs.get('php_validate', self.model.php_validate)
        self.model.test_script = kwargs.get('test_script', self.model.test_script)
        self.model.test_script_args = kwargs.get('test_script_args', self.model.test_script_args)
        self.model.generate_tests = kwargs.get('generate_tests', self.model.generate_tests)
        self.model.generate_intrusive = kwargs.get('generate_intrusive', self.model.generate_intrusive)
        self.model.generate_factory = kwargs.get('generate_factory', self.model.generate_factory)
        self.model.out_directory = fileutils.normalize_path(self.model.out_directory)
        self.model.out_data_directory = fileutils.normalize_path(self.model.out_data_directory)
        if 'add_config' in kwargs:
            self.model.additional_config_directories.append(fileutils.normalize_path(kwargs.get('add_config')))
        if 'add_data' in kwargs:
            self.model.additional_data_directories.append(fileutils.normalize_path(kwargs.get('add_data')))
            
    def add_config_directories(self, directory):
        self.model.additional_config_directories.append(fileutils.normalize_path(directory))

    def add_data_directories(self, directory):
        self.model.additional_data_directories.append(fileutils.normalize_path(directory))

    def generate(self, **kwargs):
        self._parse_kwargs(**kwargs)

        def get_config_files():
            all_directories = [self.model.configs_directory]
            all_directories.extend(self.model.additional_config_directories)
            files = []
            for directory in all_directories:
                directory = fileutils.normalize_path(directory)
                add_files = fileutils.get_files_list(directory)
                add_files = [directory + f for f in add_files]
                files.extend(add_files)

            result_files = []
            for path in files:
                if path.endswith('.mlc'):
                    if self.model.filter_code is not None and not self.model.filter_code(path):
                        continue
                    result_files.append(path)
            return result_files

        self.model.clear_data()

        all_files = get_config_files()
        parser = Parser(self.model)
        parser.parse_files(all_files)
        self.model.parser = parser

        # cpp
        # php
        language = Language(self.model.language, self.model)
        language.get_generator().generate(self.model, language.get_writer())

        Linker().link(self.model)
        Validator().validate(self.model)

        language.get_translator().translate(self.model)
        language.get_serializer().generate_methods(self.model)
        language.get_writer().save(self.model)
        # module_python

    def generate_data(self, **kwargs):
        self._parse_kwargs(**kwargs)

        classes = []
        for class_ in self.model.classes:
            if class_.is_storage:
                classes.append(class_)
        for class_ in self.model.classes_for_data:
            if class_.is_storage:
                classes.append(class_)
        data_parser = DataParser(classes, self.model.data_directory, self.model.filter_data)
        data_parser.parse(self.model.additional_data_directories)
        data_parser.flush(self.model.out_data_directory)

    def run_test(self, **kwargs):
        self._parse_kwargs(**kwargs)

        if self.model.test_script and os.path.isfile(self.model.test_script):
            python = 'python3' if sys.version_info[0] == 3 else 'python'
            command = '{} {} {}'.format(python, self.model.test_script, self.model.test_script_args)
            Log.message('Run test (%s):' % command)
            if os.system(command) != 0:
                print('TODO: exit - 1. mlc_tools.py 1')
                exit(1)
        if not os.path.isfile(self.model.test_script):
            Log.warning('Test script (%s) not founded' % self.model.test_script)

    def run_user_generator(self, state):
        if self.model.custom_generator:
            self.model.custom_generator.execute(state)
