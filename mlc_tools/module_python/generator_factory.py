from .constants import FACTORY
from .writer import Writer


class GeneratorFactory(object):

    def __init__(self):
        pass

    @staticmethod
    def generate(model):
        writer = Writer('')
        writer.model = model
        line = '''
        if type == "{0}":
            from . import {0}
            return {0}.{0}()'''
        builders = ''
        for cls in model.classes:
            builders += line.format(cls.name)
        content = FACTORY.format(builders=builders)
        content = writer.prepare_file(content)
        model.add_file('Factory.py', content)
