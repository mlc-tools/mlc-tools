from ..core.Object import *


class TranslatorBase:

    def __init__(self):
        pass

    def translate(self, parser):
        for cls in parser.classes:
            if cls.type == 'enum':
                self.convert_to_enum(cls)
            for method in cls.functions:
                self.translate_function(cls, method, parser)
                # print('{}::{}\n{}\n\n'.format(cls.name, method.name, method.body))
    
    def translate_function(self, cls, method, parser):
        pass

    def convert_to_enum(self, cls):
        pass
