import os
import subprocess
from mlc_tools import Generator


def simple_test():
    generator = Generator(configs_directory='simple_test/config', side='client', disable_logs='yes')

    def run(lang, format):
        generator.generate(lang, format, 'simple_test/generated_%s' % (lang if lang != 'cpp' else lang + '/' + format))
        generator.generate_data('simple_test/data_%s/' % format, 'simple_test/assets')
        generator.run_test('simple_test/test_%s.py' % lang, format)
        print '-----------------------------------------'
        print '|  test with params [{}, {}] finished'.format(lang, format)
        print '-----------------------------------------'

    run('py', 'json')
    run('py', 'xml')
    run('cpp', 'json')
    run('cpp', 'xml')
    run('php', 'json')
    run('php', 'xml')


def test_serialize():

    def execute(command):
        p = subprocess.Popen(command, shell=True)
        (output, err) = p.communicate()
        p.wait()
        return 0 if err is None else err

    root = os.path.dirname(os.path.abspath(__file__)) + ''
    command = 'python {}/test_serialize/run.py'.format(root)
    if 0 != execute(command):
        exit(1)


if __name__ == '__main__':
    simple_test()
    test_serialize()
