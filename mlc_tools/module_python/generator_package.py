from ..base.model import SerializeFormat


class GeneratorPackage(object):

    def __init__(self):
        pass

    @staticmethod
    def generate(model):
        content = ''
        filename = '__init__.py'

        for serialize_format, format_string in SerializeFormat.get_all():
            support = True if model.serialize_formats & serialize_format else False
            content += '\n    SUPPORT_{}_PROTOCOL = {}'.format(format_string.upper(), support)
        content = CONTENT.format(content)
        model.add_file(filename, content)


CONTENT = '''

class Config:{0}

    def __init__(self):
        pass
'''
