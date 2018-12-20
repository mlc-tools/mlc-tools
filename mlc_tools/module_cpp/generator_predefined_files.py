from .cpp_extension import cpp_files


class GeneratorPredefinedFiles(object):

    def __init__(self):
        pass

    @staticmethod
    def get_namespace():
        return 'mg'

    def generate(self, model, writer):
        self.generate_config_files(writer)
        for pair in cpp_files:
            filename = pair[0]
            if 'intrusive_ptr' in filename and not model.generate_intrusive:
                continue
            if 'Factory' in filename and not model.generate_factory:
                continue
            content = pair[1]
            content = content.replace('@{namespace}', self.get_namespace())
            content = content.replace('@{namespace_upper}', self.get_namespace().upper())
            filename = filename.replace('@{namespace}', self.get_namespace())
            writer.save_file(filename, content)

    def generate_config_files(self, writer):
        pattern = '#ifndef __{0}_Config_h__\n#define __{0}_Config_h__\n\n{1}\n\n#endif //#ifndef __{0}_Config_h__'
        configs = list()
        configs.append('#define {}_JSON 1'.format(self.get_namespace().upper()))
        configs.append('#define {}_XML 2'.format(self.get_namespace().upper()))
        configs.append('\n#define {0}_SERIALIZE_FORMAT {0}_{1}'.format(self.get_namespace().upper(), 'XML'))
        filename_config = '{}_config.h'.format(self.get_namespace())
        writer.save_file(filename_config, pattern.format(self.get_namespace(), '\n'.join(configs)))
