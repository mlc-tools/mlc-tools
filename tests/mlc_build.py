import os
import inspect
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from mlc_tools import Generator


def get_root():
    return os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/..')


def run_tests(generator, root, withdata=False):
    def run(lang, format):
        generator.generate(lang, format, root + 'generated_%s' % (lang if lang != 'cpp' else lang + '/' + format))
        if withdata:
            generator.generate_data(root + 'data_%s/' % format, root + 'assets')
        generator.run_test(root + 'test_%s.py' % lang, format)
        print('-----------------------------------------')
        print('|  test with params [{}, {}] finished'.format(lang, format))
        print('-----------------------------------------')

    run('cpp', 'json')
    run('cpp', 'xml')
    run('py', 'json')
    run('py', 'xml')
    run('php', 'json')
    run('php', 'xml')


def simple_test():
    root = get_root() + '/tests/simple_test/'
    generator = Generator(configs_directory=root + 'config', side='client', disable_logs=False,
                          generate_tests=True, generate_intrusive=True, generate_factory=True)
    run_tests(generator, root, True)


def test_functions():
    root = get_root() + '/tests/test_functions/'
    generator = Generator(configs_directory=root + 'config', generate_intrusive=True, generate_factory=True)
    run_tests(generator, root)


def test_database():
    root = get_root() + '/tests/test_database/'
    generator = Generator(configs_directory=root + 'config', generate_intrusive=True, generate_factory=True, generate_tests=True)
    run_tests(generator, root)


def test_serialize():

    def execute(command):
        p = os.system(command)
        return p

    root = get_root()
    python = 'python3' if sys.version_info[0] == 3 else 'python'
    command = '{} {}/tests/test_serialize/run.py'.format(python, root)
    result = execute(command)
    if 0 != result:
        exit(1)


if __name__ == '__main__':
    simple_test()
    test_serialize()
    test_functions()
    # Dont run this test in CI
    # test_database()
