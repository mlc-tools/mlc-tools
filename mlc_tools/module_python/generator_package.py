

class GeneratorPackage(object):

    def __init__(self):
        pass

    @staticmethod
    def generate(writer):
        writer.save_file('__init__.py', '')
