import xml.etree.ElementTree as ElementTree
import xml.dom.minidom
import json
import os
import re
from ..utils import fileutils
from ..utils.error import Error
from ..base.generator_data_storage_base import get_class_name_from_data_name
from ..base.generator_data_storage_base import get_data_list_name, get_data_name
from ..utils.error import Log


class DataParser(object):

    def __init__(self, classes, data_directory, filter_func):
        self.objects = {}
        self.format = None
        self.classes = classes
        self.filter_func = filter_func
        self.directories = [data_directory]

    def parse(self, additional_directories):
        directories = self.directories
        directories.extend(additional_directories)
        for directory in directories:
            directory = fileutils.normalize_path(directory)
            self._parse_directory(directory)
        self._validate()

    def flush(self, out_data_directory):
        buffer_ = ''
        if self.format is None:
            self.format = 'xml'
        filename = 'data.' + self.format
        if self.format == 'xml':
            buffer_ = self._flush_xml()
        elif self.format == 'json':
            buffer_ = self._flush_json()

        full_path = out_data_directory + filename
        exist = os.path.isfile(full_path)
        result, _ = fileutils.write(full_path, buffer_)
        if result:
            msg = ' Create: {}' if not exist else ' Overwriting: {}'
            Log.message(msg.format(filename))

    def _parse_directory(self, directory):
        files = fileutils.get_files_list(directory)
        for filename in files:
            full_path = directory + filename
            if self.filter_func is not None and not self.filter_func(full_path):
                continue
            if filename.endswith('.xml') and (self.format is None or self.format == 'xml'):
                self.format = 'xml'
                self._parse_xml(full_path)
            elif filename.endswith('.json') and (self.format is None or self.format == 'json'):
                self.format = 'json'
                self._parse_json(full_path)

    def _parse_xml(self, full_path):
        try:
            tree = ElementTree.parse(full_path)
            root = tree.getroot()

            def add(obj):
                if obj.tag not in self.objects:
                    self.objects[obj.tag] = []
                self._validate_type(obj.tag, full_path)
                self.objects[obj.tag].append(obj)

            if root.tag == 'data':
                for node in root:
                    add(node)
            else:
                add(root)
        except ElementTree.ParseError:
            Error.exit(Error.CANNOT_PARSE_XML, full_path)

    def _parse_json(self, full_path):
        root = json.loads(open(full_path, encoding='utf-8').read())

        if isinstance(root, dict):
            for key in root:
                self._parse_json_node(full_path, key, root)
        elif isinstance(root, list):
            for dict_ in root:
                for key in dict_:
                    self._parse_json_node(full_path, key, dict_)

    def _parse_json_node(self, full_path, key, dict_):
        name = key
        self._validate_type(key, full_path)
        if name not in self.objects:
            self.objects[name] = []
        self.objects[name].append(dict_)

    def _validate(self):
        pass

    def _validate_type(self, type_, filename=''):
        class_name = get_class_name_from_data_name(type_)
        valid = False
        for class_ in self.classes:
            if class_.name == class_name:
                valid = class_.is_storage
                break
        if not valid:
            Error.exit(Error.UNKNOWN_DATA_TYPE, type_, class_name, filename)

    def _flush_xml(self):
        root = ElementTree.Element('data')
        for type_ in self.objects:
            name = get_data_list_name(get_data_name(type_))
            node = ElementTree.SubElement(root, name)
            for obj in self.objects[type_]:
                pair = ElementTree.SubElement(node, 'pair')
                pair.attrib['key'] = obj.attrib['name']
                obj.tag = 'value'
                pair.append(obj)

        text = ElementTree.tostring(root).decode()
        return re.sub(r'>(\s+)<', '><', text)

    def _flush_json(self):
        dict_ = {}
        for key in self.objects:
            name = get_data_list_name(get_data_name(key))
            dict_[name] = []
            for object_ in self.objects[key]:
                dict_obj = {}
                for obj in object_:
                    dict_obj['key'] = object_[obj]['name']
                    dict_obj['value'] = object_[obj]
                dict_[name].append(dict_obj)
        return json.dumps(dict_, indent=2)
