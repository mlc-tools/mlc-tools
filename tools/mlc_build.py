import os


def main():
    command = '''python {0}/src/main.py
        -i {0}/simple_test/config
        -o {0}/simple_test/generated_php
        -data {0}/simple_test/data_json
        -data_out {0}/simple_test/assets
        -l php
        -f json
        -php_validate yes
        -test_script {0}/simple_test/test_php.py
        -use_colors no
        '''
    command = command.replace('\n', '')
    root = os.path.dirname(os.path.abspath(__file__)) + '/..'
    if 0 != os.system(command.format(root)):
        exit(1)


if __name__ == '__main__':
    main()
