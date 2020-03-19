import xml.etree.ElementTree as ET
import json as JS

from tests.test_serializer.py.SerializerJson import SerializerJson
from tests.test_serializer.py.gen.AllTypes import AllTypes

test = AllTypes()
test.initialize()

serializer = SerializerJson({})
serializer.serialize(test, "AllTypes")
print(JS.dumps(serializer.json))

test_dict = {test: test}
serializer = SerializerJson({})
serializer.serialize(test_dict, "AllTypes")
print(JS.dumps(serializer.json))
