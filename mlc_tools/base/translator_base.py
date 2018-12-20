

class TranslatorBase(object):

    def __init__(self):
        pass

    def translate(self, model):
        for cls in model.classes:
            if cls.type == 'enum':
                self.convert_to_enum(cls)
            for method in cls.functions:
                self.translate_function(cls, method, model)

    def translate_function(self, cls, method, model):
        pass

    def convert_to_enum(self, cls):
        pass
