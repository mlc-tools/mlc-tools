from os.path import isfile
import yaml
from mlc_tools.utils.fileutils import normalize_path


class Feature(object):
    GENERATE_TESTS = 'tests'
    INTRUSIVE_PTR = 'intrusive_ptr'
    FACTORY = 'factory'
    PHP_VALIDATE = 'php_validate'
    AUTO_REGISTRATION = 'auto_registration'


class ProjectConfig(object):
    def __init__(self):
        self.has_config = False
        self.root = None
        self.arguments = None
        self.name = None
        self.binary_type = 'app'
        self.serialize_format = None
        self.src_directory = None
        self.src_directory_add = None
        self.data_directory = None
        self.build_directory = None
        self.third_party_source_url = None
        self.third_party_release = None
        self.generate_sources_directory = None
        self.lang = None
        self.serialize_format = None
        self.set_defaults('')
        self.features = {}

    def set_defaults(self, root, arguments=None):
        self.root = root
        self.arguments = arguments
        self.name = 'app'
        self.serialize_format = 'xml'
        self.src_directory = normalize_path(root + 'src')
        self.data_directory = normalize_path(root + 'data')
        self.build_directory = normalize_path(root + 'build/' + arguments.mode if arguments else 'debug')
        self.generate_sources_directory = normalize_path(self.build_directory + 'gen')
        self.third_party_source_url = 'https://github.com/mlc-tools/third_party.git'
        self.third_party_release = 'master'
        self.lang = 'cpp'
        self.serialize_format = 'xml'
        self.features = {}

    def parse(self, root, arguments):
        self.set_defaults(root, arguments)
        root = normalize_path(root)
        config_file = root + arguments.config
        if not isfile(config_file):
            return
        with open(config_file, encoding='utf-8') as stream:
            try:
                data = yaml.safe_load(stream)
                self._parse_dict(data)
            except yaml.YAMLError as exception:
                print(exception)
                raise RuntimeError('Cannot parse project.yaml file')
            self.has_config = True

    def _parse_dict(self, dictionary):
        try:
            self.name = dictionary.get('project')
            self.serialize_format = dictionary.get('serialize_format', self.serialize_format)
            self.binary_type = dictionary.get('binary_type', self.binary_type)
            self.lang = dictionary.get('lang', self.lang)
            if 'src_directory' in dictionary:
                self.src_directory = normalize_path(self.root + dictionary.get('src_directory'))
            if 'src_directory_add' in dictionary:
                self.src_directory_add = normalize_path(self.root + dictionary.get('src_directory_add'))
            if 'data_directory' in dictionary:
                self.data_directory = normalize_path(self.root + dictionary.get('data_directory'))
            if 'build_directory' in dictionary:
                self.build_directory = normalize_path(self.root + dictionary.get('build_directory'))
                self.build_directory += self.arguments.mode if self.arguments else 'debug'
                self.build_directory = normalize_path(self.build_directory)
            if 'generate_sources_directory' in dictionary:
                self.generate_sources_directory = normalize_path(self.root + dictionary.get('generate_sources_directory'))

            if 'features' in dictionary:
                features = dictionary['features']
                features = [x.strip() for x in features.split(' ')]
                for feature in features:
                    self.features[feature] = True

        except KeyError as error:
            print('Project data has not key')
            print(error)
            raise RuntimeError('Cannot parse project data')
        self._validate_values('serialize_format')
        self._validate_values('lang')
        self._validate_values('binary_type')

    def _validate_values(self, name):
        values = {
            'serialize_format': ['xml', 'json'],
            'lang': ['cpp', 'py', 'php', 'js'],
            'binary_type': ['app', 'lib', ''],
        }
        value = self.__getattribute__(name)
        if name in values and value not in values[name]:
            raise RuntimeError(f'Incorrect value of field:\n  {name}: {value}\n  Can be one of {values[name]}')
