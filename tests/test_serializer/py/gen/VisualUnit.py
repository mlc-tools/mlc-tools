# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import json
from .common import *
from ..SerializerJson import SerializerJson


class VisualUnit(object):
    TYPE = "VisualUnit"
    __slots__ = ["name", "icon"]

    def __init__(self):
        self.name = ""
        self.icon = ""

    def __hash__(self):
        return id(self)

    def __eq__(self, rhs):
        result = True
        result = result and self.name == rhs.name
        result = result and self.icon == rhs.icon
        return result
        pass

    def __ne__(self, rhs):
        return not (self == rhs)
        pass

    def get_type(self):
        return VisualUnit.TYPE
        pass

    def serialize_json(self, serializer: SerializerJson):
        pass

    def deserialize_json(self, dictionary):
        pass
