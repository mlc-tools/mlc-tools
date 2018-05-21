java_xml = '''
#string
#serialize:
#with default value:
if($(OWNER)$(FIELD) != $(DEFAULT_VALUE))
{
    ((Element)xml).setAttribute("$(FIELD)", $(OWNER)$(FIELD));
}
#without default value:
((Element)xml).setAttribute("$(FIELD)", $(OWNER)$(FIELD));
#deserialize:
#with default value:
var $(FIELD)_attr = xml.getAttributes().getNamedItem("$(FIELD)");
if ($(FIELD)_attr != null)
{
    $(OWNER)$(FIELD) = $(FIELD)_attr.getNodeValue();
}
#without default value:
$(OWNER)$(FIELD) = $(FIELD)_attr.getNodeValue();


#int
#serialize:
#with default value:
if($(OWNER)$(FIELD) != $(DEFAULT_VALUE))
{
    ((Element)xml).setAttribute("$(FIELD)", Integer.toString($(OWNER)$(FIELD)));
}
#without default value:
((Element)xml).setAttribute("$(FIELD)", Integer.toString($(OWNER)$(FIELD)));
#deserialize:
#with default value:
var $(FIELD)_attr = xml.getAttributes().getNamedItem("$(FIELD)");
if ($(FIELD)_attr != null)
{
    $(OWNER)$(FIELD) = Integer.valueOf($(FIELD)_attr.getNodeValue());
}
#without default value:
$(OWNER)$(FIELD) = $(TYPE).valueOf($(FIELD)_attr.getNodeValue());

#float
#serialize:
#with default value:
if($(OWNER)$(FIELD) != $(DEFAULT_VALUE))
{
    ((Element)xml).setAttribute("$(FIELD)", Float.toString($(OWNER)$(FIELD)));
}
#without default value:
((Element)xml).setAttribute("$(FIELD)", Float.toString($(OWNER)$(FIELD)));
#deserialize:
#with default value:
var $(FIELD)_attr = xml.getAttributes().getNamedItem("$(FIELD)");
if ($(FIELD)_attr != null)
{
    $(OWNER)$(FIELD) = Float.valueOf($(FIELD)_attr.getNodeValue());
}
#without default value:
$(OWNER)$(FIELD) = $(TYPE).valueOf($(FIELD)_attr.getNodeValue());

#bool
#serialize:
#with default value:
if($(OWNER)$(FIELD) != $(DEFAULT_VALUE))
{
    ((Element)xml).setAttribute("$(FIELD)", $(OWNER)$(FIELD) ? "yes" : "no");
}
#without default value:
((Element)xml).setAttribute("$(FIELD)", $(OWNER)$(FIELD) ? "yes" : "no");
#deserialize:
#with default value:
var $(FIELD)_attr = xml.getAttributes().getNamedItem("$(FIELD)");
if ($(FIELD)_attr != null)
{
    $(OWNER)$(FIELD) = $(FIELD)_attr.getNodeValue() == "yes";
}
#without default value:
$(OWNER)$(FIELD) = $(FIELD)_attr.getNodeValue() == "yes";


#serialized
#serialize:
$(OWNER)$(FIELD).serialize(xml.addChild("$(FIELD)"));
#deserialize:
$(OWNER)$(FIELD) = new $(TYPE);
$(OWNER)$(FIELD).deserialize(xml.$(FIELD));

#pointer
#serialize
if($(OWNER)$(FIELD))
{
    $child = xml.addChild("$(FIELD)");
    $child.setAttribute("type", $(OWNER)$(FIELD).get_type());
    $(OWNER)$(FIELD).serialize($child);
}
#deserialize:
if(xml.$(FIELD))
{
    $type = (string)xml.$(FIELD)["type"];
    $(OWNER)$(FIELD) = Factory::build($type);
    $(OWNER)$(FIELD).deserialize(xml.$(FIELD));
}


#list<int>, list<bool>, list<float>, list<string>
#serialize:
var xml_$(FIELD) = xml.getOwnerDocument().createElement("$(FIELD)");
for ($(ARG_0) item : this.$(FIELD))
{
    var xml_item = xml.getOwnerDocument().createElement("item");
    xml_item.setAttribute("value", item.toString());
    xml_item.appendChild(xml_item);
}
xml.appendChild(xml_$(FIELD));
#deserialize:
        var $(FIELD)_xml = ((Element)xml).getElementsByTagName("$(FIELD)");
        if ($(FIELD)_xml != null)
        {
            var node = (Node)$(FIELD)_xml;
            var children = node.getChildNodes();
            for (int i=0; i<children.getLength(); ++i)
            {
                var item = children.item(i).getAttributes().getNamedItem("value").getNodeValue();
                this.$(FIELD).add($(ARG_0).valueOf(item));
            }
        }


#list<serialized>
#serialize:
xml_list = xml.addChild("$(FIELD)");
foreach($(OWNER)$(FIELD) as $item)
{
    $item.serialize(xml_list.addChild("item"));
}
#deserialize:
if(xml.$(FIELD))
{
    foreach(xml.$(FIELD).children() as $item)
    {
        $obj = new $(TYPE)();
        $obj.deserialize($item);
        array_push($(OWNER)$(FIELD), $obj);
    }
}


#list<pointer>
#serialize:
xml_list = xml.addChild("$(FIELD)");
foreach($(OWNER)$(FIELD) as $item)
{
    $item.serialize(xml_list.addChild($item.get_type()));
}
#deserialize:
if(xml.$(FIELD))
{
    foreach(xml.$(FIELD).children() as $item)
    {
        $type = $item.getName();
        $obj = Factory::build($type);
        $obj.deserialize($item);
        array_push($(OWNER)$(FIELD), $obj);
    }
}


#link
#serialize:
xml.setAttribute("$(FIELD)", is_string($(OWNER)$(FIELD)) ? $(OWNER)$(FIELD) : $(OWNER)$(FIELD).name);
#deserialize:
$(OWNER)$(FIELD) = DataStorage::shared().get$(TYPE)((string)xml["$(FIELD)"]);


#list<link>
#serialize:
xml_list = xml.addChild("$(FIELD)");
foreach($(OWNER)$(FIELD) as $item)
{
    xml_list.addChild("item").setAttribute("value", is_string($item) ? $item : $item.name);
}
#deserialize:
foreach(xml.$(FIELD).item as $item)
{
    array_push($(OWNER)$(FIELD), DataStorage::shared().get$(ARG_0)((string)$item["value"]));
}

#map
#serialize:
$map_$(FIELD) = xml.addChild("$(FIELD)");
xml_main = xml;
foreach($(OWNER)$(FIELD) as $key => $value)
{
    xml = $map_$(FIELD).addChild("pair");
    $(KEY_SERIALIZE)
    $(VALUE_SERIALIZE)
}
xml = xml_main;
#deserialize:
xml_cache = xml;
if(xml.$(FIELD))
{
    foreach(xml.$(FIELD).children() as xml_child)
    {
        xml = xml_child;
        $(VALUE)
        $(KEY_SERIALIZE)
        map_key = (string)key;
        $(VALUE_SERIALIZE)
        $(OWNER)$(FIELD)[map_key] = $value;
    }
}
xml = xml_cache;


#enum
#serialize:
xml.setAttribute("$(FIELD)", $(OWNER)$(FIELD));
#deserialize:
$(OWNER)$(FIELD) = (string)(xml["$(FIELD)"]);
'''

java_json = '''

#int,bool,float,string
#serialize:
#with default value:
if($(OWNER)$(FIELD) != $(DEFAULT_VALUE))
{
    json.$(FIELD) = ($(TYPE))$(OWNER)$(FIELD);
}
#without default value:
json.$(FIELD) = ($(TYPE))$(OWNER)$(FIELD);
#deserialize:
#with default value:
if(isset(json.$(FIELD)))
{
    $(OWNER)$(FIELD) = json.$(FIELD);
}
#without default value:
$(OWNER)$(FIELD) = json.$(FIELD);


#serialized
#serialize:
json.$(FIELD) = json_decode("{}");
$(OWNER)$(FIELD).serialize(json.$(FIELD));
#deserialize:
$(OWNER)$(FIELD) = new $(TYPE);
$(OWNER)$(FIELD).deserialize(json.$(FIELD));

#pointer
#serialize
if($(OWNER)$(FIELD))
{
    $type = $(OWNER)$(FIELD).get_type();
    json.$(FIELD)        = json_decode("{}");
    json.$(FIELD).$type = json_decode("{}");
    $(OWNER)$(FIELD).serialize(json.$(FIELD).$type);
}
#deserialize:
if(isset(json.$(FIELD)))
{
    $type = (string) key(json.$(FIELD));
    $(OWNER)$(FIELD) = Factory::build($type);
    $(OWNER)$(FIELD).deserialize(json.$(FIELD).$type);
}


#list<int>, list<bool>, list<float>, list<string>
#serialize:
json.$(FIELD) = array();
foreach($(OWNER)$(FIELD) as $item)
{
    array_push(json.$(FIELD), $item);
}
#deserialize:
if(isset(json.$(FIELD)))
{
    foreach(json.$(FIELD) as $item)
    {
        array_push($(OWNER)$(FIELD), $item);
    }
}


#list<serialized>
#serialize:
json.$(FIELD) = array();
foreach($(OWNER)$(FIELD) as $item)
{
    array_push(json.$(FIELD), "");
    $item.serialize(json.$(FIELD)[count(json.$(FIELD))]);
}
#deserialize:
foreach(json.$(FIELD) as $item)
{
    $obj = new $(TYPE)();
    $obj.deserialize($item);
    array_push($(OWNER)$(FIELD), $obj);
}

#list<pointer>
#serialize:
json.$(FIELD) = array();
foreach($(OWNER)$(FIELD) as $t)
{
    $obj        = json_decode("{}");
    $obj.$type = json_decode("{}");
    $t.serialize($obj.$type);
    array_push(json.$(FIELD), $obj);
}
#deserialize:
$arr_$(FIELD) = json.$(FIELD);
foreach($arr_$(FIELD) as $item)
{
    $type = key($item);
    $obj = Factory::build($type);
    $obj.deserialize($item.$type);
    array_push($(OWNER)$(FIELD), $obj);
}


#link
#serialize:
json.$(FIELD) = $(OWNER)$(FIELD).name;
#deserialize:
$name = json.$(FIELD);
$(OWNER)$(FIELD) = DataStorage::shared().get$(TYPE)((string)$name);

#list<link>
#serialize:
json[$(FIELD)] = array();
foreach($(OWNER)$(FIELD) as $data)
{
    array_push(json[$(FIELD)], $data.name);
}
#deserialize:
foreach(json.$(FIELD) as $name)
{
    $data = DataStorage::shared().get$(ARG_0)((string)$name);
    array_push($(OWNER)$(FIELD), $data);
}

#map
#serialize:
$map_$(FIELD) = array();
json_main          = json;
foreach ($(OWNER)$(FIELD) as $key => $value)
{
    $arr = json_decode("{}");
    json = $arr;
    $(KEY_SERIALIZE)
    $(VALUE_SERIALIZE)

    array_push($map_$(FIELD), $arr);
}
json = json_main;
json.$(FIELD) = $map_$(FIELD);
#deserialize:
json_cache = json;
if(isset(json.$(FIELD)))
{
    $arr = json.$(FIELD);
    foreach($arr as json)
    {
        $(VALUE)
        $(KEY_SERIALIZE)
        map_key = (string)key;
        $(VALUE_SERIALIZE)
        $(OWNER)$(FIELD)[map_key] = $value;
    }
}
json = json_cache;



#enum
#serialize:
json.$(FIELD) = $(OWNER)$(FIELD);
#deserialize:
$(OWNER)$(FIELD) = (string)(json.$(FIELD));

'''
