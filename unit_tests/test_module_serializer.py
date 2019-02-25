import unittest

import os
import sys
import inspect

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/..'))
from mlc_tools.core.object import Object, Objects
from mlc_tools.core.class_ import *
from mlc_tools.core.function import *
from mlc_tools.base.model import Model
from mlc_tools.base.parser import Parser
from mlc_tools.module_cpp.serializer import Serializer as SerializerCpp


class TestCppSerializer(unittest.TestCase):

    def test_list_list_bool(self):
        serializer = SerializerCpp()
        serializer.model = Model()
        serializer.model.parser = Parser(serializer.model)
        serializer.load_protocols()

        obj = Parser.create_object('list<list<bool>> field')
        result = serializer.build_serialize_operation(obj, 0, 'json')

        source = '''auto& arr_field = json["field"];
int i_field=0;
for(auto& t : field)
{
    t.serialize_json(arr_field[i_field++]);
}

'''
        self.assertEqual(result, source)