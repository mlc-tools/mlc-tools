import os
import inspect
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from mlc_tools import Mlc


def get_root():
    return os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/..')


def run_tests(generator, root, withdata=False, cpp=True, python=True, php=True):
    def run(lang, serialized_format):
        out_directory = root + 'generated_%s' % (lang if lang != 'cpp' else lang + '/' + serialized_format)
        generator.generate(language=lang,
                           out_directory=out_directory
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
        # run('cpp', 'json')
        run('cpp', 'xml')
    if python:
        # run('py', 'json')
        run('py', 'xml')
    if php:
        # run('php', 'json')
        run('php', 'xml')


def simple_test():
    root = get_root() + '/tests/simple_test/'
    generator = Mlc(configs_directory=root + 'config',
                    side='client',
                    disable_logs=False,
                    generate_tests=True,
                    generate_intrusive=True,
                    generate_factory=True)
    generator.add_config_directories(root + 'config_additional')
    generator.add_data_directories(root + 'data_additional')
    run_tests(generator, root, True)


def test_functions():
    root = get_root() + '/tests/test_functions/'
    generator = Mlc(configs_directory=root + 'config', generate_intrusive=True, generate_factory=True)
    run_tests(generator, root)


def test_database():
    root = get_root() + '/tests/test_database/'
    generator = Mlc(configs_directory=root + 'config',
                    generate_intrusive=True,
                    generate_factory=True,
                    generate_tests=True)
    run_tests(generator, root)


def test_serialize():
    root = get_root()
    python = 'python3' if sys.version_info[0] == 3 else 'python'
    command = '{} {}/tests/test_serialize/run.py'.format(python, root)
    result = os.system(command)
    if 0 != result:
        exit(1)


def unit_tests_generator():
    root = get_root() + '/tests/unit_tests_generator/'
    generator = Mlc(configs_directory=root, generate_intrusive=True, generate_factory=True, generate_tests=True)
    run_tests(generator, root)


def test_virtual_methods():
    root = get_root() + '/tests/test_virtual_methods/'
    generator = Mlc(configs_directory=root, generate_intrusive=True, generate_factory=True, generate_tests=True)
    run_tests(generator, root, python=False, php=False)


if __name__ == '__main__':
    simple_test()
    test_serialize()
    test_functions()
    unit_tests_generator()
    test_virtual_methods()

    # Dont run this test in CI
    # test_database()
