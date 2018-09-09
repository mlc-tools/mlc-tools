from .protocols_php import php_xml
from .protocols_php import php_json

cpp_xml = '''
#int
#serialize:
#with default value:
if($(FIELD) != $(DEFAULT_VALUE))
{
    xml.append_attribute("$(FIELD)").set_value($(FIELD));
}
#without default value:
xml.append_attribute("$(FIELD)").set_value($(FIELD));

#deserialize:
#with default value:
$(FIELD) = xml.attribute("$(FIELD)").as_int($(DEFAULT_VALUE));
#without default value:
$(FIELD) = xml.attribute("$(FIELD)").as_int();


#bool
#serialize:
#with default value:
if($(FIELD) != $(DEFAULT_VALUE))
{
    xml.append_attribute("$(FIELD)").set_value($(FIELD));
}
#without default value:
xml.append_attribute("$(FIELD)").set_value($(FIELD));

#deserialize:
#with default value:
$(FIELD) = xml.attribute("$(FIELD)").as_bool($(DEFAULT_VALUE));
#without default value:
$(FIELD) = xml.attribute("$(FIELD)").as_bool();


#float
#serialize:
#with default value:
if($(FIELD) != $(DEFAULT_VALUE))
{
    xml.append_attribute("$(FIELD)").set_value($(FIELD));
}
#without default value:
xml.append_attribute("$(FIELD)").set_value($(FIELD));

#deserialize:
#with default value:
$(FIELD) = xml.attribute("$(FIELD)").as_float($(DEFAULT_VALUE));
#without default value:
$(FIELD) = xml.attribute("$(FIELD)").as_float();


#string
#serialize:
#with default value:
if($(FIELD) != $(DEFAULT_VALUE))
{
    xml.append_attribute("$(FIELD)").set_value($(FIELD).c_str());
}
#without default value:
xml.append_attribute("$(FIELD)").set_value($(FIELD).c_str());

#deserialize:
#with default value:
$(FIELD) = xml.attribute("$(FIELD)").as_string($(DEFAULT_VALUE));
#without default value:
$(FIELD) = xml.attribute("$(FIELD)").as_string();


#serialized
#serialize:
$(FIELD).serialize(xml.append_child("$(FIELD)"));
#deserialize:
$(FIELD).deserialize(xml.child("$(FIELD)"));


#pointer
#serialize
if($(FIELD))
{
    auto child = xml.append_child("$(FIELD)");
    child.append_attribute("type").set_value($(FIELD)->get_type().c_str());
    $(FIELD)->serialize(child);
}
#deserialize:
auto xml_$(FIELD) = xml.child("$(FIELD)");
if(xml_$(FIELD))
{
    std::string type = xml_$(FIELD).attribute("type").as_string();
    $(FIELD) = Factory::shared().build<$(TYPE)>(type);
    $(FIELD)->deserialize(xml_$(FIELD));
}


#list<int>
#serialize:
auto arr_$(FIELD) = xml.append_child("$(FIELD)");
for(auto t : $(FIELD))
{
    arr_$(FIELD).append_child("item").append_attribute("value").set_value(t);
}
#deserialize:
auto arr_$(FIELD) = xml.child("$(FIELD)");
for(const auto& child : arr_$(FIELD))
{
    $(FIELD).push_back(child.attribute("value").as_int());
}

#list<bool>
#serialize:
auto arr_$(FIELD) = xml.append_child("$(FIELD)");
for(auto t : $(FIELD))
{
    arr_$(FIELD).append_child("item").append_attribute("value").set_value(t);
}
#deserialize:
auto arr_$(FIELD) = xml.child("$(FIELD)");
for(const auto& child : arr_$(FIELD))
{
    $(FIELD).push_back(child.attribute("value").as_bool());
}
#list<float>
#serialize:
auto arr_$(FIELD) = xml.append_child("$(FIELD)");
for(auto t : $(FIELD))
{
    arr_$(FIELD).append_child("item").append_attribute("value").set_value(t);
}
#deserialize:
auto arr_$(FIELD) = xml.child("$(FIELD)");
for(const auto& child : arr_$(FIELD))
{
    $(FIELD).push_back(child.attribute("value").as_float());
}
#list<string>
#serialize:
auto arr_$(FIELD) = xml.append_child("$(FIELD)");
for(const auto& t : $(FIELD))
{
    arr_$(FIELD).append_child("item").append_attribute("value").set_value(t.c_str());
}
#deserialize:
auto arr_$(FIELD) = xml.child("$(FIELD)");
for(const auto& child : arr_$(FIELD))
{
    $(FIELD).push_back(child.attribute("value").as_string(""));
}

#list<serialized>
#serialize:
auto arr_$(FIELD) = xml.append_child("$(FIELD)");
for(auto& t : $(FIELD))
{
    t.serialize(arr_$(FIELD).append_child("item"));
}
#deserialize:
auto arr_$(FIELD) = xml.child("$(FIELD)");
for(auto child : arr_$(FIELD))
{
    $(FIELD).emplace_back();
    $(FIELD).back().deserialize(child);
}


#list<pointer>
#serialize:
auto arr_$(FIELD) = xml.append_child("$(FIELD)");
for(auto& t : $(FIELD))
{
    t->serialize(arr_$(FIELD).append_child(t->get_type().c_str()));
}
#deserialize:
auto arr_$(FIELD) = xml.child("$(FIELD)");
for(auto child : arr_$(FIELD))
{
    auto type = child.name();
    $(FIELD).push_back(Factory::shared().build<$(ARG_0)>(type));
    $(FIELD).back()->deserialize(child);
}


#link
#serialize:
xml.append_attribute("$(FIELD)").set_value($(FIELD)->name.c_str());
#deserialize:
auto name_$(FIELD) = xml.attribute("$(FIELD)").as_string();
$(FIELD) = DataStorage::shared().get<$(TYPE)>(name_$(FIELD));


#list<link>
#serialize:
auto arr_$(FIELD) = xml.append_child("$(FIELD)");
for(auto& t : $(FIELD))
{
    arr_$(FIELD).append_child("data").append_attribute("value").set_value(t->name.c_str());
}
#deserialize:
auto arr_$(FIELD) = xml.child("$(FIELD)");
for(auto& child : arr_$(FIELD))
{
    auto name = child.attribute("value").as_string("");
    $(FIELD).push_back(DataStorage::shared().get<$(ARG_0)>(name));
}

#map
#serialize:
auto map_$(FIELD) = xml.append_child("$(FIELD)");
for(auto& pair : $(FIELD))
{
    auto xml = map_$(FIELD).append_child("pair");
    auto& key = pair.first;
    auto& value = pair.second;
    $(KEY_SERIALIZE)
    $(VALUE_SERIALIZE)
}
#deserialize:
auto map_$(FIELD) = xml.child("$(FIELD)");
for(auto child : map_$(FIELD))
{
    auto xml = child;
    $(KEY)
    $(VALUE_TYPE) value;
    $(KEY_SERIALIZE)
    $(VALUE_SERIALIZE)
    $(FIELD)[key] = value;
}

#enum
#serialize:
xml.append_attribute("$(FIELD)").set_value($(FIELD).str().c_str());
#deserialize:
$(FIELD) = std::string(xml.attribute("$(FIELD)").as_string(""));

#list<enum>
#serialize:
auto arr_$(FIELD) = xml.append_child("$(FIELD)");
for(auto t : $(FIELD))
{

    arr_$(FIELD).append_child("item").append_attribute("value").set_value(t.str().c_str());
}
#deserialize:
auto arr_$(FIELD) = xml.child("$(FIELD)");
for(const auto& child : arr_$(FIELD))
{
    $(FIELD).emplace_back(child.attribute("value").as_string());
}
'''


cpp_json = '''

#int, bool, float, string
#serialize:
#with default value:
if($(FIELD) != $(DEFAULT_VALUE))
{
    @{namespace}::set(json,"$(FIELD)",$(FIELD));
}
#without default value:
@{namespace}::set(json,"$(FIELD)",$(FIELD));

#deserialize:
#with default value:
if(json.isMember("$(FIELD)"))
{
    $(FIELD) = @{namespace}::get<$(TYPE)>(json["$(FIELD)"]);
}
else
{
    $(FIELD) = $(DEFAULT_VALUE);
}
#without default value:
$(FIELD) = @{namespace}::get<$(TYPE)>(json["$(FIELD)"]);


#serialized
#serialize:
$(FIELD).serialize(json["$(FIELD)"]);
#deserialize:
$(FIELD).deserialize(json["$(FIELD)"]);


#pointer
#serialize
if($(FIELD))
{
    $(FIELD)->serialize(json["$(FIELD)"][$(FIELD)->get_type()]);
}
#deserialize:
if(json.isMember("$(FIELD)"))
{
    auto type_$(FIELD) = json["$(FIELD)"].getMemberNames()[0];
    $(FIELD) = Factory::shared().build<$(TYPE)>(type_$(FIELD));
    $(FIELD)->deserialize(json["$(FIELD)"][type_$(FIELD)]);
}


#list<bool>
#serialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
int i_$(FIELD)=0;
for(const auto& t : $(FIELD))
{
    arr_$(FIELD)[i_$(FIELD)++] = Json::Value(t);
}
#deserialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
for(int i = 0; i < arr_$(FIELD).size(); ++i)
{
    $(FIELD).emplace_back();
    $(FIELD).back() = @{namespace}::get<$(ARG_0)>(arr_$(FIELD)[i]);
}

#list<int>, list<float>, list<string>
#serialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
int i_$(FIELD)=0;
for(const auto& t : $(FIELD))
{
    @{namespace}::set(arr_$(FIELD)[i_$(FIELD)++], t);
}
#deserialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
for(int i = 0; i < arr_$(FIELD).size(); ++i)
{
    $(FIELD).emplace_back();
    $(FIELD).back() = @{namespace}::get<$(ARG_0)>(arr_$(FIELD)[i]);
}


#list<serialized>
#serialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
int i_$(FIELD)=0;
for(auto& t : $(FIELD))
{
    t.serialize(arr_$(FIELD)[i_$(FIELD)++]);
}
#deserialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
for(int i = 0; i < arr_$(FIELD).size(); ++i)
{
    $(FIELD).emplace_back();
    $(FIELD).back().deserialize(arr_$(FIELD)[i]);
}


#list<pointer>
#serialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
for(auto& t : $(FIELD))
{
    auto index = arr_$(FIELD).size();
    t->serialize(arr_$(FIELD)[index][t->get_type()]);
}
#deserialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
auto size_$(FIELD) = arr_$(FIELD).size();
for(int i = 0; i < size_$(FIELD); ++i)
{
    auto type = arr_$(FIELD)[i].getMemberNames()[0];
    auto obj = Factory::shared().build<$(ARG_0)>(type);
    $(FIELD).emplace_back(obj);
    $(FIELD).back()->deserialize(arr_$(FIELD)[i][type]);
}


#link
#serialize:
@{namespace}::set(json,"$(FIELD)",$(FIELD)->name);
#deserialize:
$(FIELD) = DataStorage::shared().get<$(TYPE)>(@{namespace}::get<std::string>(json["$(FIELD)"]));


#list<link>
#serialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
for(auto& item : $(FIELD))
{
    arr_$(FIELD).append(item->name);
}
#deserialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
for(auto item : arr_$(FIELD))
{
    auto name = @{namespace}::get<std::string>(item);
    auto data = DataStorage::shared().get<$(ARG_0)>(name);
    $(FIELD).push_back(data);
}


#map
#serialize:
auto& map_$(FIELD) = json["$(FIELD)"];
for(auto& pair : $(FIELD))
{
    auto& json = map_$(FIELD)[map_$(FIELD).size()];
    auto& key = pair.first;
    auto& value = pair.second;
    $(KEY_SERIALIZE)
    $(VALUE_SERIALIZE)
}
#deserialize:
auto& map_$(FIELD) = json["$(FIELD)"];
auto size_$(FIELD)= map_$(FIELD).size();
for(unsigned int i = 0; i < size_$(FIELD); ++i)
{
    auto& json = map_$(FIELD)[i];
    $(KEY);
    $(VALUE_TYPE) value;
    $(VALUE_SERIALIZE)
    $(KEY_SERIALIZE)
    $(FIELD)[key] = value;
}


#enum
#serialize:
@{namespace}::set(json, "$(FIELD)", $(FIELD).str());
#deserialize:
$(FIELD) = @{namespace}::get<std::string>(json["$(FIELD)"]);

#list<enum>
#serialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
int i_$(FIELD)=0;
for(const auto& t : $(FIELD))
{
    @{namespace}::set(arr_$(FIELD)[i_$(FIELD)++], t.str());
}
#deserialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
for(int i = 0; i < arr_$(FIELD).size(); ++i)
{
    $(FIELD).emplace_back(@{namespace}::get<std::string>(arr_$(FIELD)[i]));
}
'''

py_xml = '''
# $(0) = obj_name
# $(1) = obj_type
# $(2) = obj_value
# ??? {3} = '{}'
# $(4) = owner
# $(5) = obj_template_args[0].type if len(obj_template_args) > 0 else 'unknown_arg'

#int
#serialize:
#with default value:
if $(OWNER)$(FIELD) != $(DEFAULT_VALUE):
            xml.set("$(FIELD)", str($(OWNER)$(FIELD)))
#without default value:
xml.set("$(FIELD)", str($(OWNER)$(FIELD)))
#deserialize:
#with default value:
$(OWNER)$(FIELD) = int(float(xml.get("$(FIELD)", default=$(DEFAULT_VALUE))))
#without default value:
$(OWNER)$(FIELD) = int(float(xml.get("$(FIELD)")))

#bool
#serialize:
#with default value:
if $(OWNER)$(FIELD) != $(DEFAULT_VALUE):
            xml.set("$(FIELD)", "yes" if $(OWNER)$(FIELD) else "no")
#without default value:
xml.set("$(FIELD)", str($(OWNER)$(FIELD)))
#deserialize:
#with default value:
value = xml.get("$(FIELD)", default="$(DEFAULT_VALUE)")
        value = value.lower()[0] in ['t', 'y'] if value else False
        $(OWNER)$(FIELD) = value
#without default value:
value = xml.get("$(FIELD)")
        value = value.lower()[0] in ['t', 'y'] if value else False
        $(OWNER)$(FIELD) = value

#float
#serialize:
#with default value:
if $(OWNER)$(FIELD) != $(DEFAULT_VALUE):
            xml.set("$(FIELD)", str($(OWNER)$(FIELD)))
#without default value:
xml.set("$(FIELD)", str($(OWNER)$(FIELD)))
#deserialize:
#with default value:
$(OWNER)$(FIELD) = float(xml.get("$(FIELD)", default=$(DEFAULT_VALUE)))
#without default value:
$(OWNER)$(FIELD) = float(xml.get("$(FIELD)"))

#string
#serialize:
#with default value:
if $(OWNER)$(FIELD) != $(DEFAULT_VALUE):
            xml.set("$(FIELD)", str($(OWNER)$(FIELD)))
#without default value:
xml.set("$(FIELD)", str($(OWNER)$(FIELD)))
#deserialize:
#with default value:
$(OWNER)$(FIELD) = str(xml.get("$(FIELD)", default=$(DEFAULT_VALUE)))
#without default value:
$(OWNER)$(FIELD) = str(xml.get("$(FIELD)"))





#pointer
#serialize:
if $(OWNER)$(FIELD):
            xml_pointer = ET.SubElement(xml, '$(FIELD)')
            xml_pointer.set('type', $(OWNER)$(FIELD).get_type())
            $(OWNER)$(FIELD).serialize(xml_pointer)
#deserialize:
xml_pointer = xml.find('$(FIELD)')
        if xml_pointer is not None:
            type = xml_pointer.get('type')
            $(OWNER)$(FIELD) = Factory.build(type)
            $(OWNER)$(FIELD).deserialize(xml_pointer)


#list<int>
#serialize:
arr = ET.SubElement(xml, '$(FIELD)')
        for obj in $(OWNER)$(FIELD):
            ET.SubElement(arr, 'item').set('value', str(obj))
#deserialize:
$(OWNER)$(FIELD) = list()
        arr = xml.find('$(FIELD)')
        if arr is not None:
            for obj in arr:
                $(OWNER)$(FIELD).append(int(float(obj.get('value'))))

#list<bool>
#serialize:
arr = ET.SubElement(xml, '$(FIELD)')
        for obj in $(OWNER)$(FIELD):
            ET.SubElement(arr, 'item').set('value', str(obj))
#deserialize:
$(OWNER)$(FIELD) = list()
        arr = xml.find('$(FIELD)')
        if arr is not None:
            for obj in arr:
                value = obj.get('value')
                value = value.lower()[0] in ['t', 'y'] if value else False
                $(OWNER)$(FIELD).append(value)

#list<float>
#serialize:
arr = ET.SubElement(xml, '$(FIELD)')
        for obj in $(OWNER)$(FIELD):
            ET.SubElement(arr, 'item').set('value', str(obj))
#deserialize:
$(OWNER)$(FIELD) = list()
        arr = xml.find('$(FIELD)')
        if arr is not None:
            for obj in arr:
                $(OWNER)$(FIELD).append(float(obj.get('value')))

#list<string>
#serialize:
arr = ET.SubElement(xml, '$(FIELD)')
        for obj in $(OWNER)$(FIELD):
            ET.SubElement(arr, 'item').set('value', str(obj))
#deserialize:
$(OWNER)$(FIELD) = list()
        arr = xml.find('$(FIELD)')
        if arr is not None:
            for obj in arr:
                $(OWNER)$(FIELD).append(str(obj.get('value')))


#list<serialized>
#serialize:
arr = ET.SubElement(xml, '$(FIELD)')
        for obj in $(OWNER)$(FIELD):
            item = ET.SubElement(arr, 'item')
            obj.serialize(item)
#deserialize:
$(OWNER)$(FIELD) = list()
        arr = xml.find('$(FIELD)')
        if arr is not None:
            from .$(TYPE) import $(TYPE)
            for xml_child in arr:
                obj = $(TYPE)()
                obj.deserialize(xml_child)
                $(OWNER)$(FIELD).append(obj)


#serialized
#serialize:
if $(OWNER)$(FIELD):
            xml_child = ET.SubElement(xml, '$(FIELD)')
            $(OWNER)$(FIELD).serialize(xml_child)
#deserialize:
xml_child = xml.find('$(FIELD)')
        from .$(TYPE) import $(TYPE)
        if xml_child is not None:
            $(OWNER)$(FIELD) = $(TYPE)()
            $(OWNER)$(FIELD).deserialize(xml_child)


#list<pointer>
#serialize:
arr = ET.SubElement(xml, '$(FIELD)')
        for t in $(OWNER)$(FIELD):
            item = ET.SubElement(arr, t.get_type())
            t.serialize(item)
#deserialize:
$(OWNER)$(FIELD) = list()
        arr = xml.find('$(FIELD)')
        if arr is not None:
            for xml_item in arr:
                type = xml_item.tag
                obj = Factory.build(type)
                obj.deserialize(xml_item)
                $(OWNER)$(FIELD).append(obj)

#link
#serialize:
from .$(TYPE) import $(TYPE)
        if isinstance($(OWNER)$(FIELD), $(TYPE)):
            xml.set("$(FIELD)", $(OWNER)$(FIELD).name)
        else:
            xml.set("$(FIELD)", $(OWNER)$(FIELD))
#deserialize:
name_$(FIELD) = xml.get("$(FIELD)")
        from .$(TYPE) import $(TYPE)
        $(OWNER)$(FIELD) = DataStorage.shared().get$(TYPE)(name_$(FIELD))

#list<link>
#serialize:
arr_$(FIELD) = ET.SubElement(xml, '$(FIELD)')
        for t in $(OWNER)$(FIELD):
            item = ET.SubElement(arr_$(FIELD), 'item')
            item.set("value", t.name)
#deserialize:
$(OWNER)$(FIELD) = list()
        arr = xml.find('$(FIELD)')
        if arr is not None:
            for xml_item in arr:
                name = xml_item.get('value')
                data = DataStorage.shared().get$(ARG_0)(name)
                $(OWNER)$(FIELD).append(data)

#map
#serialize
        xml_cache = xml
        map = ET.SubElement(xml, '$(FIELD)')
        for key, value in $(OWNER)$(FIELD).iteritems():
            xml = ET.SubElement(map, 'pair')
$(KEY_SERIALIZE)
$(VALUE_SERIALIZE)
        xml = xml_cache
#deserialize
        xml_cache = xml
        map = xml.find('$(FIELD)')
        for xml_child in (map if map is not None else []):
            xml = xml_child
$(KEY_SERIALIZE)
            map_key = key
$(VALUE_SERIALIZE)
            $(OWNER)$(FIELD)[map_key] = value
        xml = xml_cache

#enum
#serialize:
xml.set("$(FIELD)", str($(OWNER)$(FIELD)))
#deserialize:
$(OWNER)$(FIELD) = xml.get("$(FIELD)")
'''

py_json = '''
#int, bool, float, string
#serialize:
#with default value:
if $(OWNER)$(FIELD) != $(DEFAULT_VALUE):
            dictionary["$(FIELD)"] = $(OWNER)$(FIELD)
#without default value:
dictionary["$(FIELD)"] = $(OWNER)$(FIELD)
#deserialize
#with default value:
if "$(FIELD)" in dictionary:
            $(OWNER)$(FIELD) = dictionary["$(FIELD)"]
#without default value:
$(OWNER)$(FIELD) = dictionary["$(FIELD)"]


#pointer
#serialize
if $(OWNER)$(FIELD):
            dictionary['$(FIELD)'] = $({})
            dictionary['$(FIELD)'][$(OWNER)$(FIELD).get_type()] = $({})
            $(OWNER)$(FIELD).serialize(dictionary['$(FIELD)'][$(OWNER)$(FIELD).get_type()])
#deserialize
if '$(FIELD)' in dictionary:
            for key, value_ in dictionary['$(FIELD)'].iteritems():
                $(OWNER)$(FIELD) = Factory.build(key)
                $(OWNER)$(FIELD).deserialize(value_)
                break

#list<int>, list<float>, list<bool>, list<string>
#serialize
arr_$(FIELD) = []
        for obj in $(OWNER)$(FIELD):
            arr_$(FIELD).append(obj)
        dictionary['$(FIELD)'] = arr_$(FIELD)
#deserialize
$(OWNER)$(FIELD) = list()
        arr_$(FIELD) = dictionary['$(FIELD)']
        for obj in arr_$(FIELD):
            $(OWNER)$(FIELD).append(obj)

#list<serialized>
#serialize
arr_$(FIELD) = []
        for obj in $(OWNER)$(FIELD):
            dict = $({})
            obj.serialize(dict)
            arr_$(FIELD).append(dict)
        dictionary['$(FIELD)'] = arr_$(FIELD)
#deserialize
$(OWNER)$(FIELD) = list()
        from .$(TYPE) import $(TYPE)
        arr_$(FIELD) = dictionary['$(FIELD)']
        for dict in arr_$(FIELD):
            obj = $(TYPE)()
            obj.deserialize(dict)
            $(OWNER)$(FIELD).append(obj)

#serialized
#serialize
if $(OWNER)$(FIELD):
            dict = $({})
            $(OWNER)$(FIELD).serialize(dict)
            dictionary["$(FIELD)"] = dict
#deserialize
if '$(FIELD)' in dictionary:
            from .$(TYPE) import $(TYPE)
            $(OWNER)$(FIELD) = $(TYPE)()
            $(OWNER)$(FIELD).deserialize(dictionary['$(FIELD)'])

#list<pointer>
#serialize
dictionary['$(FIELD)'] = []
        arr = dictionary['$(FIELD)']
        for t in $(OWNER)$(FIELD):
            arr.append($({}))
            arr[-1][t.get_type()] = $({})
            t.serialize(arr[-1][t.get_type()])
#deserialize
$(OWNER)$(FIELD) = list()
        arr = dictionary['$(FIELD)']
        size = len(arr)
        for index in range(size):
            for key, value in arr[index].iteritems():
                obj = Factory.build(key)
                $(OWNER)$(FIELD).append(obj)
                $(OWNER)$(FIELD)[-1].deserialize(arr[index][key])
                break


#link
#serialize:
from .$(TYPE) import $(TYPE)
        if isinstance($(OWNER)$(FIELD), $(TYPE)):
            from .$(TYPE) import $(TYPE)
            dictionary['$(FIELD)'] = $(OWNER)$(FIELD).name
        else:
            dictionary['$(FIELD)'] = $(OWNER)$(FIELD)
#deserialize:
name = dictionary["$(FIELD)"]
        $(OWNER)$(FIELD) = DataStorage.shared().get$(TYPE)(name)


#list<link>
#serialize:
dictionary['$(FIELD)'] = []
        arr = dictionary['$(FIELD)']
        for t in $(OWNER)$(FIELD):
            arr.append(t.name)
#deserialize:
$(OWNER)$(FIELD) = list()
        arr = dictionary['$(FIELD)']
        for name in arr:
            data = DataStorage.shared().get$(ARG_0)(name)
            $(OWNER)$(FIELD).append(data)


#map
#serialize
        dict_cach = dictionary
        arr = []
        dictionary['$(FIELD)'] = arr
        for key, value in $(OWNER)$(FIELD).iteritems():
            arr.append($({}))
            dictionary = arr[-1]
$(KEY_SERIALIZE)
$(VALUE_SERIALIZE)
        dictionary = dict_cach
#deserialize
        dict_cach = dictionary
        arr = dictionary['$(FIELD)']
        for dict in arr:
            key = dict['key']
            type = key
            dictionary = dict
$(VALUE_SERIALIZE)
            $(OWNER)$(FIELD)[type] = value
        dictionary = dict_cach


#enum
#serialize:
dictionary["$(FIELD)"] = $(OWNER)$(FIELD)
#deserialize
$(OWNER)$(FIELD) = dictionary["$(FIELD)"]
'''

protocols = {}
protocols['cpp'] = {'xml': cpp_xml, 'json': cpp_json}
protocols['py'] = {'xml': py_xml, 'json': py_json}
protocols['php'] = {'xml': php_xml, 'json': php_json}
