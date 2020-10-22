from .constants import FILES_DICT
from ..base.writer_base import WriterBase
from ..base.model import SerializeFormat


class GeneratorPredefinedFiles(object):

    def __init__(self):
        pass

    @staticmethod
    def get_namespace():
        return 'mg'

    def generate(self, model):
        writer = WriterBase('')
        writer.model = model
        for pair in FILES_DICT:
            filename = pair[0]
            content = pair[1]
            content = writer.prepare_file(content)
            model.add_file(None, filename, content)
