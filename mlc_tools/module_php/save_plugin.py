import re
from ..base.save_plugin_base import SavePluginBase


class SavePlugin(SavePluginBase):
    def __init__(self, model):
        SavePluginBase.__init__(self, model)

    def _create_combine_file_header(self):
        header = '<?php\n'
        file_name = 'mg.php'
        return header, file_name

    def _finalize_combine_file(self, content):
        return content + '\n?>'

    def _remove_includes(self, file_content):
        file_content = file_content.replace('<?php\n', '')
        file_content = file_content.replace('\n?>', '')
        file_content = re.sub(r'\s*require_once.+', '', file_content)
        return file_content
