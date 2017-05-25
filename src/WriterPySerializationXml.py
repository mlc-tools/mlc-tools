from WriterPython import WriterPython
from WriterPython import SERIALIZATION
from WriterPython import DESERIALIZATION
from Object import Object
from Class import Class


class WriterPySerializationXml(WriterPython):
    def __init__(self, outDirectory, parser, configsDirectory):
        WriterPython.__init__(self, outDirectory, parser, configsDirectory)

    def create_serialization_patterns(self):
        self.simple_types = ["int", "float", "bool", "string"]
        self.serialize_formats = self.parser.parse_serialize_protocol('protocol_py_xml.txt')

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
    def getPatternSerializationMap(self):
        return '''
        xml_cache = xml
        map = ET.SubElement(xml, '{0}')
        for key, value in self.{0}.iteritems():
            xml = ET.SubElement(map, 'pair')
{1}
{2}
        xml = xml_cache
'''

    def getPatternDeserializationMap(self):
        return '''
        xml_cache = xml
        map = xml.find('{0}')
        for xml_child in map:
            key = xml_child.get('key')
            type = key
            xml = xml_child
{2}
            self.{0}[type] = _value
        xml = xml_cache
'''