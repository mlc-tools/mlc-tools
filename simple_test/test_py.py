from generated_py.AllTests import AllTests
from generated_py.DataStorage import DataStorage
import os.path as fs

file = fs.abspath(fs.dirname(__file__)) + '/assets/data.json'
content = open(file).read()
DataStorage.shared().initialize(content)


class Loger:

    def add_result(self, result, message):
        print '{}: {}'.format(message, result)
        return result
loger = Loger()

result = True
result = AllTests.run(loger) and result

print result
exit(0 if result else -1)
