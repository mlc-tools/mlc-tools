import re

from tests.test_serializer.py.DeserializerJson import DeserializerJson, Meta
from tests.test_serializer.py.SerializerJson import SerializerJson
from tests.test_serializer.py.cpp_tests import TESTS
from tests.test_serializer.py.gen.AllTypes import AllTypes
from tests.test_serializer.py.gen.AllTypesChildren import AllTypesChildren
from tests.test_serializer.py.gen.DataStorage import DataStorage
from tests.test_serializer.py.gen.DataUnit import DataUnit
from tests.test_serializer.py.gen.DataWrapper import DataWrapper
from tests.test_serializer.py.gen.TestEnum import TestEnum
from tests.test_serializer.py.gen.intrusive_ptr import make_intrusive, IntrusivePtr


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
        'std::vector<std::vector<bool>>': [[True, False], [False, True]],
        'std::map<int, int>': {1: 2, 2: 3},
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
        'std::vector<std::vector<bool>>': Meta(list, Meta(list, bool)),
        'std::map<int, int>': Meta(dict, int, int)
    }
    (k, v), = build_dict(parts, types, get_object).items()
    return Meta(dict, k, v)


def compare(counter, description, orig, serialized):
    if orig != serialized:
        counter += 1
        print('-------')
        print("Failed: ", description)
        print('Orig:', orig)
        print('Curr:', serialized)
        print('{}/{}'.format(counter, len(TESTS)))
        exit(1)
    return counter


def test_cpp():
    counter = 0
    for description in TESTS:
        obj = get_object(description)
        meta = get_meta(description)
        orig = TESTS[description]

        try:
            serializer = SerializerJson({})
            serializer.serialize(obj, 'object')
            counter = compare(counter, description, orig, serializer.json)

            deserializer = DeserializerJson(serializer.json)
            obj = deserializer.deserialize('object', meta)
            serializer = SerializerJson({})
            serializer.serialize(obj, 'object')
            counter = compare(counter, description, orig, serializer.json)
        except AssertionError as e:
            print(e)
            counter = compare(counter, description, orig, {})

    print('Success: {}/{}'.format(len(TESTS) - counter, len(TESTS)))


def test_all_types():
    obj = AllTypes()
    obj.initialize()
    serializer = SerializerJson({})
    serializer.serialize(obj, 'object')
    orig = serializer.json

    deserializer = DeserializerJson(serializer.json)
    obj = deserializer.deserialize('object', AllTypes)
    serializer = SerializerJson({})
    serializer.serialize(obj, 'object')
    compare(0, 'AllTypes', orig, serializer.json)
