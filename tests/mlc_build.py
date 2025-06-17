import os
import sys
import glob
import inspect
import shutil
from time import sleep

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from mlc_tools import Mlc


def get_root():
    return os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/..')


def run_tests(generator, root, withdata=False, cpp=True, python=True, php=True, js=True, with_join=False):
    def run(lang, serialized_format, join_to_one_file=False, clean_out_dir=True):
        out_directory = root + 'generated_%s' % (lang if lang != 'cpp' else lang + '/' + serialized_format)

        # clean python pyc files:
        def clean():
            try:
                shutil.rmtree(out_directory)
            except OSError:
                pass

        if clean_out_dir:
            clean()
        generator.generate(language=lang,
                           out_directory=out_directory,
                           formats=serialized_format,
                           join_to_one_file=join_to_one_file,
                           generate_ref_counter=True,
                           validate_allow_different_virtual_method=True
                           )
        if withdata:
            generator.generate_data(data_directory=root + 'data_%s/' % serialized_format,
                                    out_data_directory=root + 'assets')
        generator.run_test(test_script=root + 'test_%s.py' % lang,
                           test_script_args=serialized_format)
        print('-----------------------------------------')
        print('|  test with params [{}, {}] finished'.format(lang, serialized_format))
        print('-----------------------------------------')

    if cpp:
        generator.model.php_validate = False
        run('cpp', 'json', clean_out_dir=False)
        run('cpp', 'xml', clean_out_dir=False)
    if python:
        generator.model.php_validate = False
        run('py', 'json', False)
        run('py', 'xml', False)
        with_join and run('py', 'json', True)
        with_join and run('py', 'xml', True)
    # if php:
    #     generator.model.php_validate = True
    #     run('php', 'json', False)
    #     run('php', 'xml', False)
    #     with_join and run('php', 'json', True)
    #     with_join and run('php', 'xml', True)
    # if js:
    #     generator.model.php_validate = False
    #     run('js', 'json')


def simple_test():
    root = get_root() + '/tests/simple_test/'
    generator = Mlc(configs_directory=root + 'config',
                    side='server',
                    disable_logs=False,
                    generate_tests=True,
                    generate_intrusive=True,
                    generate_factory=True,
                    auto_registration=False,
                    user_includes=True)
    generator.add_config_directories(root + 'config_additional')
    generator.add_data_directories(root + 'data_additional')
    run_tests(generator, root, True, with_join=True)
    return 0


def test_functions():
    root = get_root() + '/tests/test_functions/'
    generator = Mlc(configs_directory=root + 'config', generate_intrusive=True, generate_factory=True)
    run_tests(generator, root)
    return 0


def test_database():
    root = get_root() + '/tests/test_database/'
    generator = Mlc(configs_directory=root + 'config',
                    generate_intrusive=True,
                    generate_factory=True,
                    generate_tests=True)
    run_tests(generator, root)
    return 0


def test_serialize():
    root = get_root()
    python = 'python3' if sys.version_info[0] == 3 else 'python'
    command = '{} {}/tests/test_serialize/run.py'.format(python, root)
    result = os.system(command)
    if 0 != result:
        sys.exit(1)
    return 0


def unit_tests_generator():
    root = get_root() + '/tests/unit_tests_generator/'
    generator = Mlc(configs_directory=root, generate_intrusive=True, generate_factory=True, generate_tests=True)
    run_tests(generator, root)
    return 0


def test_virtual_methods():
    root = get_root() + '/tests/test_virtual_methods/'
    generator = Mlc(configs_directory=root, generate_intrusive=True, generate_factory=True, generate_tests=True)
    run_tests(generator, root, python=False, php=False)
    return 0


def test_console():
    if sys.version_info[0] == 2:
        return
    python = 'python3'
    command = 'cd {1}/tests/test_console_compile; {0} run.py'.format(python, get_root())
    result = os.system(command)
    if 0 != result:
        sys.exit(1)
    return 0


if __name__ == '__main__':
    if len(sys.argv) == 1:
        simple_test()
        test_serialize()
        test_functions()
        unit_tests_generator()
        test_virtual_methods()
        test_console()
    else:
        exec(sys.argv[1])

    # Dont run this test in CI
    # test_database()
