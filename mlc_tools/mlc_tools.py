from .Error import Log
from .Parser import Parser
from . import fileutils
from .Generator_ import Generator
from .Linker import Linker
from .Validator import Validator


class Mlc:
    def __init__(self, **kwargs):
        self.configs_directory = ''
        self.out_directory = ''
        self.data_directory = ''
        self.out_data_directory = ''
        self.language = 'py'
        self.serialize_format = 'xml'
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
        self.serialize_format = kwargs.get('serialize_format', self.serialize_format)
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
        
        parser = Parser(self.side)
        all_files = get_config_files()
        parser.parse_files(all_files)

        generator = Generator()
        generator.generate_tests_interfaces(parser)
        generator.generate_acceptor_interfaces(parser)
        
        linker = Linker()
        linker.link(parser)

        validator = Validator()
        validator.validate(parser)

        language = self.build_language()
        # cpp
        # php
        language.get_generator().generate_data_storage(parser)
        language.get_generator().generate_factory(parser, language.get_writer())
        language.get_generator().generate_init_files(parser, language.get_writer())
        language.get_translator().translate(parser)
        # python
        language.get_serializer().generate_methods(parser)
        language.get_writer().save(parser)
        
    def build_language(self):
        if self.language == 'py':
            from .python import Language
            language = Language(self.out_directory)
            return language
        return None
            

    def run_user_generator(self, state):
        if self.custom_generator:
            self.custom_generator.execute(state)
