from .constants import FACTORY
from .writer import Writer


class GeneratorFactory(object):

    def __init__(self):
        pass

    @staticmethod
    def generate(model):
        writer = Writer('')
        writer.model = model
        content = writer.prepare_file(FACTORY)
        model.add_file(None, 'Factory.js', content)
