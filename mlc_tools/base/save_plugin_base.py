import os
from ..utils import fileutils
from ..utils.error import Log


class SavePluginBase(object):

    def __init__(self, model):
        self.model = model
        self.streams = []

    def save_files(self, combine_to_one=True):
        if combine_to_one:
            self.__sort_files()
            self.__save_one()
        else:
            self.__save_all()

        for stream in self.streams:
            stream.close()
        self.__remove_old_files()

    # To override methods:
    def _create_combine_file_header(self):
        return None, None

    def _finalize_combine_file(self, content):
        return content

    def _is_need_save_file_on_combine(self, _):
        return False

    def _remove_includes(self, file_content):
        return file_content

    # Private methods
    def __save_one(self):
        self.__sort_files()

        combine_file, file_path = self._create_combine_file_header()
        for _, local_path, content in self.model.files:
            combine_file = self.__add_to_combine_file(combine_file, content)
            if self._is_need_save_file_on_combine(local_path):
                self.__save_file(local_path, combine_file)

        self.__save_file(file_path, combine_file)

    def __save_all(self):
        if isinstance(self.model.out_dict, dict):
            for _, local_path, content in self.model.files:
                self.model.out_dict[local_path] = content
            return

        for _, local_path, content in self.model.files:
            self.__save_file(local_path, content)

    def __save_file(self, local_path, content):
        self.model.created_files.append(local_path)
        full_path = fileutils.normalize_path(self.model.out_directory) + local_path
        exist = os.path.isfile(full_path)
        result, stream = fileutils.write(full_path, content)
        if result:
            self.streams.append(stream)
            msg = ' Create: {}' if not exist else ' Overwriting: {}'
            Log.message(msg.format(local_path))

    def __sort_files(self):
        def sort_func(data):
            weight = ''
            cls = data[0]
            if cls is None:
                return weight
            weight = cls.name
            while cls.superclasses:
                cls = cls.superclasses[0]
                weight = '~' + weight
            return weight
        self.model.files = sorted(self.model.files, key=sort_func)

    def __add_to_combine_file(self, combine, data):
        combine += self._remove_includes(data)
        return combine

    def __remove_old_files(self):
        files = fileutils.get_files_list(self.model.out_directory)
        for local_path in files:
            if local_path not in self.model.created_files and not local_path.endswith('.pyc'):
                os.remove(self.model.out_directory + local_path)
                Log.debug(' Removed: {}'.format(local_path))
