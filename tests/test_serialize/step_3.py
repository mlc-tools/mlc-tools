from generated_py.TestData import TestData
import xml.etree.ElementTree as ET
import json

data0 = TestData()

if True:  # MG_SERIALIZE_FORMAT == MG_XML:
    string = open('data.cpp.xml').read()
    root = ET.fromstring(string)
    data0.deserialize_xml(root)
else:
    js = json.load(open('data.cpp.json'))
    data0.deserialize_json(js)


data1 = TestData()
data1.initialize()

if data0.equal(data1):
    print('Ok')
else:
    print('Failed')
