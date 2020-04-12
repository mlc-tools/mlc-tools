# -*- coding: utf-8 -*-
from tests.test_serializer.py.gen.DataWrapper import DataWrapper
from tests.test_serializer.py.gen.IntrusivePtr import IntrusivePtr
import xml.etree.ElementTree as ET


class SerializerXml(object):
    def __init__(self, node):
        self.node = node

    def serialize(self, obj, key, default_value=None):
        if isinstance(obj, DataWrapper):
            self.serialize_attr(obj.name, key, default_value)
        elif isinstance(obj, IntrusivePtr):
            child = self.add_child(key)
            child.serialize_attr(obj.get_type(), 'type', default_value)
            obj.serialize_xml(child)
        elif hasattr(obj, 'serialize_xml'):
            obj.serialize_xml(self.add_child(key))
        elif isinstance(obj, list):
            self.serialize_list(obj, key)
        elif isinstance(obj, dict):
            self.serialize_dict(obj, key)
        else:
            self.serialize_attr(obj, key, default_value)

    def serialize_attr(self, obj, key, default_value):
        if obj != default_value:
            if obj is True:
                self.node.attrib[key] = 'true'
            elif obj is False:
                if default_value is not None:
                    self.node.attrib[key] = 'false'
            else:
                self.node.attrib[key] = str(obj)

    def serialize_dict(self, obj, key):
        node = SerializerXml(self.node) if not key else self.add_child(key)
        for k, v in obj.items():
            item = node.add_child('pair')
            item.serialize_key(k)
            item.serialize_value(v)

    def serialize_list(self, obj, key):
        node = SerializerXml(self.node) if not key else self.add_child(key)
        for item in obj:
            node.add_child('item').serialize_list_item(item)

    def add_child(self, key):
        node = ET.SubElement(self.node, key) if key else self.node
        return SerializerXml(node)

    def serialize_key(self, k):
        self.serialize(k, 'key')

    def serialize_value(self, v):
        self.serialize(v, 'value')

    def serialize_list_item(self, obj):
        if isinstance(obj, DataWrapper):
            self.serialize_attr(obj.name, 'value', '')
        elif isinstance(obj, IntrusivePtr):
            self.node.tag = obj.get_type()
            obj.serialize_xml(self)
        elif hasattr(obj, 'serialize_xml'):
            self.serialize(obj, '')
        elif isinstance(obj, list):
            self.serialize_list(obj, '')
        elif isinstance(obj, dict):
            self.serialize_dict(obj, '')
        else:
            self.serialize_attr(obj, 'value', None)
