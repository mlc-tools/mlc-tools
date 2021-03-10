# -*- coding: utf-8 -*-
from tests.test_serializer.py.SerializerJson import SerializerJson
from tests.test_serializer.py.DeserializerJson import DeserializerJson


def create_command_from_json(string):
    import json
    from .Factory import Factory
    dictionary = json.loads(string)
    for key in dictionary:
        command = Factory.build(key)
        if command is not None:
            deserializer = DeserializerJson(dictionary[key])
            command.deserialize_json(deserializer)
        return command

def serialize_command_to_json(command):
    import json
    js = dict()
    js[command.get_type()] = dict()
    serializer = SerializerJson(js[command.get_type()])
    command.serialize_json(serializer)
    return json.dumps(js)

def clone_object(obj):
    payload = serialize_command_to_json(obj)
    clone = create_command_from_json(payload)
    return clone
