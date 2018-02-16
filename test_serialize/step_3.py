from generated_py.TestData import TestData
import xml.etree.ElementTree as ET


string = open('data.cpp.xml').read()
root = ET.fromstring(string)

data0 = TestData()
data0.deserialize(root)

data1 = TestData()
data1.initialize()

if data0.equal(data1):
    print 'Ok'
else:
    print 'Failed'
