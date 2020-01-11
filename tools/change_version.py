import sys
import subprocess


def change(version):
    print(version)
    open('../mlc_tools/version.py', 'w').write(f'__version__="0.4.{version}"')


def main():
    if len(sys.argv) == 0:
        process = subprocess.Popen(['git', 'rev-list', 'HEAD', '--count'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate(timeout=60)
        if err:
            exit(1)
        version = int(out.decode('utf-8'))
    else:
        version = sys.argv[1]
    change(version)


if __name__ == '__main__':
    main()
