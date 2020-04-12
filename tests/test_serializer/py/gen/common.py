# -*- coding: utf-8 -*-

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
