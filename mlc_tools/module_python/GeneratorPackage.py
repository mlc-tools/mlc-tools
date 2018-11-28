

class GeneratorPackage:

    def __init__(self):
        pass

    @staticmethod
    def generate(model, writer):
        writer.save_file('__init__.py', '')
