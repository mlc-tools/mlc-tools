# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import json
from .common import *
from .UnitType import UnitType
from ..DeserializerJson import DeserializerJson
from ..DeserializerXml import DeserializerXml
from ..SerializerJson import SerializerJson
from ..SerializerXml import SerializerXml


class DataUnit(object):
    TYPE = "DataUnit"
    __slots__ = ["name", "unit_type", "visual", "link_to_data", "all_units", "map_units"]

    def __init__(self):
        self.name = ""
        self.unit_type = UnitType()
        from .VisualUnit import VisualUnit
        self.visual = VisualUnit()
        self.link_to_data = None
        self.all_units = []
        self.map_units = {}

    def __hash__(self):
        return id(self)

    def __eq__(self, rhs):
        result = True
        result = result and self.name == rhs.name
        result = result and self.unit_type == rhs.unit_type
        result = result and self.visual == rhs.visual
        result = result and self.all_units == rhs.all_units
        result = result and self.map_units == rhs.map_units
        return result
        pass

    def __ne__(self, rhs):
        return not (self == rhs)
        pass

    def get_type(self):
        return DataUnit.TYPE
        pass

    def serialize_xml(self, serializer: SerializerXml):
        pass

    def deserialize_xml(self, deserializer: DeserializerXml):
        pass

    def serialize_json(self, serializer: SerializerJson):
        pass

    def deserialize_json(self, deserializer: DeserializerJson):
        pass
