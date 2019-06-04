from generated_py.TestData import TestData
import xml.etree.ElementTree as ET
import json


data = TestData()
data.initialize()

if True:  # MG_SERIALIZE_FORMAT == MG_XML:
    root = ET.Element('data')
    data.serialize_xml(root)
    string = str(ET.tostring(root))
    string = string.strip()
    string = string.replace('\\n', '\n')
    string = string.replace('\\t', '\t')
    if string.startswith("b'"):
        string = string[2:]
    if string.endswith("'"):
        string = string[0:-1]
    open('data.py.xml', 'w').write(str(string))
else:
    dict_ = {}
    data.serialize_json(dict_)
    string = json.dumps(dict_, indent=1)
    open('data.py.json', 'w').write(string)
