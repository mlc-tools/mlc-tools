from WriterCpp import WriterCpp
from WriterCpp import SERIALIZATION as S
from WriterCpp import DESERIALIZATION as D
from Object import Object
from Class import Class


class WriterCppSerializationXml(WriterCpp):
    def __init__(self, out_directory, parser):
        WriterCpp.__init__(self, out_directory, parser)

    def create_serialization_patterns(self):
        self.serialize_formats[S]['simple'] = []
        self.serialize_formats[S]['simple'].append('if({0} != {2}) \n__begin__\n::set(xml,"{0}",{0});\n__end__')
        self.serialize_formats[S]['simple'].append('::set(xml,"{0}",{0});')
        self.serialize_formats[D]['simple'] = []
        self.serialize_formats[D]['simple'].append('''auto attr_{0} = xml.attribute("{0}");
            if(attr_{0})
            {3}
                {0} = ::get<{1}>(attr_{0});
            {4}
            else
            {3}
                {0} = {2};
            {4}''')
        self.serialize_formats[D]['simple'].append('{0} = ::get<{1}>(xml, "{0}");')

        self.serialize_formats[S]['serialized'] = []
        self.serialize_formats[S]['serialized'].append('{0}.serialize(xml.append_child("{0}"));')
        self.serialize_formats[S]['serialized'].append('{0}.serialize(xml.append_child("{0}"));')
        self.serialize_formats[D]['serialized'] = []
        self.serialize_formats[D]['serialized'].append('{0}.deserialize(xml.child("{0}"));')
        self.serialize_formats[D]['serialized'].append('{0}.deserialize(xml.child("{0}"));')

        self.serialize_formats[S]['pointer'] = []
        self.serialize_formats[S]['pointer'].append('static_assert(0, "field "{0}" should have not initialize value");')
        self.serialize_formats[S]['pointer'].append('''
            if({0})
            {3}
                auto child = xml.append_child("{0}");
                child.append_attribute("type").set_value({0}->get_type().c_str());
                {0}->serialize(child);
            {4}''')
        self.serialize_formats[D]['pointer'] = []
        self.serialize_formats[D]['pointer'].append('static_assert(0, "field "{0}" should have not initialize value");')
        self.serialize_formats[D]['pointer'].append('''
            auto xml_{0} = xml.child("{0}");
            if(xml_{0})
            {3}
                std::string type = xml_{0}.attribute("type").as_string();
                {0} = Factory::shared().build<{1}>(type);
                {0}->deserialize(xml_{0});
            {4}''')

        self.serialize_formats[S]['list<simple>'] = []
        self.serialize_formats[S]['list<simple>'].append(
            'static_assert(0, "list "{0}" not should have a initialize value");'
        )
        self.serialize_formats[S]['list<simple>'].append('''auto arr_{0} = xml.append_child("{0}");
             for(auto& t : {0})
             {3}
                auto attr = arr_{0}.append_child("{5}").append_attribute("value");
                set(attr, t);
             {4}''')
        self.serialize_formats[D]['list<simple>'] = []
        self.serialize_formats[D]['list<simple>'].append(
            'static_assert(0, "list "{0}" not should have a initialize value");'
        )
        self.serialize_formats[D]['list<simple>'].append('''auto arr_{0} = xml.child("{0}");
            for(auto child : arr_{0})
            {3}
                {0}.emplace_back();
                {0}.back() = get<{5}>(child, "value");
            {4}''')

        self.serialize_formats[S]['serialized_list'] = []
        self.serialize_formats[S]['serialized_list'].append(
            'static_assert(0, "list "{0}" not should have a initialize value");'
        )
        self.serialize_formats[S]['serialized_list'].append('''auto arr_{0} = xml.append_child("{0}");
            for(auto& t : {0})
            {3}
                t.serialize(arr_{0}.append_child(t.get_type().c_str()));
            {4}''')
        self.serialize_formats[D]['serialized_list'] = []
        self.serialize_formats[D]['serialized_list'].append(
            'static_assert(0, "list "{0}" not should have a initialize value");'
        )
        self.serialize_formats[D]['serialized_list'].append('''auto arr_{0} = xml.child("{0}");
            for(auto child : arr_{0})
            {3}
                {0}.emplace_back();
                {0}.back().deserialize(child);
            {4}''')

        self.serialize_formats[S]['pointer_list'] = []
        self.serialize_formats[S]['pointer_list'].append(
            'static_assert(0, "list "{0}" not should have a initialize value");'
        )
        self.serialize_formats[S]['pointer_list'].append('''auto arr_{0} = xml.append_child("{0}");
            for(auto& t : {0})
            {3}
                t->serialize(arr_{0}.append_child(t->get_type().c_str()));
            {4}''')
        self.serialize_formats[D]['pointer_list'] = []
        self.serialize_formats[D]['pointer_list'].append(
            'static_assert(0, "list "{0}" not should have a initialize value");'
        )
        self.serialize_formats[D]['pointer_list'].append('''auto arr_{0} = xml.child("{0}");
            for(auto child : arr_{0})
            {3}
                auto type = child.name();
                auto obj = Factory::shared().build<{5}>(type);
                {0}.emplace_back(obj);
                {0}.back()->deserialize(child);
            {4}''')

        self.serialize_formats[S]['link'] = []
        self.serialize_formats[S]['link'].append('static_assert(0, "link "{0}" not should have a initialize value");')
        self.serialize_formats[S]['link'].append('''::set(xml,"{0}",{0}->name);''')
        self.serialize_formats[D]['link'] = []
        self.serialize_formats[D]['link'].append('static_assert(0, "link "{0}" not should have a initialize value");')
        self.serialize_formats[D]['link'].append('''auto name_{0} = ::get<std::string>(xml, "{0}");
            {0} = get_data_storage().get<{1}>(name_{0});''')

        self.serialize_formats[S]['list<link>'] = []
        self.serialize_formats[S]['list<link>'].append(
            'static_assert(0, "list "{0}" not should have a initialize value");'
        )
        self.serialize_formats[S]['list<link>'].append('''auto arr_{0} = xml.append_child("{0}");
             for(auto& t : {0})
             {3}
                auto attr = arr_{0}.append_child("{5}").append_attribute("value");
                set(attr, t->name);
             {4}''')
        self.serialize_formats[D]['list<link>'] = []
        self.serialize_formats[D]['list<link>'].append(
            'static_assert(0, "list "{0}" not should have a initialize value");'
        )
        self.serialize_formats[D]['list<link>'].append('''auto arr_{0} = xml.child("{0}");
            for(auto child : arr_{0})
            {3}
                name = ::get<std::string>(child, "value");
                {0}.push_back(get_data_storage().get<{5}>(name));
            {4}''')

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
            return ['xml', 'pugi::xml_node']
        if serialization_type == D:
            return ['xml', 'const pugi::xml_node&']
        return ['', '']

    def get_behavior_call_format(self):
        return '{0}::{1}(xml);'

    def build_map_serialization(self, obj_name, obj_type, obj_value, obj_is_pointer, obj_template_args):
        key = obj_template_args[0]
        value = obj_template_args[1]
        key_type = key.name if isinstance(key, Class) else key.type
        value_type = value.name if isinstance(value, Class) else value.type
        pattern = '''
        auto map_{0} = xml.append_child("{0}");
        for(auto pair : {0})
        __begin__
            auto xml = map_{0}.append_child("pair");
            auto& key = pair.first;
            auto& value = pair.second;
            {1}
            {2}
        __end__
        '''
        _value_is_pointer = value.is_pointer
        a0 = obj_name
        a1 = self._build_serialize_operation('key', key_type, None, key.is_pointer, [], S, key.is_link)
        a2 = self._build_serialize_operation('value', value_type, None, _value_is_pointer, [], S, value.is_link)
        return pattern.format(a0, a1, a2)

    def build_map_deserialization(self, obj_name, obj_type, obj_value, obj_is_pointer, obj_template_args):
        key = obj_template_args[0]
        value = obj_template_args[1]
        key_type = key.name if isinstance(key, Class) else key.type
        value_type = value.name if isinstance(value, Class) else value.type
        pattern = '''
        auto map_{0} = xml.child("{0}");
        for(auto child : map_{0})
        __begin__
            auto xml = child;
            {3}{1}
            {4} value;
            {2}
            {0}[key] = value;
        __end__
        '''
        if key.is_link:
            key_str = 'const {}* key(nullptr);'.format(key_type)
        elif key.is_pointer:
            key_str = 'auto key = make_intrusive<{}>();'.format(key_type)
        else:
            key_str = '{} key;'.format(key_type)

        _value_is_pointer = value.is_pointer if isinstance(value, Object) else False
        a0 = obj_name
        a1 = self._build_serialize_operation('key', key_type, None, key.is_pointer, [], D, key.is_link)
        a2 = self._build_serialize_operation('value', value_type, None, _value_is_pointer, [], D, value.is_link)
        a3 = key_str
        a4 = value_type
        if value.is_pointer:
            a4 = 'IntrusivePtr<{}>'.format(value_type)
        return pattern.format(a0, a1, a2, a3, a4)

    def _build_serialize_operation_enum(
            self,
            obj_name,
            obj_type,
            obj_value,
            obj_is_pointer,
            obj_template_args,
            serialization_type
    ):
        if serialization_type == S:
            return '::set(xml, "{0}", (std::string){0});'.format(obj_name)
        else:
            return '{0} = ::get<std::string>(xml, "{0}");'.format(obj_name)
