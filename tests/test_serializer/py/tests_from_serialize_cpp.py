import re
import xml.etree.ElementTree as ET

from tests.test_serializer.py.DeserializerJson import DeserializerJson
from tests.test_serializer.py.DeserializerXml import DeserializerXml
from tests.test_serializer.py.Meta import Meta
from tests.test_serializer.py.SerializerJson import SerializerJson
from tests.test_serializer.py.SerializerXml import SerializerXml
from tests.test_serializer.py.cpp_tests import JSON_TESTS, XML_TESTS
from tests.test_serializer.py.gen.AllTypes import AllTypes
from tests.test_serializer.py.gen.AllTypesChildren import AllTypesChildren
from tests.test_serializer.py.gen.DataStorage import DataStorage
from tests.test_serializer.py.gen.DataUnit import DataUnit
from tests.test_serializer.py.gen.DataWrapper import DataWrapper
from tests.test_serializer.py.gen.Point import Point
from tests.test_serializer.py.gen.TestEnum import TestEnum
from tests.test_serializer.py.gen.IntrusivePtr import make_intrusive, IntrusivePtr
from tests.test_serializer.py.gen.UnitType import UnitType
from tests.test_serializer.py.gen.common import serialize_command_to_json


def build_dict(parts, types, functor):
    if parts[0][0] in types:
        key = types[parts[0][0]]
    else:
        key = functor(parts[0][0])
    if parts[0][1] in types:
        value = types[parts[0][1]]
    else:
        value = functor(parts[0][1])
    return {key: value}


def get_object(description):
    parts = re.findall(r'map<(.+)\|(.+)>', description)
    types = {
        'int': 123,
        'bool': True,
        'float': 123.5,
        'std::string': '434312some_random',
        'TestEnum': TestEnum.value2,
        'const DataUnit*': DataStorage.shared().getDataUnit("unit1"),
        'AllTypesChildren': AllTypesChildren(),
        'intrusive_ptr<AllTypesChildren>': make_intrusive(AllTypesChildren),
        'std::vector<int>': [1, 2, 3, 4],
        'std::vector<float>': [1, 2],
        'std::vector<std::vector<bool>>': [[True, False], [False, True]],
        'std::map<int, int>': {1: 2, 2: 3},
        'std::vector<const DataUnit*>': [
            DataStorage.shared().getDataUnit("unit1"),
            DataStorage.shared().getDataUnit("unit1"),
        ],
        'std::vector<intrusive_ptr<AllTypesChildren>': [
            make_intrusive(AllTypesChildren),
            make_intrusive(AllTypesChildren),
        ],
        'std::vector<AllTypesChildren>': [
            AllTypesChildren(),
            AllTypesChildren()
        ]
    }
    return build_dict(parts, types, get_object)


def get_meta(description) -> Meta:
    parts = re.findall(r'map<(.+)\|(.+)>', description)
    types = {
        'int': int,
        'bool': bool,
        'float': float,
        'std::string': str,
        'TestEnum': TestEnum,
        'const DataUnit*': Meta(DataWrapper, DataUnit),
        'AllTypesChildren': AllTypesChildren,
        'intrusive_ptr<AllTypesChildren>': Meta(IntrusivePtr, AllTypesChildren),
        'std::vector<int>': Meta(list, int),
        'std::vector<float>': Meta(list, float),
        'std::vector<std::vector<bool>>': Meta(list, Meta(list, bool)),
        'std::map<int, int>': Meta(dict, int, int),
        'std::vector<const DataUnit*>': Meta(list, Meta(DataWrapper, DataUnit)),
        'std::vector<intrusive_ptr<AllTypesChildren>': Meta(list, Meta(IntrusivePtr, AllTypesChildren)),
        'std::vector<AllTypesChildren>': Meta(list, AllTypesChildren)
    }
    (k, v), = build_dict(parts, types, get_object).items()
    return Meta(dict, k, v)


def compare_json(counter, description, orig, serialized, total):
    if orig != serialized:
        counter += 1
        print('-------')
        print("Failed Json: ", description)
        print('Orig:', orig)
        print('Curr:', serialized)
        print('{}/{}'.format(counter, total))
        exit(1)
    return counter


def compare_xml(counter, description, orig, serialized, total):

    if ET.tostring(orig) != ET.tostring(serialized):
        counter += 1
        print('-------')
        print("Failed Xml: ", description)
        print('Orig:', ET.tostring(orig).decode())
        print('Curr:', ET.tostring(serialized).decode())
        print('{}/{}'.format(counter, total))
        exit(1)
    return counter


def test_json():
    counter = 0
    for description in JSON_TESTS:
        obj = get_object(description)
        meta = get_meta(description)
        orig = JSON_TESTS[description]

        try:
            serializer = SerializerJson({})
            serializer.serialize(obj, 'object')
            counter = compare_json(counter, description, orig, serializer.json, len(JSON_TESTS))

            deserializer = DeserializerJson(serializer.json)
            obj = deserializer.deserialize('object', meta)
            serializer = SerializerJson({})
            serializer.serialize(obj, 'object')
            counter = compare_json(counter, description, orig, serializer.json, len(JSON_TESTS))
        except AssertionError as e:
            print(e)
            counter = compare_json(counter, description, orig, {}, len(JSON_TESTS))
    print('Success Json: {}/{}'.format(len(JSON_TESTS) - counter, len(JSON_TESTS)))


def test_xml():
    counter = 0
    for description in XML_TESTS:
        orig = ET.fromstring(XML_TESTS[description])

        try:
            obj = get_object(description)
            meta = get_meta(description)
            serializer = SerializerXml(ET.Element('root'))
            serializer.serialize(obj, 'object')
            counter = compare_xml(counter, description, orig, serializer.node, len(XML_TESTS))

            deserializer = DeserializerXml(serializer.node)
            obj = deserializer.deserialize('object', meta)
            serializer = SerializerXml(ET.Element('root'))
            serializer.serialize(obj, 'object')
            counter = compare_xml(counter, description, orig, serializer.node, len(XML_TESTS))
        except AssertionError as e:
            print(e)
            counter = compare_xml(counter, description, orig, {})
        except IndexError as e:
            print(e)
            print('  - Cannot build object or meta for description: [%s]' % description)
            exit(1)
        # except TypeError as e:
        #     print('  -', e)
        #     print('  - Cannot save xml for description: [%s]' % description)
        #     exit(1)
    print('Success Xml: {}/{}'.format(len(XML_TESTS) - counter, len(XML_TESTS)))


def test_all_types_json():
    obj = AllTypes()
    obj.initialize()
    serializer = SerializerJson({})
    serializer.serialize(obj, 'object')
    orig = serializer.json

    deserializer = DeserializerJson(serializer.json)
    obj = deserializer.deserialize('object', AllTypes)
    serializer = SerializerJson({})
    serializer.serialize(obj, 'object')
    compare_json(0, 'AllTypes Json', orig, serializer.json, 1)
    print('Success AllTypes Json: {}/{}'.format(1, 1))


def test_all_types_xml():
    obj = AllTypes()
    obj.initialize()
    serializer = SerializerXml(ET.Element('root'))
    serializer.serialize(obj, 'object')
    orig = ET.fromstring(ET.tostring(serializer.node))

    deserializer = DeserializerXml(serializer.node)
    obj = deserializer.deserialize('object', AllTypes)
    serializer = SerializerXml(ET.Element('root'))
    serializer.serialize(obj, 'object')
    compare_xml(0, 'AllTypes Json', orig, serializer.node, 1)
    print('Success AllTypes Xml: {}/{}'.format(1, 1))


def test_deserialize_all_types_from_min_string_xml():
    deserializer = DeserializerXml(ET.fromstring('<object int_value0="5" />'))
    obj = AllTypes()
    obj.deserialize_xml(deserializer)
    assert obj.int_value0 == 5


def test_deserialize_all_types_from_min_string_json():
    deserializer = DeserializerJson({"int_value0": 10})
    obj = AllTypes()
    obj.deserialize_json(deserializer)
    assert obj.int_value0 == 10


def test_empty_enum_deserialize_xml():
    string = '<unit/>'
    deserializer = DeserializerXml(ET.fromstring(string))
    data = DataUnit()
    data.deserialize_xml(deserializer)
    assert data.unit_type == UnitType.defend
    assert isinstance(data.items, dict)


def test_empty_enum_deserialize_json():
    deserializer = DeserializerJson({})
    data = DataUnit()
    data.deserialize_json(deserializer)
    assert data.unit_type == UnitType.attack
    assert isinstance(data.items, dict)


def test_serialize_list_points_to_json():
    unit = DataUnit()
    unit.points.append(Point())
    unit.points[-1].row = 1
    unit.points[-1].col = 2
    js = serialize_command_to_json(unit)
    assert js == '{"DataUnit": {"points": [{"row": 1, "col": 2}]}}'
