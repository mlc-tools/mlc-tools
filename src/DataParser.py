import xml.etree.ElementTree as ET
import fileutils
import xml.etree.ElementTree as ET
import xml.dom.minidom
from DataStorageCreators import get_member_name
import json

class DataParser:
    def __init__(self, classes, format, data_directory):
        self.objects = {}
        self.format = format
        
        if self.format == 'xml':
            self._parse_xml(data_directory)
        elif self.format == 'json':
            self._parse_json(data_directory)
        self._validate(classes)

    def flush(self, out_data_directory):
        buffer = ''
        file = 'data.' + self.format
        if self.format == 'xml':
            buffer = self._flush_xml(out_data_directory)
        elif self.format == 'json':
            buffer = self._flush_json(out_data_directory)
        fileutils.write(out_data_directory + file, buffer)

    def _parse_xml(self, data_directory):
        files = fileutils.get_files_list(data_directory)
        for file in files:
            file = data_directory + file
            tree = ET.parse(file)
            root = tree.getroot()
            for object in root:
                if object.tag not in self.objects:
                    self.objects[object.tag] = []
                self.objects[object.tag].append(object)

    def _parse_json(self, data_directory):
        files = fileutils.get_files_list(data_directory)
        for file in files:
            file = data_directory + file
            root = json.loads(open(file).read())
            for key in root:
                name = key;
                if name not in self.objects:
                    self.objects[name] = []
                self.objects[name].append(root)

            

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

    def _flush_xml(self, out_data_directory):
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
        return buffer

    def _flush_json(self, out_data_directory):
        dict_ = {}
        for key in self.objects:
            name = get_member_name(key)
            dict_[name] = []
            for object in self.objects[key]:
                dict_obj = {}
                for obj in object:
                    dict_obj['key'] = object[obj]['name']
                    dict_obj['value'] = object[obj]
                dict_[name].append(dict_obj)
        return json.dumps(dict_, indent=2)

        