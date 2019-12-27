import os
import shutil


def usage():
    result = True
    result = result and os.system(f'PYTHONPATH=../../ python3 ../../mlc_tools/console/console.py') == 0
    result = result and os.system(f'PYTHONPATH=../../ python3 ../../mlc_tools/console/console.py help') == 0
    result = result and os.system(f'PYTHONPATH=../../ python3 ../../mlc_tools/console/console.py -h') == 0
    result = result and os.system(f'PYTHONPATH=../../ python3 ../../mlc_tools/console/console.py --help') == 0
    if not result:
        print('usage: Failed')
    return result


def init():
    app = 'test_app'
    if os.path.isdir(f'{app}'):
        shutil.rmtree(f'{app}')
    result = True
    result = result and os.system(f'PYTHONPATH=../../ python3 ../../mlc_tools/console/console.py init {app}') == 0
    result = result and os.path.isdir(f'{app}')
    result = result and os.path.isdir(f'{app}/src')
    result = result and os.path.isfile(f'{app}/project.yaml')
    result = result and os.path.isfile(f'{app}/src/main.mlc')
    if not result:
        print('init: Failed')
    return result


def clean_empty():
    app = 'test_app'
    result = True
    result = result and os.path.isdir(f'{app}')
    result = result and not os.path.isdir(f'{app}/build')
    result = result and os.system(f'cd {app}; PYTHONPATH=../../../ python3 ../../../mlc_tools/console/console.py clean') == 0
    result = result and not os.path.isdir(f'{app}/build')
    if not result:
        print('clean_empty: Failed')
    return result


def build():
    app = 'test_app'
    result = True
    result = result and os.path.isdir(f'{app}')

    result = result and os.system(f'cd {app}; PYTHONPATH=../../../ python3 ../../../mlc_tools/console/console.py build --verbose') == 0
    result = result and os.path.isdir(f'{app}/build')
    result = result and os.path.isdir(f'{app}/build/debug')
    result = result and os.path.isfile(f'{app}/build/debug/{app}')

    result = result and os.system(f'cd {app}; PYTHONPATH=../../../ python3 ../../../mlc_tools/console/console.py build --mode debug --verbose') == 0
    result = result and os.path.isdir(f'{app}/build')
    result = result and os.path.isdir(f'{app}/build/debug')
    result = result and os.path.isfile(f'{app}/build/debug/{app}')

    result = result and os.system(f'cd {app}; PYTHONPATH=../../../ python3 ../../../mlc_tools/console/console.py build --mode release --verbose') == 0
    result = result and os.path.isdir(f'{app}/build')
    result = result and os.path.isdir(f'{app}/build/release')
    result = result and os.path.isfile(f'{app}/build/release/{app}')
    if not result:
        print('build: Failed')
    return result


def run():
    app = 'test_app'
    result = True
    result = result and os.path.isdir(f'{app}')
    result = result and not os.path.isdir(f'{app}/build/debug/{app}')
    result = result and not os.path.isdir(f'{app}/build/release/{app}')
    result = result and os.system(f'cd {app}; PYTHONPATH=../../../ python3 ../../../mlc_tools/console/console.py run') == 0
    result = result and os.system(f'cd {app}; PYTHONPATH=../../../ python3 ../../../mlc_tools/console/console.py run --mode debug') == 0
    result = result and os.system(f'cd {app}; PYTHONPATH=../../../ python3 ../../../mlc_tools/console/console.py run --mode release') == 0
    if not result:
        print('run: Failed')
    return result


def clean_after_build():
    app = 'test_app'
    result = True
    result = result and os.path.isdir(f'{app}')
    result = result and os.path.isdir(f'{app}/build')
    result = result and os.path.isdir(f'{app}/build/debug')
    result = result and os.path.isdir(f'{app}/build/release')
    result = result and os.system(f'cd {app}; PYTHONPATH=../../../ python3 ../../../mlc_tools/console/console.py clean') == 0
    result = result and not os.path.isdir(f'{app}/build/debug')
    result = result and os.system(f'cd {app}; PYTHONPATH=../../../ python3 ../../../mlc_tools/console/console.py clean --mode release') == 0
    result = result and not os.path.isdir(f'{app}/build/release')
    if not result:
        print('clean_after_build: Failed')
    return result


def main():
    result = True
    result = result and usage()
    result = result and init()
    result = result and clean_empty()
    result = result and build()
    result = result and run()
    result = result and clean_after_build()
    print(result)
    if not result:
        exit(1)


if __name__ == '__main__':
    main()
