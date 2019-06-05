from ..base.save_plugin_base import SavePluginBase


class SavePlugin(SavePluginBase):
    def __init__(self, model):
        SavePluginBase.__init__(self, model)

    def save_files(self, combine_to_one=True):
        SavePluginBase.save_files(self, False)
