import os

root = os.path.dirname(os.path.abspath(__file__)) + '/..'


def generate(lang, protocol):
    global root

    out_path_postfix = lang
    if lang == 'cpp':
        out_path_postfix = lang + '/' + protocol
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
    if 0 != os.system(command):
        exit(1)

generate('py', 'xml')
generate('php', 'xml')
generate('cpp', 'xml')

if os.path.isfile('../test_serialize/data.py.xml'):
    os.remove('../test_serialize/data.py.xml')
if os.path.isfile('../test_serialize/data.php.xml'):
    os.remove('../test_serialize/data.php.xml')
if os.path.isfile('../test_serialize/data.cpp.xml'):
    os.remove('../test_serialize/data.cpp.xml')
if os.path.isfile('../test_serialize/step_2'):
    os.remove('../test_serialize/step_2')

command = '''
    cd ../test_serialize;
    python step_0.py;
    php step_1.php;
    cd build; make install; cd ..; ./step_2;
    python step_3.py;
    '''
command = command.replace('\n', '')
if 0 != os.system(command):
    exit(1)
