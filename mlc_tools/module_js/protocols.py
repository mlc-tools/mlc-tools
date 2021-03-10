JS_JSON = '''
#int, bool, float, string
#serialize:
#with default value:
if($(OWNER)$(FIELD) != $(DEFAULT_VALUE))
{
    json["$(FIELD)"] = $(OWNER)$(FIELD);
}
#without default value:
json["$(FIELD)"] = $(OWNER)$(FIELD);
#deserialize
#with default value:
if("$(FIELD)" in json)
{
    $(OWNER)$(FIELD) = json["$(FIELD)"];
}
#without default value:
$(OWNER)$(FIELD) = json["$(FIELD)"];


#serialized
#serialize
if($(OWNER)$(FIELD))
{
    let dict = {};
    $(OWNER)$(FIELD).serialize_$(FORMAT)(dict);
    json["$(FIELD)"] = dict;
}
#deserialize
if('$(FIELD)' in json)
{
    $(OWNER)$(FIELD) = new $(TYPE)();
    $(OWNER)$(FIELD).deserialize_$(FORMAT)(json['$(FIELD)']);
}


#pointer
#serialize
if($(OWNER)$(FIELD))
{
    json['$(FIELD)'] = $({});
    json['$(FIELD)'].type = $(OWNER)$(FIELD).get_type();
    $(OWNER)$(FIELD).serialize_$(FORMAT)(json['$(FIELD)']);
}
#deserialize
if('$(FIELD)' in json)
{
    let type = json['$(FIELD)'].type;
    $(OWNER)$(FIELD) = Factory.build(type);
    $(OWNER)$(FIELD).deserialize_$(FORMAT)(json['$(FIELD)']);
}


#list<int>, list<float>, list<bool>, list<string>
#serialize
let arr_$(FIELD) = [];
for(let obj of $(OWNER)$(FIELD))
{
    arr_$(FIELD).push(obj);
}
json['$(FIELD)'] = arr_$(FIELD);
#deserialize
$(OWNER)$(FIELD) = [];
let arr_$(FIELD) = json['$(FIELD)']
for(let obj of arr_$(FIELD))
{
    $(OWNER)$(FIELD).push(obj)
}

#list<serialized>
#serialize
let arr_$(FIELD) = [];
for(let obj in $(OWNER)$(FIELD))
{
    let dict = {};
    obj.serialize_$(FORMAT)(dict);
    arr_$(FIELD).push(dict);
}
json['$(FIELD)'] = arr_$(FIELD);
#deserialize
$(OWNER)$(FIELD) = [];
let arr_$(FIELD) = json['$(FIELD)'];
for(let dict of arr_$(FIELD))
{
    let obj = new $(TYPE)();
    obj.deserialize_$(FORMAT)(dict);
    $(OWNER)$(FIELD).push(obj);
}


#list<pointer>
#serialize
json['$(FIELD)'] = [];
let arr_$(FIELD) = json['$(FIELD)'];
for(let t in $(OWNER)$(FIELD))
{
    arr_$(FIELD).push($({}));
    arr_$(FIELD)[-1][t.get_type()] = {};
    t.serialize_$(FORMAT)(arr_$(FIELD)[-1][t.get_type()]);
}
#deserialize
$(OWNER)$(FIELD) = [];
let arr_$(FIELD) = json['$(FIELD)'];
let size_$(FIELD) = arr_$(FIELD).length;
for(let index in size_$(FIELD))
{
    for(let key in arr_$(FIELD)[index])
    {
        let value = arr_$(FIELD)[index][key];
        let obj = Factory.build(key);
        $(OWNER)$(FIELD).push(obj);
        $(OWNER)$(FIELD)[-1].deserialize_$(FORMAT)(arr_$(FIELD)[index][key]);
        break;
    }
}


#link
#serialize:
if($(OWNER)$(FIELD))
{
    json['$(FIELD)'] = $(OWNER)$(FIELD).name;
}
#deserialize:
let name_$(FIELD) = json["$(FIELD)"];
if(name_$(FIELD))
{
    $(OWNER)$(FIELD) = DataStorage.shared().get$(TYPE)(name_$(FIELD));
}


#list<link>
#serialize:
json['$(FIELD)'] = [];
let arr_$(FIELD) = json['$(FIELD)'];
for(let t in $(OWNER)$(FIELD))
{
    arr_$(FIELD).push(t.name);
}
#deserialize:
$(OWNER)$(FIELD) = [];
let arr_$(FIELD) = json['$(FIELD)'];
for(let name in arr_$(FIELD))
{
    let data = DataStorage.shared().get$(ARG_0)(name);
    $(OWNER)$(FIELD).push(data);
}


#map
#serialize
let json_cache_$(FIELD) = json;
let arr_$(FIELD) = [];
json['$(FIELD)'] = arr_$(FIELD);
for(let key in $(OWNER)$(FIELD))
{
    let value = $(OWNER)$(FIELD)[key];
    arr_$(FIELD).push($({}));
    let json = arr_$(FIELD)[-1];
    $(KEY_SERIALIZE)
    $(VALUE_SERIALIZE)
}
json = json_cache_$(FIELD);
#deserialize
let json_cache_$(FIELD) = json;
let arr_$(FIELD) = json['$(FIELD)'];
for(let dict_key in arr_$(FIELD))
{
    let dict = arr_$(FIELD)[dict_key];
    let key = dict['key'];
    let type = key;
    let json = dict;
    let value = undefined;
    $(VALUE_SERIALIZE)
    $(OWNER)$(FIELD)[type] = value;
}
json = json_cache_$(FIELD);



#enum
#serialize:
json["$(FIELD)"] = $(OWNER)$(FIELD);
#deserialize
$(OWNER)$(FIELD) = json["$(FIELD)"];
'''
