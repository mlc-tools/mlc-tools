from tests.test_serializer.py.gen.BaseEnum import BaseEnum
from tests.test_serializer.py.gen.DataWrapper import DataWrapper
from tests.test_serializer.py.gen.intrusive_ptr import IntrusivePtr, make_intrusive


class Meta(object):
    __base__ = object

    def __init__(self, *args):
        self.args = args

    def build(self, value):
        if isinstance(self.args[0], Meta):
            return self.args[0].build(value)
        return self.args[0](value)


class DeserializerJson(object):
    def __init__(self, json):
        self.json = json

    def deserialize(self, key, meta, default_value=None):
        js = self.json if not key else self.json[key] if key in self.json else {}
        if meta.__base__ == BaseEnum:
            value = DeserializerJson(js).deserialize_attr('', str, '')
            return getattr(meta, value)
        if isinstance(meta, Meta):
            if meta.args[0] == dict:
                return DeserializerJson(js).deserialize_dict('', meta)
            if meta.args[0] == list:
                return DeserializerJson(js).deserialize_list('', meta)
            if meta.args[0] == DataWrapper:
                from tests.test_serializer.py.gen.DataStorage import DataStorage
                value = DeserializerJson(js).deserialize_attr('', str, '')
                return DataStorage.shared().getDataUnit(value)
            if meta.args[0] == IntrusivePtr:
                obj = make_intrusive(meta.args[1])
                obj.deserialize_json(DeserializerJson(js))
                return obj
            assert 0
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
        return default_value

    def deserialize_dict(self, key, meta):
        js = DeserializerJson(self.json) if not key else self.get_child_array(key)
        assert isinstance(js.json, list)
        result = {}
        for item in js.json:
            k = DeserializerJson(item).deserialize_key(meta.args[1])
            v = DeserializerJson(item).deserialize_value(meta.args[2])
            result[k] = v
        return result

    def deserialize_list(self, key, meta):
        assert isinstance(self.json, list)
        if not self.json:
            return []
        result = []
        for js in self.json:
            item = DeserializerJson(js).deserialize('', meta.args[1])
            result.append(item)
        return result

    def get_child(self, key):
        return DeserializerJson(self.json[key] if key in self.json else {})

    def get_child_array(self, key):
        return DeserializerJson(self.json[key] if key in self.json else [])

    def deserialize_key(self, meta: Meta):
        return self.deserialize('key', meta)

    def deserialize_value(self, meta: Meta):
        return self.deserialize('value', meta)

    def deserialize_list_item(self, obj):
        self.json.append(None)
        if hasattr(obj, 'deserialize_json'):
            self.json[-1] = {}
            deserializer = DeserializerJson(self.json[-1])
            deserializer.deserialize(obj, '')
        elif isinstance(obj, list):
            self.json[-1] = []
            DeserializerJson(self.json[-1]).deserialize_list(obj, '')
        elif isinstance(obj, dict):
            self.deserialize_dict(obj, '')
        else:
            self.json[-1] = obj
