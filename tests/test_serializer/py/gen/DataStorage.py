# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import json

from .DataWrapper import DataWrapper
from .common import *
from .. import SerializerXml
from ..DeserializerXml import DeserializerXml
from ..SerializerJson import SerializerJson


class DataStorage(object):
    __instance = None
    TYPE = "DataStorage"

    def __init__(self):
        self.units = {}
        self._loaded = False

    def __hash__(self):
        return id(self)

    @staticmethod
    def shared():
        if not DataStorage.__instance:
            DataStorage.__instance = DataStorage()
        return DataStorage.__instance
        pass

    def initialize_json(self, content):
        js = json.loads(content)
        self.deserialize_json(js)
        self._loaded = True
        pass

    def getDataUnit(self, name):
        if not self._loaded and name not in self.units:
            from .DataUnit import DataUnit
            self.units[name] = DataUnit()
            self.units[name].name = name
        return DataWrapper(self.units[name])
        pass

    def get_type(self):
        return DataStorage.TYPE
        pass

    def serialize_xml(self, serializer: SerializerXml):
        pass

    def deserialize_xml(self, serializer: DeserializerXml):
        pass

    def serialize_json(self, serializer: SerializerJson):
        pass

    def deserialize_json(self, dictionary):
        pass
