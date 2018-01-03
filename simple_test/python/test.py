from mg.DataUnit import DataUnit
from mg.DataStorage import DataStorage

content = open('assets/data.xml').read()
DataStorage.shared().initialize(content)

result = True
result = DataUnit.tests() and result

print result
exit(0 if result else -1)