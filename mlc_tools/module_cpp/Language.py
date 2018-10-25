from .Generator import Generator
from .Translator import Translator
from .Serializer import Serializer
from .Writer import Writer


class Language:

    def __init__(self, out_directory):
        self.generator = Generator()
        self.translator = Translator()
        self.serializer = Serializer()
        self.writer = Writer(out_directory)

    def get_generator(self):
        return self.generator

    def get_translator(self):
        return self.translator

    def get_serializer(self):
        return self.serializer

    def get_writer(self):
        return self.writer
