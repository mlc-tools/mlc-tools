from WriterCpp import WriterCpp
from WriterCpp import SERIALIZATION
from DataStorageCreators import DataStorageCppJson


class WriterCppSerializatorJson(WriterCpp):
    def __init__(self, out_directory, parser):
        WriterCpp.__init__(self, out_directory, parser)

    def create_serialization_patterns(self):
        self.simple_types = ["int", "float", "bool", "string"]
        self.serialize_formats = self.parser.parse_serialize_protocol('protocol_cpp_json.txt')

    def get_serialization_object_arg(self, serialization_type):
        if serialization_type == SERIALIZATION:
            return ["json", "Json::Value&"]
        else:
            return ["json", "const Json::Value&"]

    def get_behavior_call_format(self):
        return "{0}::{1}(json);"

    def create_data_storage_class(self, name, classes):
        return DataStorageCppJson(name, classes, self.parser)
