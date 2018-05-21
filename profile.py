from mlc_tools.main import Generator


def test_game_s():
    game_root = '/Work/survival/'
    generator = Generator(game_root + 'config', generate_tests='yes')
    generator.generate('py', 'json', game_root + 'tests/python/web', 'client')
    generator.generate('cpp', 'json', game_root + 'tests/cpp/web', 'client')
    generator.generate('cpp', 'json', game_root + 'client/generated/web', 'client')
    generator.generate_data(game_root + '/config/data', game_root + '/tests/data')


def test_game_m():
    game_root = '/work/marines/'
    generator = Generator(game_root + 'config', generate_tests='no')
    generator.generate('cpp', 'xml', game_root + 'client/generated/web', 'client')
    generator.generate('py', 'xml', game_root + 'server/tests/lib/mg', 'client')

    generator = Generator(game_root + 'config_battle', generate_tests='no', namespace='photon')
    generator.generate('cpp', 'json', game_root + 'client/generated/photon', 'client')


def profile():
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
    print get_profile_(test_game_m)

# profile()
test_game_s()
