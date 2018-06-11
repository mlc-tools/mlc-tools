import os
import subprocess
import inspect
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from mlc_tools import Generator


def get_root():
    return os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/..')


def simple_test():
    simple_test = get_root() + '/tests/simple_test/'
    generator = Generator(configs_directory=simple_test + 'config', side='client', disable_logs=False,
                          generate_tests=True, generate_intrusive=True, generate_factory=True)

    def run(lang, format):
        generator.generate(lang, format, simple_test + 'generated_%s' % (lang if lang != 'cpp' else lang + '/' + format))
        generator.generate_data(simple_test + 'data_%s/' % format, simple_test + 'assets')
        generator.run_test(simple_test + 'test_%s.py' % lang, format)
        print('-----------------------------------------')
        print('|  test with params [{}, {}] finished'.format(lang, format))
        print('-----------------------------------------')

    run('py', 'json')
    run('py', 'xml')
    run('cpp', 'json')
    run('cpp', 'xml')
    run('php', 'json')
    run('php', 'xml')


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
