from .cpp_extension import FILES_DICT
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
        self.generate_config_files(model)
        for pair in FILES_DICT:
            filename = pair[0]
            if 'intrusive_ptr' in filename and not model.generate_intrusive:
                continue
            if 'Factory' in filename and not model.generate_factory:
                continue
            content = pair[1]
            content = content.replace('@{namespace}', self.get_namespace())
            content = content.replace('@{namespace_upper}', self.get_namespace().upper())
            content = writer.prepare_file(content)
            filename = filename.replace('@{namespace}', self.get_namespace())
            model.add_file(filename, content)

    def generate_config_files(self, model):
        pattern = '#ifndef __{0}_Config_h__\n#define __{0}_Config_h__\n\n{1}\n\n#endif //#ifndef __{0}_Config_h__'
        configs = list()

        for serialize_format, format_string in SerializeFormat.get_all():
            support = 'true' if model.serialize_formats & serialize_format != 0 else 'false'
            configs.append('#define SUPPORT_{}_PROTOCOL {}'.format(format_string.upper(), support))

        model.add_file('config.h', pattern.format(self.get_namespace(), '\n'.join(configs)))
