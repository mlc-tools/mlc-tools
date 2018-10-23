from ..language import WriterBase
from .. import fileutils


class Writer(WriterBase):
    
    def __init__(self, out_directory):
        WriterBase.__init__(self, out_directory)
        pass

