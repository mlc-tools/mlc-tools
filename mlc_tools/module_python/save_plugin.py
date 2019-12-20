import re
from ..base.save_plugin_base import SavePluginBase


class SavePlugin(SavePluginBase):
    def __init__(self, model):
        SavePluginBase.__init__(self, model)

    def _create_combine_file_header(self):
        header = '''# -*- coding: utf-8 -*-
import json
import xml.etree.ElementTree as ET
'''
        file_name = 'mg.py'
        return header, file_name

    def _is_need_save_file_on_combine(self, file_name):
        return file_name == '__init__.py'

    def _remove_includes(self, file_content):
        file_content = re.sub(r'\n\s*from.+import.+', '', file_content)
        file_content = re.sub(r'\n\s*import.+', '', file_content)
        file_content = file_content.replace('# -*- coding: utf-8 -*-\n', '')
        return file_content
