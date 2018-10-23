FACTORY = '''# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import json


class Factory:

    @staticmethod
    def build(type):
{builders}
        return None

    @staticmethod
    def create_command_from_xml(string):
        root = ET.fromstring(string)
        type = root.tag
        command = Factory.build(type)
        if command is not None:
            command.deserialize(root)
        return command

    @staticmethod
    def serialize_command_to_xml(command):
        root = ET.Element(command.get_type())
        command.serialize(root)
        return ET.tostring(root)

    @staticmethod
    def create_command_from_json(string):
        dictionary = json.loads(string)
        for key in dictionary:
            command = Factory.build(key)
            if command is not None:
                command.deserialize(dictionary[key])
            return command

    @staticmethod
    def serialize_command_to_json(command):
        js = dict()
        js[command.get_type()] = dict()
        command.serialize(js[command.get_type()])
        return json.dumps(js)
'''
