from ..utils import fileutils
from ..utils.Error import Log


class WriterBase:

    def __init__(self, out_directory):
        self.model = None
        self.out_directory = out_directory
        self.files = []
        self.created_files = []

    def save_file(self, filename, content):
        if self.model is not None and self.model.out_dict is not None:
            self.model.out_dict[filename] = content
            return

        full_path = fileutils.normalize_path(self.out_directory) + filename
        self.created_files.append(filename)
        exist = fileutils.isfile(full_path)
        if fileutils.write(full_path, content):
            msg = ' Create: {}' if not exist else ' Overwriting: {}'
            Log.debug(msg.format(filename))

    def save(self, model):
        self.model = model
        for cls in model.classes:
            sources = self.write_class(cls)
            for filename, content in sources:
                self.save_file(filename, content)

    def write_class(self, cls):
        return [('', '')]

    def set_initial_values(self, cls):
        return ''

    def write_function(self, method):
        return ''

    def write_object(self, obj):
        return ''

    def prepare_file(self, text):
        return text
