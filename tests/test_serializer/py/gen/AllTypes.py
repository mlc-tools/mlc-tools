# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import json

from .AllTypesChildren import AllTypesChildren
from .common import *
from ..DeserializerXml import DeserializerXml
from ..SerializerJson import SerializerJson
from ..DeserializerJson import DeserializerJson
from ..Meta import Meta
from tests.test_serializer.py.gen.IntrusivePtr import IntrusivePtr, make_intrusive
from .TestEnum import TestEnum
from ..SerializerXml import SerializerXml


class AllTypes(object):
    TYPE = "AllTypes"
    __slots__ = ["int_value0", "int_value1", "int_value2", "float_value0", "float_value1", "bool_value0", "bool_value1", "str_value0", "str_value1", "int_list", "float_list", "bool_list", "string_list", "int_string_map", "float_string_map", "bool_string_map", "string_string_map", "string_int_map", "string_float_map", "string_bool_map", "object", "object_ptr", "object_list", "object_ptr_list", "object_map", "object_ptr_map", "enum_list", "enum_map"]

    def __init__(self, arg=None):
        self.int_value0 = 0 if arg is None else arg
        self.int_value1 = 0
        self.int_value2 = None
        self.float_value0 = 0
        self.float_value1 = 0.0
        self.bool_value0 = True
        self.bool_value1 = False
        self.str_value0 = ""
        self.str_value1 = ""
        self.int_list = []
        self.float_list = []
        self.bool_list = []
        self.string_list = []
        self.int_string_map = {}
        self.float_string_map = {}
        self.bool_string_map = {}
        self.string_string_map = {}
        self.string_int_map = {}
        self.string_float_map = {}
        self.string_bool_map = {}
        from .AllTypesChildren import AllTypesChildren
        self.object = AllTypesChildren()
        self.object_ptr = 0
        self.object_list = []
        self.object_ptr_list = []
        self.object_map = {}
        self.object_ptr_map = {}
        self.enum_list = []
        self.enum_map = {}

    def __hash__(self):
        return id(self)

    def initialize(self):
        from .AllTypesChildren import AllTypesChildren
        self.int_value0 = 1
        self.int_value1 = 1
        self.int_value2 = 0
        self.float_value0 = 1.0
        self.float_value1 = 1.0
        self.bool_value0 = False
        self.bool_value1 = True
        self.str_value0 = "test_string"
        self.str_value1 = "test_string"
        self.int_list.append(0)
        self.int_list.append(1)
        self.float_list.append(0.0)
        self.float_list.append(1.0)
        self.bool_list.append(True)
        self.bool_list.append(True)
        self.string_list.append("0")
        self.string_list.append("1")
        self.int_string_map[0] = "0"
        self.int_string_map[1] = "1"
        self.bool_string_map[True] = "0"
        self.bool_string_map[False] = "1"
        self.float_string_map[0.0] = "0"
        self.float_string_map[1.0] = "1"
        self.string_string_map["0"] = "0"
        self.string_string_map["1"] = "1"
        self.string_int_map["0"] = 0
        self.string_int_map["1"] = 1
        self.string_bool_map["0"] = True
        self.string_bool_map["1"] = False
        self.string_float_map["0"] = 0.0
        self.string_float_map["1"] = 1.0
        self.string_string_map["0"] = "0"
        self.string_string_map["1"] = "1"
        self.object.value = 0
        self.object_ptr = make_intrusive(AllTypesChildren)
        self.object_ptr.value = 0
        self.object_list.extend([self.object, self.object])
        self.enum_list.append(TestEnum.value1)
        self.enum_list.append(TestEnum.value2)
        self.enum_map[TestEnum.value1] = 1
        self.enum_map[TestEnum.value2] = 2
        pass

    @staticmethod
    def tests(logger):
        result = True
        inst = AllTypes()
        inst.initialize()
        return result
        pass

    def __eq__(self, rhs):
        result = True
        result = result and self.int_value0 == rhs.int_value0
        result = result and self.int_value1 == rhs.int_value1
        result = result and self.int_value2 == rhs.int_value2
        result = result and self.float_value0 == rhs.float_value0
        result = result and self.float_value1 == rhs.float_value1
        result = result and self.bool_value0 == rhs.bool_value0
        result = result and self.bool_value1 == rhs.bool_value1
        result = result and self.str_value0 == rhs.str_value0
        result = result and self.str_value1 == rhs.str_value1
        result = result and self.int_list == rhs.int_list
        result = result and self.float_list == rhs.float_list
        result = result and self.bool_list == rhs.bool_list
        result = result and self.string_list == rhs.string_list
        result = result and self.int_string_map == rhs.int_string_map
        result = result and self.float_string_map == rhs.float_string_map
        result = result and self.bool_string_map == rhs.bool_string_map
        result = result and self.string_string_map == rhs.string_string_map
        result = result and self.string_int_map == rhs.string_int_map
        result = result and self.string_float_map == rhs.string_float_map
        result = result and self.string_bool_map == rhs.string_bool_map
        result = result and self.object == rhs.object
        result = result and ((self.object_ptr is None and rhs.object_ptr is None) or (self.object_ptr is not None and rhs.object_ptr is not None and self.object_ptr == rhs.object_ptr))
        result = result and self.object_list == rhs.object_list
        result = result and self.object_ptr_list == rhs.object_ptr_list
        result = result and self.object_map == rhs.object_map
        result = result and self.object_ptr_map == rhs.object_ptr_map
        result = result and self.enum_list == rhs.enum_list
        result = result and self.enum_map == rhs.enum_map
        return result
        pass

    def __ne__(self, rhs):
        return not (self == rhs)
        pass

    def get_type(self):
        return AllTypes.TYPE
        pass

    def serialize_xml(self, serializer: SerializerXml):
        serializer.serialize(self.int_value0, 'int_value0')
        serializer.serialize(self.int_value1, 'int_value1')
        serializer.serialize(self.int_value2, 'int_value2')
        serializer.serialize(self.float_value0, 'float_value0')
        serializer.serialize(self.float_value1, 'float_value1')
        serializer.serialize(self.bool_value0, 'bool_value0', True)
        serializer.serialize(self.bool_value1, 'bool_value1', False)
        serializer.serialize(self.str_value0, 'str_value0')
        serializer.serialize(self.str_value1, 'str_value1')
        serializer.serialize(self.int_list, 'int_list')
        serializer.serialize(self.float_list, 'float_list')
        serializer.serialize(self.bool_list, 'bool_list')
        serializer.serialize(self.string_list, 'string_list')
        serializer.serialize(self.int_string_map, 'int_string_map')
        serializer.serialize(self.float_string_map, 'float_string_map')
        serializer.serialize(self.bool_string_map, 'bool_string_map')
        serializer.serialize(self.string_string_map, 'string_string_map')
        serializer.serialize(self.string_int_map, 'string_int_map')
        serializer.serialize(self.string_float_map, 'string_float_map')
        serializer.serialize(self.string_bool_map, 'string_bool_map')
        serializer.serialize(self.object, 'object')
        serializer.serialize(self.object_ptr, 'object_ptr')
        serializer.serialize(self.object_list, 'object_list')
        serializer.serialize(self.object_ptr_list, 'object_ptr_list')
        serializer.serialize(self.object_map, 'object_map')
        serializer.serialize(self.object_ptr_map, 'object_ptr_map')
        serializer.serialize(self.enum_list, 'enum_list')
        serializer.serialize(self.enum_map, 'enum_map')

    def deserialize_xml(self, deserializer: DeserializerXml):
        self.int_value0 = deserializer.deserialize('int_value0', int, 0)
        self.int_value1 = deserializer.deserialize('int_value1', int, 1)
        self.int_value2 = deserializer.deserialize('int_value2', int)
        self.float_value0 = deserializer.deserialize('float_value0', float, 0)
        self.float_value1 = deserializer.deserialize('float_value1', float, 0.0)
        self.bool_value0 = deserializer.deserialize('bool_value0', bool, True)
        self.bool_value1 = deserializer.deserialize('bool_value1', bool, False)
        self.str_value0 = deserializer.deserialize('str_value0', str, '')
        self.str_value1 = deserializer.deserialize('str_value1', str, '')
        self.int_list = deserializer.deserialize('int_list', Meta(list, int))
        self.float_list = deserializer.deserialize('float_list', Meta(list, float))
        self.bool_list = deserializer.deserialize('bool_list', Meta(list, bool))
        self.string_list = deserializer.deserialize('string_list', Meta(list, str))
        self.int_string_map = deserializer.deserialize('int_string_map', Meta(dict, int, str))
        self.float_string_map = deserializer.deserialize('float_string_map', Meta(dict, float, str))
        self.bool_string_map = deserializer.deserialize('bool_string_map', Meta(dict, bool, str))
        self.string_string_map = deserializer.deserialize('string_string_map', Meta(dict, str, str))
        self.string_int_map = deserializer.deserialize('string_int_map', Meta(dict, str, int))
        self.string_float_map = deserializer.deserialize('string_float_map', Meta(dict, str, float))
        self.string_bool_map = deserializer.deserialize('string_bool_map', Meta(dict, str, bool))
        self.object = deserializer.deserialize('object', AllTypesChildren)
        self.object_ptr = deserializer.deserialize('object_ptr', Meta(IntrusivePtr, AllTypesChildren))
        self.object_list = deserializer.deserialize('object_list', Meta(list, AllTypesChildren))
        self.object_ptr_list = deserializer.deserialize('object_ptr_list', Meta(list, Meta(IntrusivePtr, AllTypesChildren)))
        self.object_map = deserializer.deserialize('object_map', Meta(dict, str, AllTypesChildren))
        self.object_ptr_map = deserializer.deserialize('object_ptr_map', Meta(dict, str, Meta(IntrusivePtr, AllTypesChildren)))
        self.enum_list = deserializer.deserialize('enum_list', Meta(list, TestEnum))
        self.enum_map = deserializer.deserialize('enum_map', Meta(dict, TestEnum, int))


    def serialize_json(self, serializer: SerializerJson):
        serializer.serialize(self.int_value0, 'int_value0')
        serializer.serialize(self.int_value1, 'int_value1')
        # serializer.serialize(self.int_value2, 'int_value2')
        serializer.serialize(self.float_value0, 'float_value0')
        serializer.serialize(self.float_value1, 'float_value1')
        serializer.serialize(self.bool_value0, 'bool_value0')
        serializer.serialize(self.bool_value1, 'bool_value1')
        serializer.serialize(self.str_value0, 'str_value0')
        serializer.serialize(self.str_value1, 'str_value1')
        serializer.serialize(self.int_list, 'int_list')
        serializer.serialize(self.float_list, 'float_list')
        serializer.serialize(self.bool_list, 'bool_list')
        serializer.serialize(self.string_list, 'string_list')
        serializer.serialize(self.int_string_map, 'int_string_map')
        serializer.serialize(self.float_string_map, 'float_string_map')
        serializer.serialize(self.bool_string_map, 'bool_string_map')
        serializer.serialize(self.string_string_map, 'string_string_map')
        serializer.serialize(self.string_int_map, 'string_int_map')
        serializer.serialize(self.string_float_map, 'string_float_map')
        serializer.serialize(self.string_bool_map, 'string_bool_map')
        serializer.serialize(self.object, 'object')
        serializer.serialize(self.object_ptr, 'object_ptr')
        serializer.serialize(self.object_list, 'object_list')
        serializer.serialize(self.object_ptr_list, 'object_ptr_list')
        serializer.serialize(self.object_map, 'object_map')
        serializer.serialize(self.object_ptr_map, 'object_ptr_map')
        serializer.serialize(self.enum_list, 'enum_list')
        serializer.serialize(self.enum_map, 'enum_map')

    def deserialize_json(self, deserializer: DeserializerJson):
        self.int_value0 = deserializer.deserialize('int_value0', int, 0)
        self.int_value1 = deserializer.deserialize('int_value1', int, 1)
        self.int_value2 = deserializer.deserialize('int_value2', int)
        self.float_value0 = deserializer.deserialize('float_value0', float, 0)
        self.float_value1 = deserializer.deserialize('float_value1', float, 0.0)
        self.bool_value0 = deserializer.deserialize('bool_value0', bool, True)
        self.bool_value1 = deserializer.deserialize('bool_value1', bool, False)
        self.str_value0 = deserializer.deserialize('str_value0', str, '')
        self.str_value1 = deserializer.deserialize('str_value1', str, '')
        self.int_list = deserializer.deserialize('int_list', Meta(list, int))
        self.float_list = deserializer.deserialize('float_list', Meta(list, float))
        self.bool_list = deserializer.deserialize('bool_list', Meta(list, bool))
        self.string_list = deserializer.deserialize('string_list', Meta(list, str))
        self.int_string_map = deserializer.deserialize('int_string_map', Meta(dict, int, str))
        self.float_string_map = deserializer.deserialize('float_string_map', Meta(dict, float, str))
        self.bool_string_map = deserializer.deserialize('bool_string_map', Meta(dict, bool, str))
        self.string_string_map = deserializer.deserialize('string_string_map', Meta(dict, str, str))
        self.string_int_map = deserializer.deserialize('string_int_map', Meta(dict, str, int))
        self.string_float_map = deserializer.deserialize('string_float_map', Meta(dict, str, float))
        self.string_bool_map = deserializer.deserialize('string_bool_map', Meta(dict, str, bool))
        self.object = deserializer.deserialize('object', AllTypesChildren)
        self.object_ptr = deserializer.deserialize('object_ptr', Meta(IntrusivePtr, AllTypesChildren))
        self.object_list = deserializer.deserialize('object_list', Meta(list, AllTypesChildren))
        self.object_ptr_list = deserializer.deserialize('object_ptr_list', Meta(list, Meta(IntrusivePtr, AllTypesChildren)))
        self.object_map = deserializer.deserialize('object_map', Meta(dict, str, AllTypesChildren))
        self.object_ptr_map = deserializer.deserialize('object_ptr_map', Meta(dict, str, Meta(IntrusivePtr, AllTypesChildren)))
        self.enum_list = deserializer.deserialize('enum_list', Meta(list, TestEnum))
        self.enum_map = deserializer.deserialize('enum_map', Meta(dict, TestEnum, int))
