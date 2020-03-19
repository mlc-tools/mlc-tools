"""
Serializer:
общий метод serialize
 - проверяет, есть ли метод serialize у объекта. Если есть, дергает его
 - если нет, то уже isinstance и вызывает соответствующие методы у Serialize - долго
"""

"""
dict[Object, Object]:
"map_t12": [{
    "key": {
        "value": 1
    },
    "value": {
        "value": 1
    }
}],

dict[int, int]:
"map_i_i": [{
    "key": 1,
    "value": 2
}],

"""


class SerializerJson(object):
    def __init__(self, json):
        self.json = json

    def serialize(self, obj, key):
        if hasattr(obj, 'serialize_json'):
            obj.serialize_json(self.add_child(key))
        elif isinstance(obj, list):
            self.serialize_list(obj, key)
        elif isinstance(obj, dict):
            self.serialize_dict(obj, key)
        else:
            self.serialize_attr(obj, key)

    def serialize_attr(self, obj, key):
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
        self.json[key] = {}
        return SerializerJson(self.json[key])

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
        if hasattr(obj, 'serialize_json'):
            self.json[-1] = {}
            serializer = SerializerJson(self.json[-1])
            serializer.serialize(obj, '')
        elif isinstance(obj, list):
            self.serialize_list(obj, '')
        elif isinstance(obj, dict):
            self.serialize_dict(obj, '')
        else:
            self.json[-1] = obj
