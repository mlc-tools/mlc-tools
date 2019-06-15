from ..base.save_plugin_base import SavePluginBase


class SavePlugin(SavePluginBase):

    def __init__(self, model):
        SavePluginBase.__init__(self, model)

    def save_files(self, combine_to_one=True):
        SavePluginBase.save_files(self, True)

    def _create_combine_file_header(self):
        header = ''
        file_name = 'mg.js'
        return header, file_name

    def _finalize_combine_file(self, content):
        return content

    def _remove_includes(self, file_content):
        return file_content
