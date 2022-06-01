import sys


class ArgumentsError(RuntimeError):

    def __init__(self, message):
        RuntimeError.__init__(self, message)


class Arguments:
    def __init__(self):
        self.command = 'help'
        self.project_name = 'mlc_app'
        self.mode = 'debug'
        self.config = 'project.yaml'
        self.verbose = False
        self.bin = True
        self.lib = False

    def parse(self):
        args = sys.argv[1:]
        if args:
            self.set_command(args[0])

        self.set_option('mode')
        self.set_option('config')
        self.set_flag('verbose')
        self.set_flag('bin')
        self.set_flag('lib')
        if self.bin == self.lib:
            if self.bin and self.lib:
                raise ArgumentsError('Cannot define binary type')
            else:
                self.bin = True

    def print_usage(self):
        print('Usage')
        print('')
        print('  mlc help, --help, -h            - Print usage information and exit')
        print('  mlc version, --version, -v      - Print version')
        print('  mlc init <app-name> [options]   - Initialize new app')
        print('  mlc generate [options]          - Generate sources')
        print('  mlc build [options]             - Build app')
        print('  mlc run [options]               - Build and run app')
        print('  mlc clean [options]             - Clean')
        print('')
        print('Options:')
        print('')
        options = list()
        options.append(self.build_option('mode', '<values> :-: Build mode. Default is debug'))
        options.append(self.build_option('config',
                                         ' <path-to-yaml-file>:-: Path to specific config file. Default is project.yaml'))
        options.append(self.build_flag('bin', ':-: Create a package with a binary target. This is the default behavior'))
        options.append(self.build_flag('lib', ':-: Create a package with a library target'))
        options.append(self.build_flag('verbose', ':-: Show logs on build'))

        spaces = 0
        for option in options:
            pos = option.find(':-:')
            spaces = max(spaces, pos)
        for option in options:
            pos = option.find(':-:')
            tab = ' ' * (spaces - pos + 4)
            option = option.replace(':-:', f'{tab}=')
            print(option)

    def build_option(self, option, description):
        values = self._get_option_values(option)
        if values:
            values = str(values)[1:-1].replace("'", '')
        description = description.replace('<values>', f' <{values}>')
        return f'  --{option}{description}'

    @staticmethod
    def build_flag(option, description):
        return f'  --{option}{description}'

    def set_command(self, command):
        valid = [
            'init',
            'clean',
            'run',
            'generate',
            'build',
            'help', '--help', '-h',
            'version', '--version', '-v',
        ]
        if command not in valid:
            raise ArgumentsError('Unknown command: ' + command)
        self.command = command

        if self.command == 'init':
            if len(sys.argv) < 3:
                raise ArgumentsError('Error:\n  - mlc init [name]. Parameter name is skipped')
            self.project_name = sys.argv[2]
        if self.command in ['--help', '-h']:
            self.command = 'help'
        if self.command in ['--version', '-v']:
            self.command = 'help'

    def set_option(self, option):
        arg = '--' + option
        if arg not in sys.argv:
            return
        index = sys.argv.index(arg)
        if index > len(sys.argv) - 2:
            raise ArgumentsError('Error parse option: ' + arg)

        value = sys.argv[index + 1]
        self._validate_option(option, value)
        self.__setattr__(option, value)

    def set_flag(self, flag):
        arg = '--' + flag
        value = arg in sys.argv
        self._validate_flag(flag, value)
        self.__setattr__(flag, value)

    @staticmethod
    def _get_option_values(option):
        options = {
            'mode': ['debug', 'release'],
            'config': None,
        }
        if option not in options:
            raise ArgumentsError(f'Unknown option on validate: {option}')
        return options[option]

    def _validate_option(self, option, value):
        if self.__getattribute__(option) is None:
            raise ArgumentsError('Unknown option: ' + option)

        values = self._get_option_values(option)
        if values is not None and value not in values:
            raise ArgumentsError(f'Incorrect value of option: --{option} {value}. Can be one of {values}')

    def _validate_flag(self, flag, value):
        if self.__getattribute__(flag) is None:
            raise ArgumentsError(f'Unknown flag: --{flag}')
        if not isinstance(value, bool):
            raise ArgumentsError(f'Incorrect value of option: --{flag} {value}. Should be bool')
