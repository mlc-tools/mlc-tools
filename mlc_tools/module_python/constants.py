FACTORY = '''# -*- coding: utf-8 -*-
from .IntrusivePtr import make_intrusive

class Factory(object):

    @staticmethod
    def build(type):
{builders}
        return None
'''

COMMON_XML = '''

def create_command_from_xml(string):
    from .DeserializerXml import DeserializerXml
    import xml.etree.ElementTree as ET
    from .Factory import Factory
    root = ET.fromstring(string)
    type = root.tag
    command = Factory.build(type)
    if command is not None:
        deserializer = DeserializerXml(root)
        command.deserialize_xml(deserializer)
    return command


def serialize_command_to_xml(command):
    from .SerializerXml import SerializerXml
    import xml.etree.ElementTree as ET
    root = ET.Element(command.get_type())
    serializer = SerializerXml(root)
    command.serialize_xml(serializer)
    return ET.tostring(root)


def clone_object(obj, _=None):
    payload = serialize_command_to_xml(obj)
    clone = create_command_from_xml(payload)
    return clone
'''

COMMON_JSON = '''
def create_command_from_json(string):
    import json
    from .Factory import Factory
    from .DeserializerJson import DeserializerJson
    dictionary = json.loads(string)
    for key in dictionary:
        command = Factory.build(key)
        if command is not None:
            deserializer = DeserializerJson(dictionary[key])
            command.deserialize_json(deserializer)
        return command


def serialize_command_to_json(command):
    import json
    from .SerializerJson import SerializerJson
    js = dict()
    js[command.get_type()] = dict()
    serializer = SerializerJson(js[command.get_type()])
    command.serialize_json(serializer)
    return json.dumps(js)

def clone_object(obj, _=None):
    payload = serialize_command_to_json(obj)
    clone = create_command_from_json(payload)
    return clone
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
    
def list_index(container, item):
    return container.index(item) if item in container else -1
    
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

def split(string, delimiter):
    return string.split(delimiter)

def join(values, delimiter):
    return delimiter.join(values)

'''
