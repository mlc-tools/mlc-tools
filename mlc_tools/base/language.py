

class Language(object):

    def __init__(self, module_lang, model):
        from pydoc import locate
        module_name = 'module_%s' % (module_lang if module_lang != 'py' else 'python')

        self.generator = locate('mlc_tools.%s.Generator' % module_name)()
        self.translator = locate('mlc_tools.%s.Translator' % module_name)()
        self.serializer = locate('mlc_tools.%s.Serializer' % module_name)()
        self.writer = locate('mlc_tools.%s.Writer' % module_name)(model.out_directory)
        self.writer.model = model
        self.writer.serializer = self.serializer

    def get_generator(self):
        return self.generator

    def get_translator(self):
        return self.translator

    def get_serializer(self):
        return self.serializer

    def get_writer(self):
        return self.writer
