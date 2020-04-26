import time


def run():
    start = time.time()
    from mlc_tools.mlc_tools import Mlc

    project_root = '/Users/vladimirtolmachev/work/dungeon'
    out = '/Users/vladimirtolmachev/work/mlc-tools/temp'

    generator = Mlc(configs_directory=project_root + '/configs', generate_intrusive=False, generate_factory=True)
    generator.generate(language='cpp', out_directory=out + '/client/generated/mg', side='client', generate_tests=True)
    generator.generate(language='py', out_directory=out + '/server_web/mg', side='client', generate_tests=True)

    finish = time.time()
    print('Elapsed: ', finish-start)
    return finish-start


if __name__ == '__main__':
    """
    Minimal on 0 iteration (cpp+py): 2.255
    Minimal on 0 iteration (cpp):    0.978
    Minimal on 0 iteration (py):     1.259
    
    Iteration 1:
        skip translate methods if file with class not changed
    Minimal on 1 iteration (cpp+py): 1.600 (70%)
    Minimal on 1 iteration (cpp):    0.808 (83%)
    Minimal on 1 iteration (py):     0.785 (62%)
    """

    t = 1000.0
    t = min(t, run())
    t = min(t, run())
    t = min(t, run())
    t = min(t, run())
    t = min(t, run())
    t = min(t, run())
    t = min(t, run())
    t = min(t, run())
    t = min(t, run())
    t = min(t, run())
    print('Min: ', t)
