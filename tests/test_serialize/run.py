import os
import shutil
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.abspath(currentdir + '/../../')
sys.path.insert(0, parentdir)

from mlc_tools import Generator

root = os.path.dirname(os.path.abspath(__file__)) + '/..'


def execute(command):
    res = os.system(command)
    return res


def generate(lang, protocol):
    global root
    test_dir = root + '/test_serialize/'
    generator = Generator(configs_directory=test_dir, side='client', disable_logs='no', generate_tests='no', generate_intrusive='yes')
    generator.generate(lang, protocol, test_dir + 'generated_%s' % lang)


def clean():
    def rem(path):
        path = '{}/{}'.format(root, path)
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

    rem('test_serialize/data.py.xml')
    rem('test_serialize/data.php.xml')
    rem('test_serialize/data.cpp.xml')
    rem('test_serialize/data.py.json')
    rem('test_serialize/data.php.json')
    rem('test_serialize/data.cpp.json')
    rem('test_serialize/step_2')


def run(protocol):
    clean()
    generate('py', protocol)
    generate('php', protocol)
    generate('cpp', protocol)
    python = 'python3' if sys.version_info[0] == 3 else 'python'
    result = True
    result = result and 0 == execute('cd {0}/test_serialize; {1} step_0.py'.format(root, python))
    result = result and 0 == execute('cd {0}/test_serialize; php step_1.php'.format(root))
    result = result and 0 == execute('cd {0}/test_serialize; mkdir build_{1}; cd build_{1}; cmake ..; make -j8 install'.format(root, protocol))
    result = result and 0 == execute('cd {0}/test_serialize; mkdir build_{1}; ./step_2'.format(root, protocol, python))
    result = result and 0 == execute('cd {0}/test_serialize; {1} step_3.py;'.format(root, python))
    if not result:
        clean()
        print('Error')
        exit(1)

    clean()

if __name__ == '__main__':
    run('xml')
    run('json')
