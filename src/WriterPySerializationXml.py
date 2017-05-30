from WriterPython import WriterPython


class WriterPySerializationXml(WriterPython):

    def __init__(self, parser, configsDirectory):
        WriterPython.__init__(self, parser, configsDirectory)

    def getSerialiationFunctionArgs(self):
        return '(self, xml)'

    def get_pattern_file(self):
        return '''

import xml.etree.ElementTree as ET
{3}

class {0}:
    def __init__(self):
{4}
{1}
        return

    def get_type(self):
        return self.__type__

{2}
'''

    def getPatternFactoryFile(self):
        return '''import xml.etree.ElementTree as ET
{0}

class Factory:
    def __init__(self):
        return

    @staticmethod
    def build(type):
{1}
        return None

    @staticmethod
    def create_command(string):
        root = ET.fromstring(string)
        type = root.tag
        command = Factory.build(type)
        if command != None:
            command.deserialize(root)
        return command
'''
