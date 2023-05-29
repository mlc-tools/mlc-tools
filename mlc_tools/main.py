import sys
from .mlc_tools import Mlc


def get_named_arg(name):
    if name not in sys.argv:
        return None
    index = sys.argv.index(name)
    if index + 1 < len(sys.argv):
        value = sys.argv[index + 1]
        if value == 'yes':
            value = True
        if value == 'no':
            value = False
        return value
    return None


def has_flag(name):
    return name in sys.argv


def main():
    args = {}

    def add(name, name2=None):
        if name2 is None:
            name2 = name[1:]
        value = get_named_arg(name)
        if value is not None:
            args[name2] = value

    add('-i', 'configs_directory')
    add('-o', 'out_directory')
    add('-l', 'language')
    add('-f', 'formats')
    add('-j', 'join_to_one_file')
    add('-side')
    add('-data', 'data_directory')
    add('-data_out', 'out_data_directory')
    add('-generate_tests')
    add('-generate_intrusive')
    add('-generate_factory')
    add('-add_config')
    add('-add_data')
    add('-namespace')
    add('-only_data')
    add('-php_validate')
    add('-validate_allow_different_virtual_method')
    add('-test_script')
    add('-test_script_args')
    add('-auto_registration')
    add('-generate_ref_counter')
    add('-user_includes')

    print(args)

    mlc = Mlc(**args)
    mlc.generate()
    if has_flag('-data') and has_flag('-data_out'):
        mlc.generate_data()


if __name__ == '__main__':
    main()
