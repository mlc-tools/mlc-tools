import xml.etree.ElementTree as ET
import json as JS

from tests.test_serializer.py.SerializerJson import SerializerJson
from tests.test_serializer.py.gen.AllTypes import AllTypes
from tests.test_serializer.py.gen.DataStorage import DataStorage
from tests.test_serializer.py.gen.TestEnum import TestEnum
from tests.test_serializer.py.tests_from_serialize_cpp import test_json, test_xml, test_all_types_xml
from tests.test_serializer.py.tests_from_serialize_cpp import test_all_types_json
from tests.test_serializer.py.tests_intrusive import test_intrusive

# test = AllTypes()
# test.initialize()
#
# serializer = SerializerJson({})
# serializer.serialize(test, "AllTypes")
# print(JS.dumps(serializer.json))
#
# test_dict = {test: test}
# serializer = SerializerJson({})
# serializer.serialize(test_dict, "AllTypes")
# print(JS.dumps(serializer.json))

test_intrusive()
test_xml()
test_all_types_xml()
test_json()
test_all_types_json()