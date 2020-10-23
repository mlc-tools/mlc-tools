FACTORY = '''# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import json


class Factory(object):

    @staticmethod
    def build(type):
{builders}
        return None

    {{{{format=xml}}}}
    @staticmethod
    def create_command_from_xml(string):
        root = ET.fromstring(string)
        type = root.tag
        command = Factory.build(type)
        if command is not None:
            command.deserialize_xml(root)
        return command

    @staticmethod
    def serialize_command_to_xml(command):
        root = ET.Element(command.get_type())
        command.serialize_xml(root)
        return ET.tostring(root)

    @staticmethod
    def clone_object(obj):
        payload = Factory.serialize_command_to_xml(obj)
        clone = Factory.create_command_from_xml(payload)
        return clone
    {{{{end_format=xml}}}}
    {{{{format=json}}}}
    @staticmethod
    def create_command_from_json(string):
        dictionary = json.loads(string)
        for key in dictionary:
            command = Factory.build(key)
            if command is not None:
                command.deserialize_json(dictionary[key])
            return command

    @staticmethod
    def serialize_command_to_json(command):
        js = dict()
        js[command.get_type()] = dict()
        command.serialize_json(js[command.get_type()])
        return json.dumps(js)

    @staticmethod
    def clone_object(obj):
        payload = Factory.serialize_command_to_json(obj)
        clone = Factory.create_command_from_json(payload)
        return clone
    {{{{end_format=json}}}}
    {{{{format=both}}}}
    @staticmethod
    def create_command_from_xml(string):
        root = ET.fromstring(string)
        type = root.tag
        command = Factory.build(type)
        if command is not None:
            command.deserialize_xml(root)
        return command

    @staticmethod
    def serialize_command_to_xml(command):
        root = ET.Element(command.get_type())
        command.serialize_xml(root)
        return ET.tostring(root)
    @staticmethod
    def create_command_from_json(string):
        dictionary = json.loads(string)
        for key in dictionary:
            command = Factory.build(key)
            if command is not None:
                command.deserialize_json(dictionary[key])
            return command

    @staticmethod
    def serialize_command_to_json(command):
        js = dict()
        js[command.get_type()] = dict()
        command.serialize_json(js[command.get_type()])
        return json.dumps(js)

    @staticmethod
    def clone_object(obj):
        payload = Factory.serialize_command_to_json(obj)
        clone = Factory.create_command_from_json(payload)
        return clone
    {{{{end_format=both}}}}
'''

MG_EXTENSIONS = '''

def strTo(value, class_):
    if class_ == bool:
        return value.lower() in ['yes', 'true', 'y']
    return class_(value)
    
def in_list(key, container):
    return key in container
    
def list_push(container, value):
    container.append(value)
    
def list_insert(container, value, index):
    container.insert(value, index)
    
def list_remove(container, value):
    container.remove(value)
    
def list_erase(container, index):
    container.remove(container[index])
    
def list_truncate(container, size):
    while len(container) > size:
        container.pop()
        
def list_clear(container):
    container.clear()
    
def list_size(container):
    return len(container)
    
def list_resize(container, size):
    list_truncate(container, size)
    while len(container) < size:
        container.append(None)

def in_map(key, container):
    return key in container
    
def map_size(container):
    return len(container)
    
def map_remove(container, value):
    container.pop(value, None)
    
def map_clear(container):
    container.clear()

def string_empty(container):
    return len(container) == 0
    
def string_size(container):
    return len(container)

'''

FILES_DICT = [
    ['mg_extensions.py', MG_EXTENSIONS],
]
