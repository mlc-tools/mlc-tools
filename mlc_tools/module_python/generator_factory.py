from .constants import FACTORY


class GeneratorFactory:

    def __init__(self):
        pass

    @staticmethod
    def generate(model, writer):
        line = '''
        if type == "{0}":
            from . import {0}
            return {0}.{0}()'''
        builders = ''
        for cls in model.classes:
            builders += line.format(cls.name)
        content = FACTORY.format(builders=builders)
        writer.save_file('Factory.py', content)
