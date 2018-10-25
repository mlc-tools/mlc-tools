

class GeneratorPackage:

    def __init__(self):
        pass

    def generate(self, parser, writer):
        writer.save_file('__init__.py', '')
