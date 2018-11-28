from mlc_tools.mlc_tools import Mlc
#
#
# def test_game_s():
#     game_root = '/Work/survival/'
#     generator = Generator(game_root + 'config', generate_tests='yes')
#     generator.generate('py', 'json', game_root + 'tests/python/web', 'client')
#     generator.generate('cpp', 'json', game_root + 'tests/cpp/web', 'client', generate_intrusive='yes')
#     generator.generate('cpp', 'json', game_root + 'client/generated/web', 'client')
#     generator.generate_data(game_root + '/config/data', game_root + '/tests/data')
#
#
def test_game_m():
    project_root = '/Work/gushchin/marines/'
    generator = Mlc()
    generator.generate(language='cpp',
                       configs_directory=project_root + 'config',
                       out_directory=project_root + 'client/project_marines/generated/web',
                       # out_directory=project_root + 'tests/unit_tests/cpp/generated',
                       side='client'
                       )
    # generator.generate('php', 'xml', project_root + '/server/mg', 'server')
    # generator.generate('py', 'xml', project_root + '/tests/server/lib/mg', 'client')
    # generator.generate('py', 'xml', project_root + '/tests/server/lib/mg_server', 'server')
    # tests
    
    
def test_game_m_py():
    project_root = '/Work/gushchin/marines/'
    generator = Mlc()
    generator.generate(language='py',
                       configs_directory=project_root + 'config',
                       out_directory=project_root + '/tests/server/lib/mg',
                       side='client')
    
    
def test_game_m_php():
    project_root = '/Work/gushchin/marines/'
    generator = Mlc()
    generator.generate(language='php',
                       configs_directory=project_root + 'config',
                       out_directory=project_root + '/server/mg',
                       side='server')


def get_profile_(function):
    """ Returns performance statistics (as a string) for the given function.
    """
    def _run():
        function()
    import cProfile as profile
    import pstats
    import os
    import sys
    sys.modules['__main__'].__profile_run__ = _run
    id = function.__name__ + '()'
    profile.run('__profile_run__()', id)
    p = pstats.Stats(id)
    p.stream = open(id, 'w')
    p.sort_stats('time').print_stats(20)
    p.stream.close()
    s = open(id).read()
    os.remove(id)
    return s


print(get_profile_(test_game_m))
# print(get_profile_(test_game_m_py))
# print(get_profile_(test_game_m_php))
