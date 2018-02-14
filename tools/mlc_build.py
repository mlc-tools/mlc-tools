import os


def main(lang, protocol):
    root = os.path.dirname(os.path.abspath(__file__)) + '/..'
    command = '''python {0}/src/main.py
        -i {0}/simple_test/config
        -o {0}/simple_test/generated_{1}
        -data {0}/simple_test/data_{2}
        -data_out {0}/simple_test/assets
        -l {1}
        -f {2}
        -php_validate yes
        -test_script {0}/simple_test/test_{1}.py
        -use_colors no
        -side client
        '''.format(root, lang, protocol)
    command = command.replace('\n', '')
    if 0 != os.system(command):
        exit(1)


if __name__ == '__main__':
    main('cpp', 'json')
