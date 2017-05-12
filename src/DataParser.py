import xml.etree.ElementTree as ET
import fileutils
import xml.etree.ElementTree as ET
import xml.dom.minidom
from DataStorageCreators import get_member_name

class DataParser:
    def __init__(self, classes, data_directory):
        self.objects = {}
        
        self._parse(data_directory)
        self._validate(classes)

    def flush(self, out_data_directory):
        root = ET.Element('data')
        for type in self.objects:
            name = get_member_name(type)
            node = ET.SubElement(root, name)
            for object in self.objects[type]:
                pair = ET.SubElement(node, 'pair')
                pair.attrib['key'] = object.attrib['name']
                object.tag = 'value'
                pair.append(object)

        buffer = ET.tostring(root);
        xml_ = xml.dom.minidom.parseString(buffer)
        buffer = xml_.toprettyxml()
        lines = buffer.split('\n')
        buffer = ''
        for line in lines:
            if line.strip():
                buffer += line + '\n'

        fileutils.write(out_data_directory + 'data.xml', buffer)

    def _parse(self, data_directory):
        files = fileutils.get_files_list(data_directory)
        for file in files:
            file = data_directory + file
            tree = ET.parse(file)
            root = tree.getroot()
            for object in root:
                if object.tag not in self.objects:
                    self.objects[object.tag] = []
                self.objects[object.tag].append(object)

    def _validate(self, classes):
        for type in self.objects:
            class_name = 'Data' + type[0].upper() + type[1:]
            valid = False
            for class_ in classes:
                if class_.name == class_name:
                    valid = class_.is_storage
                    break
            if not valid:
                print 'Unknown data type [{}]->[{}]. please check configuration'.format(type, class_name)
                exit(-1)
        pass