from generated_py.TestData import TestData
import xml.etree.ElementTree as ET


data = TestData()
data.initialize()


root = ET.Element('data')
data.serialize(root)
string = ET.tostring(root)

open('data.py.xml', 'w').write(string)
