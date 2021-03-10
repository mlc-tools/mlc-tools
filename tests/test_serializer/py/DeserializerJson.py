# -*- coding: utf-8 -*-
from tests.test_serializer.py.Meta import Meta
from tests.test_serializer.py.gen.BaseEnum import BaseEnum
from tests.test_serializer.py.gen.DataWrapper import DataWrapper
from tests.test_serializer.py.gen.IntrusivePtr import IntrusivePtr, make_intrusive
from tests.test_serializer.py.gen.Factory import Factory


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
                from tests.test_serializer.py.gen.DataStorage import DataStorage
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
        return self.json or default_value

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
