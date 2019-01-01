

class GeneratorPackage(object):

    def __init__(self):
        pass

    @staticmethod
    def generate(model):
        model.add_file('__init__.py', '')
