from ..base.model import SerializeFormat


class GeneratorConfig(object):

    def __init__(self):
        pass

    @staticmethod
    def generate(model):
        content = ''
        filename = 'config.php'

        for serialize_format, format_string in SerializeFormat.get_all():
            support = 'true' if model.serialize_formats & serialize_format != 0 else 'false'
            line = '\n\tpublic static $SUPPORT_{}_PROTOCOL = {};'.format(format_string.upper(), support)
            content += line
        content = CONTENT.format(content)
        model.add_file(filename, content)


CONTENT = '''<?php

class Config {{{0}
}};

?>'''
