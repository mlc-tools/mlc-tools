import os


def main(lang, protocol):
    root = os.path.dirname(os.path.abspath(__file__)) + '/..'
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
    if 0 != os.system(command):
        exit(1)
    print '-----------------------------------------'
    print '|  test with params [{}, {}] finished'.format(lang, protocol)


if __name__ == '__main__':
    main('py', 'json')
    main('py', 'xml')
    main('cpp', 'json')
    main('cpp', 'xml')
    main('php', 'json')
    main('php', 'xml')
