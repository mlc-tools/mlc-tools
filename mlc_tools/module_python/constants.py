FACTORY = '''# -*- coding: utf-8 -*-

class Factory(object):

    @staticmethod
    def build(type):
{builders}
        return None
'''

COMMON_XML = '''
def create_command_from_xml(string):
    import xml.etree.ElementTree as ET
    from .Factory import Factory
    root = ET.fromstring(string)
    type = root.tag
    command = Factory.build(type)
    if command is not None:
        command.deserialize_xml(root)
    return command

def serialize_command_to_xml(command):
    import xml.etree.ElementTree as ET
    root = ET.Element(command.get_type())
    command.serialize_xml(root)
    return ET.tostring(root)

def clone_object(obj):
    payload = serialize_command_to_xml(obj)
    clone = create_command_from_xml(payload)
    return clone
'''

COMMON_JSON = '''
def create_command_from_json(string):
    import json
    from .Factory import Factory
    dictionary = json.loads(string)
    for key in dictionary:
        command = Factory.build(key)
        if command is not None:
            command.deserialize_json(dictionary[key])
        return command

def serialize_command_to_json(command):
    import json
    js = dict()
    js[command.get_type()] = dict()
    command.serialize_json(js[command.get_type()])
    return json.dumps(js)

def clone_object(obj):
    payload = serialize_command_to_json(obj)
    clone = create_command_from_json(payload)
    return clone
'''