from .constants import *
from ..base.writer_base import WriterBase
from ..base.model import SerializeFormat, Model
from ..core.class_ import Class


class GeneratorPredefinedFiles(object):

    def __init__(self):
        self.model = None

    def generate(self, model: Model):
        self.model = model
        writer = WriterBase('')
        writer.model = model

        self.build_common_content()

        for filename, content in FILES.items():
            model.add_file(None, filename, content)

    def build_common_content(self):
        content = COMMON
        xml = ''
        json = ''
        if self.model.serialize_formats & SerializeFormat.xml and self.model.serialize_formats & SerializeFormat.json:
            xml = COMMON_XML
            json = COMMON_JSON + CLONE_JSON
        elif self.model.serialize_formats & SerializeFormat.xml:
            xml = COMMON_XML + CLONE_XML
        elif self.model.serialize_formats & SerializeFormat.json:
            json = COMMON_JSON + CLONE_JSON
        content = content.replace('@{xml}', xml)
        content = content.replace('@{json}', json)
        FILES['common.php'] = content


FILES = {}