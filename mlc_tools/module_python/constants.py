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
    print(ET.tostring(root))
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