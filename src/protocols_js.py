js_xml = '''
'''

js_json = '''

#int,bool,float,string
#serialize:
#with default value:
if($(OWNER)$(FIELD) != $(DEFAULT_VALUE))
{
    json["$(FIELD)"] = $(OWNER)$(FIELD);
}
#without default value:
json["$(FIELD)"] = $(OWNER)$(FIELD);
#deserialize:
#with default value:
if("$(FIELD)" in json)
{
    $(OWNER)$(FIELD) = json.$(FIELD);
}
#without default value:
$(OWNER)$(FIELD) = json["$(FIELD)"];


#serialized
#serialize:
json["$(FIELD)"] = {};
$(OWNER)$(FIELD).serialize(json["$(FIELD)"]);
#deserialize:
$(OWNER)$(FIELD) = factory_create($(TYPE));
$(OWNER)$(FIELD).deserialize(json["$(FIELD)"]);

#pointer
#serialize
if($(OWNER)$(FIELD))
{
    var type = $(OWNER)$(FIELD).get_type();
    json["$(FIELD)"] = {};
    json["$(FIELD)"][type] = {};
    $(OWNER)$(FIELD).serialize(json["$(FIELD)"][type]);
}
#deserialize:
if("$(FIELD)" in json)
{
    var type = Object.keys(json)[0];
    $(OWNER)$(FIELD) = factory_create($type);
    $(OWNER)$(FIELD).deserialize(json["$(FIELD)"][type]);
}


#list<int>, list<bool>, list<float>, list<string>
#serialize:
json["$(FIELD)"] = [];
for(var item in $(OWNER)$(FIELD))
{
    json["$(FIELD)"].push(item);
}
#deserialize:
if("$(FIELD)" in json)
{
    for(var item in json["$(FIELD)"])
    {
        $(OWNER)$(FIELD).push(item);
    }
}


#list<serialized>
#serialize:
json["$(FIELD)"] = [];
for(var item in $(OWNER)$(FIELD))
{
    var dict = {};
    item.serialize(dict);
    json["$(FIELD)"].push(dict);
}
#deserialize:
for(var item in json["$(FIELD)"])
{
    var obj = factory_create($(TYPE));
    obj.deserialize(item);
    $(OWNER)$(FIELD).push($obj);
}

#list<pointer>
#serialize:
json["$(FIELD)"] = [];
for(var t in $(OWNER)$(FIELD))
{
    var obj = {};
    obj[type] = {};
    t.serialize(obj[type]);
    json["$(FIELD)"].push(obj);
}
#deserialize:
var arr_$(FIELD) = json["$(FIELD)"];
for(var item in arr_$(FIELD))
{
    var type = Object.keys(item)[0];
    var obj = factory_create(type);
    obj.deserialize(item[type]);
    $(OWNER)$(FIELD).push(obj);
}


#link
#serialize:
json["$(FIELD)"] = $(OWNER)$(FIELD).name;
#deserialize:
var name = json["$(FIELD)"];
$(OWNER)$(FIELD) = DataStorage.shared().get$(TYPE)(name);

#list<link>
#serialize:
json[$(FIELD)] = [];
for(var data in $(OWNER)$(FIELD))
{
    $json[$(FIELD)].push(data.name);
}
#deserialize:
for(var name in json["$(FIELD)"])
{
    var data = DataStorage.shared().get$(ARG_0)(name);
    $(OWNER)$(FIELD).push(data);
}

#map
#serialize:
var map_$(FIELD) = [];
var json_main = json;
for(var key in $(OWNER)$(FIELD))
{
    var value = $(OWNER)$(FIELD)[key];
    var arr = {};
    json = arr;
    $(KEY_SERIALIZE)
    $(VALUE_SERIALIZE)

    map_$(FIELD).push(arr);
}
json = json_main;
json["$(FIELD)"] = map_$(FIELD);
#deserialize:
var json_cache = json;
if("$(FIELD)" in json)
{
    var arr = json["$(FIELD)"];
    for(json in arr)
    {
        $(VALUE)
        $(KEY_SERIALIZE)
        var map_key = key;
        $(VALUE_SERIALIZE)
        $(OWNER)$(FIELD)[map_key] = value;
    }
}
json = json_cache;



#enum
#serialize:
json["$(FIELD)"] = $(OWNER)$(FIELD);
#deserialize:
$(OWNER)$(FIELD) = (json["$(FIELD)"]);

'''
