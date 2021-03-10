# -*- coding: utf-8 -*-
from tests.test_serializer.py.gen.DataWrapper import DataWrapper
from tests.test_serializer.py.gen.IntrusivePtr import IntrusivePtr


class SerializerJson(object):
    def __init__(self, json):
        self.json = json

    def serialize(self, obj, key, default_value=None):
        if isinstance(obj, DataWrapper):
            self.serialize_attr(obj.name, key, default_value)
        elif isinstance(obj, IntrusivePtr):
            child = self.add_child(key)
            child.serialize_attr(obj.get_type(), 'type', default_value)
            obj.serialize_json(child)
            pass
        elif hasattr(obj, 'serialize_json'):
            obj.serialize_json(self.add_child(key))
        elif isinstance(obj, list):
            self.serialize_list(obj, key)
        elif isinstance(obj, dict):
            self.serialize_dict(obj, key)
        else:
            self.serialize_attr(obj, key, default_value)

    def serialize_attr(self, obj, key, default_value):
        if obj != default_value:
            self.json[key] = obj

    def serialize_dict(self, obj, key):
        js = SerializerJson(self.json) if not key else self.add_child_array(key)
        for k, v in obj.items():
            item = js.add_array_item('')
            item.serialize_key(k)
            item.serialize_value(v)

    def serialize_list(self, obj, key):
        js = SerializerJson(self.json) if not key else self.add_child_array(key)
        for item in obj:
            js.serialize_list_item(item)

    def add_child(self, key):
        if key:
            self.json[key] = {}
            return SerializerJson(self.json[key])
        else:
            return self

    def add_child_array(self, key):
        self.json[key] = []
        return SerializerJson(self.json[key])

    def add_array_item(self, key):
        self.json.append({})
        return SerializerJson(self.json[-1])

    def serialize_key(self, k):
        self.serialize(k, 'key')

    def serialize_value(self, v):
        self.serialize(v, 'value')

    def serialize_list_item(self, obj):
        self.json.append(None)
        if isinstance(obj, DataWrapper):
            self.json[-1] = obj.name
        elif isinstance(obj, IntrusivePtr):
            self.json[-1] = {}
            self.json[-1]['type'] = obj.get_type()
            obj.serialize_xml(SerializerJson(self.json[-1]))
            pass
        elif hasattr(obj, 'serialize_json'):
            self.json[-1] = {}
            serializer = SerializerJson(self.json[-1])
            serializer.serialize(obj, '')
        elif isinstance(obj, list):
            self.json[-1] = []
            SerializerJson(self.json[-1]).serialize_list(obj, '')
        elif isinstance(obj, dict):
            self.serialize_dict(obj, '')
        else:
            self.json[-1] = obj
