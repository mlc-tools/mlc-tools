# -*- coding: utf-8 -*-
from tests.test_serializer.py.Meta import Meta
from tests.test_serializer.py.gen.BaseEnum import BaseEnum
from tests.test_serializer.py.gen.DataWrapper import DataWrapper
from tests.test_serializer.py.gen.IntrusivePtr import IntrusivePtr, make_intrusive
from tests.test_serializer.py.gen.Factory import Factory


class DeserializerXml(object):
    def __init__(self, node):
        self.node = node

    def deserialize(self, key, meta, default_value=None):
        node = self.get_child(key)
        if meta.__base__ == BaseEnum:
            value = self.deserialize_attr(key, str, '')
            return getattr(meta, value) if hasattr(meta, value) else default_value
        if isinstance(meta, Meta):
            if meta.args[0] == dict:
                return node.deserialize_dict('', meta)
            if meta.args[0] == list:
                return node.deserialize_list('', meta)
            if meta.args[0] == DataWrapper:
                from tests.test_serializer.py.gen.DataStorage import DataStorage
                value = self.deserialize_attr(key, str, '')
                return getattr(DataStorage.shared(), 'get' + meta.args[1].TYPE)(value)
            if meta.args[0] == IntrusivePtr:
                if node is not None and node.node is not None:
                    obj = Factory.build(node.node.attrib['type'])
                    obj.deserialize_xml(DeserializerXml(node.node))
                    return obj
                return None
        if hasattr(meta, 'deserialize_xml'):
            obj = meta()
            obj.deserialize_xml(node)
            return obj
        return self.deserialize_attr(key, meta, default_value)

    def deserialize_attr(self, key, meta, default_value):
        value = None
        if key and self.node is not None:
            if key in self.node.attrib:
                value = self.node.attrib[key]
            else:
                value = default_value
        if meta == bool:
            if isinstance(value, bool):
                return value
            if value is not None:
                value = value.lower()
            return True if value in ['true', 'yes'] else False if value in ['false', 'no'] else default_value if default_value else False
        if meta == str and not value and not default_value:
            return ''
        return meta(value or default_value or 0)

    def deserialize_dict(self, key, meta):
        node = DeserializerXml(self.node) if not key else self.get_child(key)
        if node.node is None:
            return {}
        result = {}
        for item in node.node:
            k = DeserializerXml(item).deserialize_key(meta.args[1])
            v = DeserializerXml(item).deserialize_value(meta.args[2])
            result[k] = v
        return result

    def deserialize_list(self, key, meta):
        if self.node is None:
            return []
        result = []
        for child in self.node:
            item = DeserializerXml(child).deserialize_list_item(meta.args[1])
            result.append(item)
        return result

    def get_child(self, key):
        return DeserializerXml(self.node.find(key) if (key and self.node is not None) else self.node)

    def deserialize_key(self, meta: Meta):
        return self.deserialize('key', meta)

    def deserialize_value(self, meta: Meta):
        return self.deserialize('value', meta)

    def deserialize_list_item(self, meta):
        if meta.__base__ == BaseEnum:
            value = self.deserialize_attr('value', str, '')
            return getattr(meta, value)
        elif hasattr(meta, 'serialize_xml'):
            obj = meta()
            obj.deserialize_xml(self)
            return obj
        elif isinstance(meta, list) or (isinstance(meta, Meta) and meta.args[0] == list):
            return self.deserialize_list('', meta)
        elif isinstance(meta, dict):
            return self.deserialize_dict('', meta)
        elif isinstance(meta, Meta):
            if meta.args[0] == DataWrapper:
                from tests.test_serializer.py.gen.DataStorage import DataStorage
                value = self.deserialize_attr('value', str, '')
                return getattr(DataStorage.shared(), 'get' + meta.args[1].TYPE)(value)
            if meta.args[0] == IntrusivePtr:
                obj = Factory.build(self.node.tag)
                obj.deserialize_xml(self)
                return obj
        else:
            return self.deserialize_attr('value', meta, None)
