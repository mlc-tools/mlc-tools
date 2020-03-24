# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import json
from .common import *
from ..DeserializerJson import DeserializerJson
from ..DeserializerXml import DeserializerXml
from ..Meta import Meta
from ..SerializerJson import SerializerJson
from ..SerializerXml import SerializerXml


class AllTypesChildren(object):
    TYPE = "AllTypesChildren"
    __slots__ = ["value"]

    def __init__(self):
        self.value = 0

    def __hash__(self):
        return id(self)

    def __eq__(self, rhs):
        result = True
        result = result and self.value == rhs.value
        return result
        pass

    def __ne__(self, rhs):
        return not (self == rhs)
        pass

    def get_type(self):
        return AllTypesChildren.TYPE
        pass

    def serialize_xml(self, serializer: SerializerXml):
        pass

    def deserialize_xml(self, serializer: DeserializerXml):
        pass

    def serialize_json(self, serializer: SerializerJson):
        serializer.serialize(self.value, 'value', 0)
        pass

    def deserialize_json(self, deserializer: DeserializerJson):
        self.value = deserializer.deserialize('value', int, 0)
