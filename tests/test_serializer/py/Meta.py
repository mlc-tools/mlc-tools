

class Meta(object):
    __base__ = object

    def __init__(self, *args):
        self.args = args

    def build(self, value):
        if isinstance(self.args[0], Meta):
            return self.args[0].build(value)
        return self.args[0](value)
