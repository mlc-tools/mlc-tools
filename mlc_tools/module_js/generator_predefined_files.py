from .constants import *
from ..base.writer_base import WriterBase
from ..base.model import Model


class GeneratorPredefinedFiles(object):

    def __init__(self):
        self.model = None

    def generate(self, model: Model):
        self.model = model
        writer = WriterBase('')
        writer.model = model

        for filename, content in FILES.items():
            model.add_file(None, filename, content)


FILES = {
    'common.php': COMMON
}