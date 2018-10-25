from .constants import FACTORY


class GeneratorFactory:

    def __init__(self):
        pass

    def generate(self, parser, writer):
        line = '''
        if type == "{0}":
            from . import {0}
            return {0}.{0}()'''
        builders = ''
        for cls in parser.classes:
            builders += line.format(cls.name)
        content = FACTORY.format(builders=builders)
        writer.save_file('Factory.py', content)
