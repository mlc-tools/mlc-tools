import os
import subprocess

root = os.path.dirname(os.path.abspath(__file__)) + '/..'


def execute(command):
    p = subprocess.Popen(command, shell=True)
    (output, err) = p.communicate()
    p.wait()
    return 0 if err is None else err


def simple_test():
    def run(lang, protocol):
        global root
        out_path_postfix = lang
        if lang == 'cpp':
            out_path_postfix = lang + '/' + protocol
        command = '''python {0}/src/main.py
            -i {0}/simple_test/config
            -o {0}/simple_test/generated_{3}
            -data {0}/simple_test/data_{2}
            -data_out {0}/simple_test/assets
            -l {1}
            -f {2}
            -php_validate yes
            -use_colors no
            -side client
            -test_script {0}/simple_test/test_{1}.py
            -test_script_arg {2}
            -disable_logs yes
            '''.format(root, lang, protocol, out_path_postfix)
        command = command.replace('\n', '')
        if 0 != execute(command):
            exit(1)
        print '-----------------------------------------'
        print '|  test with params [{}, {}] finished'.format(lang, protocol)

    run('py', 'json')
    run('py', 'xml')
    run('cpp', 'json')
    run('cpp', 'xml')
    run('php', 'json')
    run('php', 'xml')


def test_serialize():
    global root

    command = 'python {}/test_serialize/run.py'.format(root)
    if 0 != execute(command):
        exit(1)


if __name__ == '__main__':
    simple_test()
    test_serialize()
