from .. import fileutils


class WriterBase:
    def __init__(self, out_directory):
        self.out_directory = out_directory
        self.files = []
        
    def save_file(self, filename, content):
        full_path = fileutils.normalize_path(self.out_directory) + filename
        fileutils.write(full_path, content)
        
    def save(self, parser):
        pass
