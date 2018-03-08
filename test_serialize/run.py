import os
import shutil
import subprocess


root = os.path.dirname(os.path.abspath(__file__)) + '/..'


def execute(command):
    res = os.system(command)
    return res


def generate(lang, protocol):
    global root

    out_path_postfix = lang
    command = '''python {0}/src/main.py
        -i {0}/test_serialize
        -o {0}/test_serialize/generated_{3}
        -l {1}
        -f {2}
        -php_validate yes
        -use_colors no
        -side client
        -disable_logs no
        '''.format(root, lang, protocol, out_path_postfix)
    command = command.replace('\n', '')
    if 0 != execute(command):
        exit(1)


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
    command = '''
        cd {0}/test_serialize;
        python step_0.py;
        php step_1.php;
        mkdir build_{1}; cd build_{1}; cmake ..; make -j8 install; cd ..; ./step_2;
        python step_3.py;
        '''.format(root, protocol)
    command = command.replace('\n', '')
    if 0 != execute(command):
        clean()
        print 'Error'
        exit(1)

    clean()

if __name__ == '__main__':
    run('xml')
    run('json')
