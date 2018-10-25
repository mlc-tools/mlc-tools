from ..utils import fileutils


class WriterBase:

    def __init__(self, out_directory):
        self.parser = None
        self.out_directory = out_directory
        self.files = []

    def save_file(self, filename, content):
        full_path = fileutils.normalize_path(self.out_directory) + filename
        fileutils.write(full_path, content)

    def save(self, parser):
        self.parser = parser
        for cls in parser.classes:
            sources = self.write_class(cls)
            for filename, content in sources:
                self.save_file(filename, content)

    def write_class(self, cls):
        return [('', '')]
