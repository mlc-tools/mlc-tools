CPP_XML = '''
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
$(FIELD).serialize_$(FORMAT)(xml.append_child("$(FIELD)"));
#deserialize:
$(FIELD).deserialize_$(FORMAT)(xml.child("$(FIELD)"));


#pointer
#serialize
if($(FIELD))
{
    auto child = xml.append_child("$(FIELD)");
    child.append_attribute("type").set_value($(FIELD)->get_type().c_str());
    $(FIELD)->serialize_$(FORMAT)(child);
}
#deserialize:
auto xml_$(FIELD) = xml.child("$(FIELD)");
if(xml_$(FIELD))
{
    std::string type = xml_$(FIELD).attribute("type").as_string();
    $(FIELD) = Factory::shared().build<$(TYPE)>(type);
    if($(FIELD))
    {
        $(FIELD)->deserialize_$(FORMAT)(xml_$(FIELD));
    }
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
    t.serialize_$(FORMAT)(arr_$(FIELD).append_child("item"));
}
#deserialize:
auto arr_$(FIELD) = xml.child("$(FIELD)");
for(auto child : arr_$(FIELD))
{
    $(FIELD).emplace_back();
    $(FIELD).back().deserialize_$(FORMAT)(child);
}


#list<pointer>
#serialize:
auto arr_$(FIELD) = xml.append_child("$(FIELD)");
for(auto& t : $(FIELD))
{
    t->serialize_$(FORMAT)(arr_$(FIELD).append_child(t->get_type().c_str()));
}
#deserialize:
auto arr_$(FIELD) = xml.child("$(FIELD)");
for(auto child : arr_$(FIELD))
{
    auto type = child.name();
    auto obj = Factory::shared().build<$(ARG_0)>(type);
    if(obj)
    {
        $(FIELD).push_back(obj);
        $(FIELD).back()->deserialize_$(FORMAT)(child);
    }
}


#link
#serialize:
if($(FIELD))
{ 
    xml.append_attribute("$(FIELD)").set_value($(FIELD)->name.c_str());
}
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


CPP_JSON = '''

#int, bool, float, string
#serialize:
#with default value:
if($(FIELD) != $(DEFAULT_VALUE))
{
    $(NAMESPACE)::set(json,"$(FIELD)",$(FIELD));
}
#without default value:
$(NAMESPACE)::set(json,"$(FIELD)",$(FIELD));

#deserialize:
#with default value:
if(json.isMember("$(FIELD)"))
{
    $(FIELD) = $(NAMESPACE)::get<$(TYPE)>(json["$(FIELD)"]);
}
else
{
    $(FIELD) = $(DEFAULT_VALUE);
}
#without default value:
$(FIELD) = $(NAMESPACE)::get<$(TYPE)>(json["$(FIELD)"]);


#serialized
#serialize:
$(FIELD).serialize_$(FORMAT)(json["$(FIELD)"]);
#deserialize:
$(FIELD).deserialize_$(FORMAT)(json["$(FIELD)"]);


#pointer
#serialize
if($(FIELD))
{
    $(FIELD)->serialize_$(FORMAT)(json["$(FIELD)"][$(FIELD)->get_type()]);
}
#deserialize:
if(json.isMember("$(FIELD)"))
{
    auto type_$(FIELD) = json["$(FIELD)"].getMemberNames()[0];
    $(FIELD) = Factory::shared().build<$(TYPE)>(type_$(FIELD));
    if($(FIELD))
    {
        $(FIELD)->deserialize_$(FORMAT)(json["$(FIELD)"][type_$(FIELD)]);
    }
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
    $(FIELD).push_back($(NAMESPACE)::get<$(ARG_0)>(arr_$(FIELD)[i]));
}

#list<int>, list<float>, list<string>
#serialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
int i_$(FIELD)=0;
for(const auto& t : $(FIELD))
{
    $(NAMESPACE)::set(arr_$(FIELD)[i_$(FIELD)++], t);
}
#deserialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
for(int i = 0; i < arr_$(FIELD).size(); ++i)
{
    $(FIELD).emplace_back();
    $(FIELD).back() = $(NAMESPACE)::get<$(ARG_0)>(arr_$(FIELD)[i]);
}


#list<serialized>
#serialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
int i_$(FIELD)=0;
for(auto& t : $(FIELD))
{
    t.serialize_$(FORMAT)(arr_$(FIELD)[i_$(FIELD)++]);
}
#deserialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
for(int i = 0; i < arr_$(FIELD).size(); ++i)
{
    $(FIELD).emplace_back();
    $(FIELD).back().deserialize_$(FORMAT)(arr_$(FIELD)[i]);
}


#list<pointer>
#serialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
for(auto& t : $(FIELD))
{
    auto index = arr_$(FIELD).size();
    t->serialize_$(FORMAT)(arr_$(FIELD)[index][t->get_type()]);
}
#deserialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
auto size_$(FIELD) = arr_$(FIELD).size();
for(int i = 0; i < size_$(FIELD); ++i)
{
    auto type = arr_$(FIELD)[i].getMemberNames()[0];
    auto obj = Factory::shared().build<$(ARG_0)>(type);
    if(obj)
    {
        $(FIELD).emplace_back(obj);
        $(FIELD).back()->deserialize_$(FORMAT)(arr_$(FIELD)[i][type]);
    }
}


#link
#serialize:
if($(FIELD))
{
    $(NAMESPACE)::set(json,"$(FIELD)",$(FIELD)->name);
}
#deserialize:
$(FIELD) = DataStorage::shared().get<$(TYPE)>($(NAMESPACE)::get<std::string>(json["$(FIELD)"]));


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
    auto name = $(NAMESPACE)::get<std::string>(item);
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
$(NAMESPACE)::set(json, "$(FIELD)", $(FIELD).str());
#deserialize:
$(FIELD) = $(NAMESPACE)::get<std::string>(json["$(FIELD)"]);

#list<enum>
#serialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
int i_$(FIELD)=0;
for(const auto& t : $(FIELD))
{
    $(NAMESPACE)::set(arr_$(FIELD)[i_$(FIELD)++], t.str());
}
#deserialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
for(int i = 0; i < arr_$(FIELD).size(); ++i)
{
    $(FIELD).emplace_back($(NAMESPACE)::get<std::string>(arr_$(FIELD)[i]));
}
'''
