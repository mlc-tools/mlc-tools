from .constants import COMMON_XML, COMMON_JSON, MG_EXTENSIONS
from .constants_serializers import *
from ..base.writer_base import WriterBase
from ..base.model import SerializeFormat, Model


class GeneratorPredefinedFiles(object):

    def __init__(self):
        self.model = None

    def generate(self, model: Model):
        self.model = model
        writer = WriterBase('')
        writer.model = model

        self.build_common_content()

        # for filename, content in FILES_DICT.items():
        #     model.add_file(None, filename, content)
        for filename, content in FILES_DICT.items():
            content = writer.prepare_file(content)
            model.add_file(None, filename, content)

    def build_common_content(self):
        content = ''
        if self.model.serialize_formats & SerializeFormat.xml:
            content += COMMON_XML
        if self.model.serialize_formats & SerializeFormat.json:
            content += COMMON_JSON
        FILES_DICT['common.py'] = content


FILES_DICT = {
    'common.py': '',
    'mg_extensions.py': MG_EXTENSIONS,
    'Meta.py': META,
    'DataWrapper.py': DATA_WRAPPER,
    'IntrusivePtr.py': INTRUSIVE,
    'SerializerXml.py': SERIALIZER_XML,
    'DeserializerXml.py': DESERIALIZER_XML,
    'SerializerJson.py': SERIALIZER_JSON,
    'DeserializerJson.py': DESERIALIZER_JSON,
}
