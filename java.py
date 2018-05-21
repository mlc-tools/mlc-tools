from mlc_tools.main import Generator


def test_game_s():
    game_root = 'tests/java/'
    generator = Generator(game_root + 'config', generate_tests='no')
    generator.generate('java', 'xml', game_root + 'gen/org/mlc_tools/mg/', 'client', gen_data_storage=False)


if __name__ == '__main__':
    test_game_s()
