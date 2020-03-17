from .writer import Writer
from .constants import FACTORY


class GeneratorFactory(object):
    def __init__(self):
        pass

    @staticmethod
    def generate(model):
        writer = Writer('')
        writer.model = model
        content = writer.prepare_file(FACTORY)
        model.add_file(None, 'Factory.php', content)

