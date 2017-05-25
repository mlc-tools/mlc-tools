from WriterCpp import WriterCpp
from WriterCpp import SERIALIZATION as S
from WriterCpp import DESERIALIZATION as D
from Object import Object
from Class import Class
from DataStorageCreators import DataStorageCppJson

class WriterCppSerializatorJson(WriterCpp):
    def __init__(self, out_directory, parser):
        WriterCpp.__init__(self, out_directory, parser)

    def create_serialization_patterns(self):
        self.simple_types = ["int", "float", "bool", "string"]
        self.serialize_formats = self.parser.parse_serialize_protocol('protocol_cpp_json.txt')

    def get_serialization_object_arg(self, serialization_type):
        if serialization_type == S:
            return ["json", "Json::Value&"]
        if serialization_type == D:
            return ["json", "const Json::Value&"]
        return ["", ""]

    def get_behavior_call_format(self):
        return "{0}::{1}(json);"

    def build_map_serialization(self, obj_name, obj_type, obj_value, obj_is_pointer, obj_template_args):
        key = obj_template_args[0]
        value = obj_template_args[1]
        key_type = key.name if isinstance(key, Class) else key.type
        value_type = value.name if isinstance(value, Class) else value.type
        string = '''
        auto& map_{0} = json["{0}"];
        for(auto pair : {0})
        {3}
            auto& json = map_{0}[map_{0}.size()];

            auto& key = pair.first; {1}

            auto& value = pair.second; {2}
        {4}
        '''
        _value_is_pointer = value.is_pointer
        a0 = obj_name
        a1 = self._build_serialize_operation("key", key_type, None, False, [], S, key.is_link)
        a2 = self._build_serialize_operation("value", value_type, None, _value_is_pointer, [], S, value.is_link)
        return string.format(a0, a1, a2, '{', '}')

    def build_map_deserialization(self, obj_name, obj_type, obj_value, obj_is_pointer, obj_template_args):
        key = obj_template_args[0]
        value = obj_template_args[1]
        key_type = key.name if isinstance(key, Class) else key.type
        value_type = value.name if isinstance(value, Class) else value.type
        string = '''
        auto& map_{0} = json["{0}"];
        auto size_{0}= map_{0}.size();
        for(unsigned int i = 0; i < size_{0}; ++i)
        {5}
            auto& json = map_{0}[i];

            {3} key; {1}

            {4} value; {2}

            {0}[key] = value;
        {6}
        '''
        if key.is_link:
            key_str = 'const {}* key(nullptr);'.format(key_type)
        elif key.is_pointer:
            key_str = 'auto key = make_intrusive<{}>();'.format(key_type)
        else:
            key_str = '{} key;'.format(key_type)

        _value_is_pointer = value.is_pointer if isinstance(value, Object) else False
        a0 = obj_name
        a1 = self._build_serialize_operation("key", key_type, None, False, [], D, key.is_link)
        a2 = self._build_serialize_operation("value", value_type, None, _value_is_pointer, [], D, value.is_link)
        a3 = key_str
        a4 = value_type
        if value.is_pointer:
            a4 = "IntrusivePtr<{}>".format(value_type)
        return string.format(a0, a1, a2, a3, a4, '{', '}')

    def create_data_storage_class(self, name, classes):
        return DataStorageCppJson(name, classes, self.parser)
