from generated_py.TestData import TestData
from generated_py.config import *
import xml.etree.ElementTree as ET
import json


data = TestData()
data.initialize()

if MG_SERIALIZE_FORMAT == MG_XML:
    root = ET.Element('data')
    data.serialize(root)
    string = ET.tostring(root)
    open('data.py.xml', 'w').write(string)
else:
    dict_ = {}
    data.serialize(dict_)
    string = json.dumps(dict_, indent=1)
    open('data.py.json', 'w').write(string)
