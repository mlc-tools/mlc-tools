from ..base.model import SerializeFormat


class GeneratorConfig(object):

    def __init__(self):
        pass

    @staticmethod
    def generate(model):
        content = ''
        filename = 'config.js'

        for serialize_format, format_string in SerializeFormat.get_all():
            support = 'true' if model.serialize_formats & serialize_format != 0 else 'false'
            line = '\nconst SUPPORT_{}_PROTOCOL = {};'.format(format_string.upper(), support)
            content += line
        content += '\n'
        for serialize_format, format_string in SerializeFormat.get_all():
            line = '\nexports.SUPPORT_{0}_PROTOCOL = SUPPORT_{0}_PROTOCOL;'.format(format_string.upper())
            content += line

        model.add_file(None, filename, content)
