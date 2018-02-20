import os
import shutil

root = os.path.dirname(os.path.abspath(__file__)) + '/..'


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
        -disable_logs yes
        '''.format(root, lang, protocol, out_path_postfix)
    command = command.replace('\n', '')
    if 0 != os.system(command):
        exit(1)


def clean():
    def rem(file):
        if os.path.isfile(file):
            os.remove(file)
        elif os.path.isdir(file):
            shutil.rmtree(file)

    rem('../test_serialize/data.py.xml')
    rem('../test_serialize/data.php.xml')
    rem('../test_serialize/data.cpp.xml')
    rem('../test_serialize/data.py.json')
    rem('../test_serialize/data.php.json')
    rem('../test_serialize/data.cpp.json')
    rem('../test_serialize/step_2')
    rem('../test_serialize/build')
    rem('../test_serialize/generated_py')
    rem('../test_serialize/generated_php')
    rem('../test_serialize/generated_cpp')


def run(protocol):
    clean()
    generate('py', protocol)
    generate('php', protocol)
    generate('cpp', protocol)
    command = '''
        cd ../test_serialize;
        python step_0.py;
        php step_1.php;
        mkdir build; cd build; cmake ..; make -j8 install; cd ..; ./step_2;
        python step_3.py;
        '''
    command = command.replace('\n', '')
    if 0 != os.system(command):
        clean()
        exit(1)

    clean()

if __name__ == '__main__':
    run('xml')
    run('json')
