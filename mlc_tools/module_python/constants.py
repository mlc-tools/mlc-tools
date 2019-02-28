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
