from .constants import COMMON_XML, COMMON_JSON
from ..base.writer_base import WriterBase
from ..base.model import SerializeFormat, Model
from ..core.class_ import Class
from .constants_serializers import *


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
        content = ''
        if self.model.serialize_formats & SerializeFormat.xml:
            content += COMMON_XML
        if self.model.serialize_formats & SerializeFormat.json:
            content += COMMON_JSON
        FILES['common.py'] = content


FILES = {
    'common.py': '',
    'Meta.py': META,
    'DataWrapper.py': DATA_WRAPPER,
    'IntrusivePtr.py': INTRUSIVE,
    'SerializerXml.py': SERIALIZER_XML,
    'DeserializerXml.py': DESERIALIZER_XML,
    'SerializerJson.py': SERIALIZER_JSON,
    'DeserializerJson.py': DESERIALIZER_JSON,
}