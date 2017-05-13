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
        self.serialize_formats[S]['simple'] = []
        self.serialize_formats[S]['simple'].append('if({0} != {2}) \n{3}\n::set(json,"{0}",{0});\n{4}')
        self.serialize_formats[S]['simple'].append('::set(json,"{0}",{0});')
        self.serialize_formats[D]['simple'] = []
        self.serialize_formats[D]['simple'].append('''if(json.isMember("{0}"))
            {3}
                {0} = ::get<{1}>(json["{0}"]);
            {4}
            else
            {3}
                {0} = {2};
            {4}''')
        self.serialize_formats[D]['simple'].append('{0} = ::get<{1}>(json["{0}"]);')

        self.serialize_formats[S]['serialized'] = []
        self.serialize_formats[S]['serialized'].append(
            'static_assert(0, "field "{0}" not should have a initialize value");'
        )
        self.serialize_formats[S]['serialized'].append('{0}.serialize(json["{0}"]);')
        self.serialize_formats[D]['serialized'] = []
        self.serialize_formats[D]['serialized'].append(
            'static_assert(0, "field "{0}" not should have a initialize value");'
        )
        self.serialize_formats[D]['serialized'].append('{0}.deserialize(json["{0}"]);')

        self.serialize_formats[S]['pointer'] = []
        self.serialize_formats[S]['pointer'].append(
            'static_assert(0, "field "{0}" not should have a initialize value");'
        )
        self.serialize_formats[S]['pointer'].append('''
            if({0})
            {3}
                {0}->serialize(json["{0}"][{0}->get_type()]);
            {4}''')
        self.serialize_formats[D]['pointer'] = []
        self.serialize_formats[D]['pointer'].append(
            'static_assert(0, "field "{0}" not should have a initialize value");'
        )
        self.serialize_formats[D]['pointer'].append('''
            if(json.isMember("{0}"))
            {3}
                auto type_{0} = json["{0}"].getMemberNames()[0];
                {0} = Factory::shared().build<{1}>(type_{0});
                {0}->deserialize(json["{0}"][type_{0}]);
            {4}''')

        self.serialize_formats[S]['list<simple>'] = []
        self.serialize_formats[S]['list<simple>'].append(
            'static_assert(0, "list "{0}" not should have a initialize value");'
        )
        self.serialize_formats[S]['list<simple>'].append('''
            {3}
                auto& arr_{0} = json["{0}"];
                size_t i=0;
                for(auto& t : {0})
                ::set(arr_{0}[i++], t);
            {4}''')
        self.serialize_formats[D]['list<simple>'] = []
        self.serialize_formats[D]['list<simple>'].append(
            'static_assert(0, "list "{0}" not should have a initialize value");'
        )
        self.serialize_formats[D]['list<simple>'].append('''
            auto& arr_{0} = json["{0}"];
            for(size_t i = 0; i < arr_{0}.size(); ++i)
            {3}
                {0}.emplace_back();
                {0}.back() = ::get<{5}>(arr_{0}[i]);
            {4};
            ''')

        self.serialize_formats[S]['serialized_list'] = []
        self.serialize_formats[S]['serialized_list'].append(
            'static_assert(0, "list "{0}" not should have a initialize value");'
        )
        self.serialize_formats[S]['serialized_list'].append('''
            {3}
                auto& arr_{0} = json["{0}"];
                size_t i=0;
                for(auto& t : {0})
                {3}
                    t.serialize(arr_{0}[i++]);
                {4}
            {4}''')
        self.serialize_formats[D]['serialized_list'] = []
        self.serialize_formats[D]['serialized_list'].append(
            'static_assert(0, "list "{0}" not should have a initialize value");'
        )
        self.serialize_formats[D]['serialized_list'].append('''
            auto& arr_{0} = json["{0}"];
            for(size_t i = 0; i < arr_{0}.size(); ++i)
            {3}
                {0}.emplace_back();
                {0}.back().deserialize(arr_{0}[i]);
            {4}''')

        self.serialize_formats[S]['pointer_list'] = []
        self.serialize_formats[S]['pointer_list'].append(
            'static_assert(0, "list "{0}" not should have a initialize value");'
        )
        self.serialize_formats[S]['pointer_list'].append('''
            auto& arr_{0} = json["{0}"];
            for(auto& t : {0})
            {3}
                auto index = arr_{0}.size();
                t->serialize(arr_{0}[index][t->get_type()]);
            {4}''')
        self.serialize_formats[D]['pointer_list'] = []
        self.serialize_formats[D]['pointer_list'].append(
            'static_assert(0, "list "{0}" not should have a initialize value");'
        )
        self.serialize_formats[D]['pointer_list'].append('''
            auto& arr_{0} = json["{0}"];
            auto size_{0} = arr_{0}.size();
            for(size_t i = 0; i < size_{0}; ++i)
            {3}
                assert(arr_{0}[i].size() == 1);
                auto type = arr_{0}[i].getMemberNames()[0];
                auto obj = Factory::shared().build<{5}>(type);
                {0}.emplace_back(obj);
                {0}.back()->deserialize(arr_{0}[i][type]);
            {4}''')

        self.serialize_formats[S]['link'] = []
        self.serialize_formats[S]['link'].append('')
        self.serialize_formats[S]['link'].append('::set(json,"{0}",{0}->name);')
        self.serialize_formats[D]['link'] = []
        self.serialize_formats[D]['link'].append('')
        self.serialize_formats[D]['link'].append('{0} = DataStorage::shared().get<{1}>(::get<std::string>(json["{0}"]));')

        self.serialize_formats[S]['list<link>'] = []
        self.serialize_formats[S]['list<link>'].append('')
        self.serialize_formats[S]['list<link>'].append('''
            auto& arr_{0} = json["{0}"];
            for(auto& item : {0})
            {3}
                auto index = arr_{0}.size();
                arr_{0}.append(item->name);
            {4}
            ''')
        self.serialize_formats[D]['list<link>'] = []
        self.serialize_formats[D]['list<link>'].append('')
        self.serialize_formats[D]['list<link>'].append('''
            auto& arr_{0} = json["{0}"];
            for(auto item : arr_{0})
            {3}
                auto name = ::get<std::string>(item);
                auto data = DataStorage::shared().get<{5}>(name);
                {0}.push_back(data);
            {4}
        ''')

        self.simple_types = ["int", "float", "bool", "string"]
        for i in range(2):
            for type_ in self.simple_types:
                self.serialize_formats[i][type_] = []
                self.serialize_formats[i][type_].append(self.serialize_formats[i]["simple"][0])
                self.serialize_formats[i][type_].append(self.serialize_formats[i]["simple"][1])
                list_type = "list<{0}>".format(type_)
                self.serialize_formats[i][list_type] = []
                self.serialize_formats[i][list_type].append(self.serialize_formats[i]["list<simple>"][0])
                self.serialize_formats[i][list_type].append(self.serialize_formats[i]["list<simple>"][1])

            self.serialize_formats[i]["list<serialized>"] = []
            self.serialize_formats[i]["list<serialized>"].append(self.serialize_formats[i]["serialized_list"][0])
            self.serialize_formats[i]["list<serialized>"].append(self.serialize_formats[i]["serialized_list"][1])

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
        a1 = self._build_serialize_operation("key", key_type, None, False, [], S)
        a2 = self._build_serialize_operation("value", value_type, None, _value_is_pointer, [], S)
        return string.format(a0, a1, a2, '{', '}')

    def build_map_deserialization(self, obj_name, obj_type, obj_value, obj_is_pointer, obj_template_args):
        key = obj_template_args[0]
        value = obj_template_args[1]
        key_type = key.name if isinstance(key, Class) else key.type
        value_type = value.name if isinstance(value, Class) else value.type
        string = '''
        auto& map_{0} = json["{0}"];
        auto size_{0}= map_{0}.size();
        for(size_t i = 0; i < size_{0}; ++i)
        {5}
            auto& json = map_{0}[i];

            {3} key; {1}

            {4} value; {2}

            {0}[key] = value;
        {6}
        '''
        _value_is_pointer = value.is_pointer if isinstance(value, Object) else False
        a0 = obj_name
        a1 = self._build_serialize_operation("key", key_type, None, False, [], D)
        a2 = self._build_serialize_operation("value", value_type, None, _value_is_pointer, [], D)
        a3 = key_type
        a4 = value_type
        if value.is_pointer:
            a4 = "IntrusivePtr<{}>".format(value_type)
        return string.format(a0, a1, a2, a3, a4, '{', '}')

    def create_data_storage_class(self, name, classes):
        return DataStorageCppJson(name, classes)
