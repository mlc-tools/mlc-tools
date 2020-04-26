import os
import json

from mlc_tools.utils import fileutils


class Cache(object):

    def __init__(self, model):
        from mlc_tools.base.model import Model
        self.model: Model = model
        self.data = {}
        self.configuration = ''

    def load(self):
        path = self._get_path()
        if os.path.isfile(path):
            self._load(path)

        prev = self.data.get('configuration', 'None')
        curr = self._build_configuration()
        if prev != curr:
            self.data = {}

    def save(self):
        path = self._get_path()
        self.data['configuration'] = self._build_configuration()
        self._save(path)

    def _get_path(self):
        return '{}/.mlc.{}.cache'.format(self.model.configs_directory, self.model.language)

    def is_file_changed(self, path: str):
        if path not in self.data:
            self.data[path] = 0
        parse_time = self.data[path]
        change_time = fileutils.get_change_time_of_file(path)
        return parse_time < change_time or change_time == 0

    def mark_parse_time(self, path: str):
        self.data[path] = fileutils.get_change_time_of_file(path)

    def _load(self, path_to_cache_file: str):
        with open(path_to_cache_file) as out:
            self.data = json.load(out)

    def _save(self, path_to_cache_file: str):
        content = json.dumps(self.data)
        fileutils.write(path_to_cache_file, content)

    def _build_configuration(self):
        string = '{formats}.{join}.'
        return string.format(formats=self.model.serialize_formats,
                             join=self.model.join_to_one_file,
                             )
