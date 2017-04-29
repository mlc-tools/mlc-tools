from WriterPython import WriterPython
from WriterPython import SERIALIZATION
from WriterPython import DESERIALIZATION
from Object import Object
from Class import Class


class WriterPySerializationXml(WriterPython):
    def __init__(self, outDirectory, parser, configsDirectory):
        WriterPython.__init__(self, outDirectory, parser, configsDirectory)

    def create_serialization_patterns(self):
        self.simple_types = ["int", "float", "bool", "string", "cc.point"]

        # {0} = obj_name
        # {1} = obj_type
        # {2} = obj_value
        # {3} = '{}'
        # {4} = owner
        # {5} = obj_template_args[0].type if len(obj_template_args) > 0 else 'unknown_arg'
        self.serialize_formats = []
        self.serialize_formats.append({})
        self.serialize_formats.append({})
        
        self.serialize_formats[SERIALIZATION]['simple'] = []
        self.serialize_formats[SERIALIZATION]['simple'].append( 'if {4}{0} != {2}: xml.set("{0}", str({4}{0}))' )
        self.serialize_formats[SERIALIZATION]['simple'].append( 'xml.set("{0}", str({4}{0}))' )
        self.serialize_formats[DESERIALIZATION]['simple'] = []
        self.serialize_formats[DESERIALIZATION]['simple'].append( '{4}{0} = xml.get("{0}", default={2})' )
        self.serialize_formats[DESERIALIZATION]['simple'].append( '{4}{0} = xml.get("{0}")' )

        self.serialize_formats[SERIALIZATION]['pointer'] = []
        self.serialize_formats[SERIALIZATION]['pointer'].append( 'print "field {0} not should have a initialize value"' )
        self.serialize_formats[SERIALIZATION]['pointer'].append( '''
        if {4}{0} != None:
            xml_pointer = ET.SubElement(xml, '{0}')
            xml_pointer.set('type', str({1}))
            {4}{0}.serialize(xml_pointer) ''' )
        self.serialize_formats[DESERIALIZATION]['pointer'] = []
        self.serialize_formats[DESERIALIZATION]['pointer'].append( 'print "field {0} not should have a initialize value"' )
        self.serialize_formats[DESERIALIZATION]['pointer'].append( '''
        xml_pointer = xml.find('{0}')
        if xml_pointer != None:
            type = xml_pointer.get('type')
            {4}{0} = Factory.Factory.build(type);
            {4}{0}.deserialize(xml_pointer) ''')

        self.serialize_formats[SERIALIZATION]['list<simple>'] = []
        self.serialize_formats[SERIALIZATION]['list<simple>'].append( '''
        arr = ET.SubElement(xml, '{0}')
        for obj in {4}{0}:
            item = ET.SubElement(arr, 'item')
            item.set('value', str(obj))''' )
        self.serialize_formats[SERIALIZATION]['list<simple>'].append( self.serialize_formats[SERIALIZATION]['list<simple>'][0] )

        self.serialize_formats[DESERIALIZATION]['list<simple>'] = []
        self.serialize_formats[DESERIALIZATION]['list<simple>'].append( '''
        arr = xml.find('{0}')
        for obj in arr:
            {4}{0}.append(obj.get('value'))''' )
        self.serialize_formats[DESERIALIZATION]['list<simple>'].append( self.serialize_formats[DESERIALIZATION]['list<simple>'][0] )

        self.serialize_formats[SERIALIZATION]['list<serialized>'] = []
        self.serialize_formats[SERIALIZATION]['list<serialized>'].append( '''
        arr = ET.SubElement(xml, '{0}')
        for obj in {4}{0}:
            item = ET.SubElement(arr, 'item')
            obj.serialize(item)''' )
        self.serialize_formats[SERIALIZATION]['list<serialized>'].append( self.serialize_formats[SERIALIZATION]['list<serialized>'][0] )

        self.serialize_formats[DESERIALIZATION]['list<serialized>'] = []
        self.serialize_formats[DESERIALIZATION]['list<serialized>'].append( '''
        arr = xml.find('{0}')
        for xml_child in arr:
            obj = {1}()
            obj.deserialize(xml_child)
            {4}{0}.append(obj)''' )
        self.serialize_formats[DESERIALIZATION]['list<serialized>'].append( self.serialize_formats[DESERIALIZATION]['list<serialized>'][0] )

        self.serialize_formats[SERIALIZATION]['serialized'] = []
        self.serialize_formats[SERIALIZATION]['serialized'].append( '''
        if {4}{0} != None:
            xml_child = ET.SubElement(xml, '{0}')
            {4}{0}.serialize(xml_child)''' )
        self.serialize_formats[SERIALIZATION]['serialized'].append( self.serialize_formats[SERIALIZATION]['serialized'][0] )

        self.serialize_formats[DESERIALIZATION]['serialized'] = []
        self.serialize_formats[DESERIALIZATION]['serialized'].append( '''
        xml_child = xml.find('{0}')
        if(xml_child != None):
            {4}{0} = {1}()
            {4}{0}.deserialize(xml_child)''' )
        self.serialize_formats[DESERIALIZATION]['serialized'].append( self.serialize_formats[DESERIALIZATION]['serialized'][0] )

        self.serialize_formats[SERIALIZATION]['pointer_list'] = []
        self.serialize_formats[SERIALIZATION]['pointer_list'].append( 'print "field {0} not should have a initialize value"' )
        self.serialize_formats[SERIALIZATION]['pointer_list'].append( '''
        arr = ET.SubElement(xml, '{0}')
        for t in {4}{0}:
            item = ET.SubElement(arr, t.get_type())
            t.serialize(item)''' )

        self.serialize_formats[DESERIALIZATION]['pointer_list'] = []
        self.serialize_formats[DESERIALIZATION]['pointer_list'].append( 'print "field {0} not should have a initialize value"' )
        self.serialize_formats[DESERIALIZATION]['pointer_list'].append( '''
        arr = xml.find('{0}')
        for xml_item in arr:
            type = xml_item.tag
            obj = Factory.Factory.build(type)
            obj.deserialize(xml_item)
            {4}{0}.append(obj)''' )

    def getSerialiationFunctionArgs(self):
        return '(self, xml)'

    def getPatternFile(self):
        return '''import Factory
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