

class GeneratorPackage:

    def __init__(self):
        pass

    @staticmethod
    def generate(parser, writer):
        writer.save_file('__init__.py', '')
