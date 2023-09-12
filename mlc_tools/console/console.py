import os
import sys
import shutil
from mlc_tools import Mlc, version
from mlc_tools.console.arguments import Arguments, ArgumentsError
from mlc_tools.console.config import ProjectConfig, Feature
from mlc_tools.utils.fileutils import normalize_path, write
from mlc_tools.console.files import *
from mlc_tools.utils.subprocess_wrapper import SubprocessWrapper


class Console(object):
    def __init__(self):
        self.root = ''
        self.arguments = Arguments()
        self.config = ProjectConfig()
        self.generator = None
        self.built = False
        self.build_with_data = False

    def load_project(self, root):
        self.root = normalize_path(os.path.abspath(root))
        if not os.path.isdir(self.root):
            raise RuntimeError("Unknown path: " + self.root)

        self.arguments.parse()
        self.config.parse(self.root, self.arguments)

        SubprocessWrapper.VERBOSE = self.arguments.verbose

        self.built = False
        self.build_with_data = False
        self.generator = None

    def run_action(self):
        action = {
            'init': Console.init,
            'clean': Console.clean,
            'generate': Console.generate,
            'build': Console.build,
            'run': Console.run,
            'help': Console.help,
            'version': Console.version,
        }[self.arguments.command]
        action(self)

    def help(self):
        self.arguments.print_usage()

    def version(self):
        print(f'ml_tools {version}');

    def init(self):
        self._init()

    def clean(self):
        self._check_config()
        self._clean()
        print('Clean successful')

    def generate(self):
        self._check_config()
        self._generate()
        print('Generate successful')

    def build(self):
        print('Build...')
        self._check_config()
        self._generate()
        self._create_cmake()
        self._copy_third_party()
        self._create_main()
        self._build()
        self.built = True
        print('Built successful')

    def run(self):
        self._check_config()
        if not self.built:
            self.build()
        self._run()

    @staticmethod
    def check_dependencies():
        try:
            code, out, err = SubprocessWrapper('cmake --version', require_out=True).call()
        except FileNotFoundError as exception:
            raise RuntimeError('Error: cmake not installed')

        version = out.strip().replace('cmake version ', '')
        version = version.split('.')
        if len(version) < 2 or int(version[0]) < 3 or int(version[1]) < 13:
            raise RuntimeError('Error on check cmake version. Require cmake version 3.13')

    def _init(self):
        project_dir = normalize_path(self.root + self.arguments.project_name)
        if os.path.isdir(project_dir):
            raise RuntimeError('Directory ' + self.arguments.project_name + ' already exist')

        self._init_project_config(project_dir)
        Console._init_create_hello_world(project_dir)
        print('Init successful')

    def _init_project_config(self, project_dir):
        binary_type = 'app' if self.arguments.bin else 'lib'
        content = PROJECT_YAML.format(name=self.arguments.project_name, binary_type=binary_type)
        write(project_dir + 'project.yaml', content)

    @staticmethod
    def _init_create_hello_world(project_dir):
        write(project_dir + 'src/main.mlc', HELLO_WORLD_MLC)

    def _check_config(self):
        if not self.config.has_config:
            raise RuntimeError('Current directory not contain project.yaml file')

    def _clean(self):
        if os.path.isdir(self.config.build_directory):
            shutil.rmtree(self.config.build_directory)

    def _generate(self):
        self.generator = Mlc(configs_directory=self.config.src_directory,
                             data_directory=self.config.data_directory,
                             out_directory=self.config.generate_sources_directory,
                             out_data_directory=self.config.build_directory + 'data',
                             generate_intrusive=self.config.features.get(Feature.INTRUSIVE_PTR, True),
                             generate_factory=self.config.features.get(Feature.FACTORY, True),
                             generate_tests=self.config.features.get(Feature.GENERATE_TESTS, False),
                             language=self.config.lang,
                             php_validate=self.config.features.get(Feature.PHP_VALIDATE, False),
                             join_to_one_file=True,
                             auto_registration=self.config.features.get(Feature.AUTO_REGISTRATION, False),
                             formats=self.config.serialize_format,
                             add_config=self.config.src_directory_add
                             )

        self.generator.generate()
        if os.path.isdir(self.generator.model.data_directory):
            self.build_with_data = True
            self.generator.generate_data()

    def _copy_third_party(self):
        destination = self.config.build_directory + 'external'
        if not os.path.isdir(destination):
            git_clone_command = 'git clone --branch {tag} {url} {path}'.format(
                tag=self.config.third_party_release,
                url=self.config.third_party_source_url,
                path=destination
            )
            process = SubprocessWrapper(git_clone_command)
            if process.call() != 0:
                raise RuntimeError('Error on clone external source from: {}, release: {}'.format(
                    self.config.third_party_source_url, self.config.third_party_release
                ))

    def _create_main(self):
        if self.config.binary_type == 'app':
            content = MAIN_CPP_EXE
            content = content.replace('@{format}', self.config.serialize_format)
            write(self.config.build_directory + 'main.cpp', content)
        else:
            cpp = MAIN_CPP_LIB.replace('@{format}', self.config.serialize_format)
            hpp = MAIN_HPP_LIB
            write(self.config.build_directory + 'mg.cpp', cpp)
            write(self.config.build_directory + 'mg.hpp', hpp)

    def _create_cmake(self):
        content = CMAKE
        if self.config.binary_type == 'app':
            content += CMAKE_APP
        elif self.config.binary_type == 'lib':
            content += CMAKE_LIB

        content = content.replace('@{project_name}', self.config.name)
        content = content.replace('@{gen_dir}', self.config.generate_sources_directory)
        write(self.config.build_directory + 'CMakeLists.txt', content)

    def _build(self):
        mode = {
            'debug': '-DCMAKE_BUILD_TYPE=Debug',
            'release': '-DCMAKE_BUILD_TYPE=Release',
        }[self.arguments.mode]
        options = ''
        if self.build_with_data:
            options += ' -DWITH_DATA=1'
        command = f'cmake -S {self.config.build_directory} -B {self.config.build_directory} {mode}{options}'
        process = SubprocessWrapper(command)
        if process.call() != 0:
            raise RuntimeError('Error on cmake')

        process = SubprocessWrapper(f'make -j4 -C {self.config.build_directory}', require_out=True)
        code, out, err = process.call()
        if code != 0:
            print('----\nmake Out:\n----')
            print(out)
            print('----\nmake Err:\n----')
            print(err)
            print('----\nEnd make log:\n----')
            raise RuntimeError('Error on make')

    def _run(self):
        if not os.path.isfile(f'{self.config.build_directory}/{self.config.name}'):
            raise RuntimeError('Error on run: executable file not found')
        process = SubprocessWrapper(f'./{self.config.name}', self.config.build_directory, require_log=True)
        process.call()
        if process.code != 0:
            raise RuntimeError('Error on run')


def main():
    try:
        Console.check_dependencies()
    except RuntimeError as exception:
        print(exception)
        sys.exit(1)

    console = Console()
    try:
        console.load_project(os.path.curdir)
        console.run_action()
    except ArgumentsError as exception:
        print(exception)
        console.help()
        sys.exit(2)
    except RuntimeError as exception:
        print(exception)
        sys.exit(3)
    sys.exit(0)


if __name__ == '__main__':
    main()
