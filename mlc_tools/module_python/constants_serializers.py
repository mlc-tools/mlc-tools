

META = """

class Meta(object):
    __base__ = object

    def __init__(self, *args):
        self.args = args

    def build(self, value):
        if isinstance(self.args[0], Meta):
            return self.args[0].build(value)
        return self.args[0](value)
"""

DATA_WRAPPER = """# -*- coding: utf-8 -*-


class DataWrapper(object):

    def __init__(self, instance):
        object.__setattr__(self, 'instance', instance)

    def __setattr__(self, name, value):
        object.__setattr__(object.__getattribute__(self, 'instance'), name, value)

    def __getattribute__(self, name):
        try:
            if name in ['is_valid']:
                return object.__getattribute__(self, name)
            return object.__getattribute__(self, 'instance').__getattribute__(name)
        except AttributeError as e:
            return None

    def __eq__(self, rhs):
        if rhs is None:
            return object.__getattribute__(self, 'instance') is None
        return rhs is not None and rhs.name is not None and self.name == rhs.name

    def __ne__(self, rhs):
        if rhs is None:
            return object.__getattribute__(self, 'instance') is not None
        return rhs is not None and rhs.name is None or self.name != rhs.name

    def __hash__(self):
        return hash(self.name)

    def is_valid(self):
        return object.__getattribute__(self, 'instance') is not None
"""

INTRUSIVE = """# -*- coding: utf-8 -*-


class IntrusivePtr(object):

    def __init__(self, instance):
        object.__setattr__(self, 'instance', instance)

    def __setattr__(self, name, value):
        object.__setattr__(object.__getattribute__(self, 'instance'), name, value)

    def __getattribute__(self, name):
        if name in ['is_valid']:
            return object.__getattribute__(self, name)
        return object.__getattribute__(self, 'instance').__getattribute__(name)

    def __eq__(self, rhs):
        if rhs is None:
            return
        self_instance = object.__getattribute__(self, 'instance')
        rhs_instance = object.__getattribute__(rhs, 'instance') if isinstance(rhs, IntrusivePtr) else rhs
        return self_instance.__eq__(rhs_instance)

    def __hash__(self):
        return id(object.__getattribute__(self, 'instance'))

    def is_valid(self):
        return object.__getattribute__(self, 'instance') is not None


def make_intrusive(class_name, *args):
    return IntrusivePtr(class_name(*args))
"""

SERIALIZER_XML = """# -*- coding: utf-8 -*-
from .DataWrapper import DataWrapper
from .IntrusivePtr import IntrusivePtr
import xml.etree.ElementTree as ET


class SerializerXml(object):
    def __init__(self, node):
        self.node = node

    def serialize(self, obj, key, default_value=None):
        if isinstance(obj, DataWrapper) and obj is not None:
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
            if obj.is_valid():
                obj.serialize_xml(self)
        elif hasattr(obj, 'serialize_xml'):
            self.serialize(obj, '')
        elif isinstance(obj, list):
            self.serialize_list(obj, '')
        elif isinstance(obj, dict):
            self.serialize_dict(obj, '')
        else:
            self.serialize_attr(obj, 'value', None)
"""

DESERIALIZER_XML = """# -*- coding: utf-8 -*-
from .Meta import Meta
from .BaseEnum import BaseEnum
from .DataWrapper import DataWrapper
from .IntrusivePtr import IntrusivePtr, make_intrusive
from .Factory import Factory


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
                from .DataStorage import DataStorage
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
        try:
            return meta(value or default_value or 0)
        except ValueError as e:
            if meta == int:
                return int(float(value or default_value or 0))
            raise e

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
                from .DataStorage import DataStorage
                value = self.deserialize_attr('value', str, '')
                return getattr(DataStorage.shared(), 'get' + meta.args[1].TYPE)(value)
            if meta.args[0] == IntrusivePtr:
                obj = Factory.build(self.node.tag)
                if obj and obj.is_valid():
                    obj.deserialize_xml(self)
                return obj
        else:
            return self.deserialize_attr('value', meta, None)
"""

SERIALIZER_JSON = """# -*- coding: utf-8 -*-
from .DataWrapper import DataWrapper
from .IntrusivePtr import IntrusivePtr


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
            self.json[-1]['type'] = obj.get_type() if obj.is_valid() else ''
            if obj.is_valid():
                obj.serialize_json(SerializerJson(self.json[-1]))
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
"""

DESERIALIZER_JSON = """# -*- coding: utf-8 -*-
from .Meta import Meta
from .BaseEnum import BaseEnum
from .DataWrapper import DataWrapper
from .IntrusivePtr import IntrusivePtr, make_intrusive
from .Factory import Factory


class DeserializerJson(object):
    def __init__(self, json):
        self.json = json

    def deserialize(self, key, meta, default_value=None):
        js = self.json if not key else self.json[key] if key in self.json else {}
        if meta.__base__ == BaseEnum:
            value = DeserializerJson(js).deserialize_attr('', str, '')
            return getattr(meta, value) if hasattr(meta, value) else default_value
        if isinstance(meta, Meta):
            if meta.args[0] == dict:
                return DeserializerJson(js).deserialize_dict('', meta)
            if meta.args[0] == list:
                return DeserializerJson(js).deserialize_list('', meta)
            if meta.args[0] == DataWrapper:
                from .DataStorage import DataStorage
                value = DeserializerJson(js).deserialize_attr('', str, '')
                return getattr(DataStorage.shared(), 'get' + meta.args[1].TYPE)(value)
            if meta.args[0] == IntrusivePtr:
                if js and 'type' in js:
                    obj = Factory.build(js['type'])
                    # obj = make_intrusive(meta.args[1])
                    obj.deserialize_json(DeserializerJson(js))
                    return obj
                return None
        if hasattr(meta, 'deserialize_json'):
            obj = meta()
            obj.deserialize_json(DeserializerJson(js))
            return obj
        return DeserializerJson(js).deserialize_attr('', meta, default_value)

    def deserialize_attr(self, key, meta, default_value):
        if key:
            if key in self.json:
                return self.json[key]
            else:
                return default_value
        if self.json.__class__ == meta:
            return meta(self.json)
        return meta(self.json or default_value)

    def deserialize_dict(self, key, meta):
        js = DeserializerJson(self.json) if not key else self.get_child_array(key)
        if not js.json:
            return {}
        assert isinstance(js.json, list)
        result = {}
        for item in js.json:
            k = DeserializerJson(item).deserialize_key(meta.args[1])
            v = DeserializerJson(item).deserialize_value(meta.args[2])
            result[k] = v
        return result

    def deserialize_list(self, key, meta):
        if not self.json:
            return []
        assert isinstance(self.json, list)
        result = []
        for js in self.json:
            item = DeserializerJson(js).deserialize('', meta.args[1])
            result.append(item)
        return result

    def get_child_array(self, key):
        return DeserializerJson(self.json[key] if key in self.json else [])

    def deserialize_key(self, meta: Meta):
        return self.deserialize('key', meta)

    def deserialize_value(self, meta: Meta):
        return self.deserialize('value', meta)
"""