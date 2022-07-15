PHP_XML = '''
#string
#serialize:
#with default value:
if($(OWNER)$(FIELD) != $(DEFAULT_VALUE))
{
    $xml->addAttribute("$(FIELD)", $(OWNER)$(FIELD));
}
#without default value:
$xml->addAttribute("$(FIELD)", $(OWNER)$(FIELD));
#deserialize:
#with default value:
if($xml["$(FIELD)"])
{
    $(OWNER)$(FIELD) = (string)$xml["$(FIELD)"];
}
#without default value:
$(OWNER)$(FIELD) = (string)$xml["$(FIELD)"];


#float, int
#serialize:
#with default value:
if($(OWNER)$(FIELD) != $(DEFAULT_VALUE))
{
    $xml->addAttribute("$(FIELD)", $(OWNER)$(FIELD));
}
#without default value:
$xml->addAttribute("$(FIELD)", $(OWNER)$(FIELD));
#deserialize:
#with default value:
if($xml["$(FIELD)"])
{
    $(OWNER)$(FIELD) = ($(TYPE))$xml["$(FIELD)"];
}
#without default value:
$(OWNER)$(FIELD) = ($(TYPE))$xml["$(FIELD)"];

#bool
#serialize:
#with default value:
if($(OWNER)$(FIELD) != $(DEFAULT_VALUE))
{
    $xml->addAttribute("$(FIELD)", $(OWNER)$(FIELD) ? 'yes' : 'no');
}
#without default value:
$xml->addAttribute("$(FIELD)", $(OWNER)$(FIELD) ? 'yes' : 'no');
#deserialize:
#with default value:
if(isset($xml["$(FIELD)"]))
{
    $value = strtolower((string)$xml["$(FIELD)"]);
    $(OWNER)$(FIELD) = ($value == 'true' || $value == 'yes');
}
#without default value:
$value = strtolower((string)$xml["$(FIELD)"]);
$(OWNER)$(FIELD) = ($value == 'true' || $value == 'yes');


#serialized
#serialize:
$(OWNER)$(FIELD)->serialize_$(FORMAT)($xml->addChild("$(FIELD)"));
#deserialize:
$(OWNER)$(FIELD) = new $(TYPE);
$(OWNER)$(FIELD)->deserialize_$(FORMAT)($xml->$(FIELD));

#pointer
#serialize
if($(OWNER)$(FIELD))
{
    $child = $xml->addChild("$(FIELD)");
    $child->addAttribute("type", $(OWNER)$(FIELD)->get_type());
    $(OWNER)$(FIELD)->serialize_$(FORMAT)($child);
}
#deserialize:
if($xml->$(FIELD))
{
    $type = (string)$xml->$(FIELD)["type"];
    $(OWNER)$(FIELD) = Factory::build($type);
    if($(OWNER)$(FIELD))
    {
        $(OWNER)$(FIELD)->deserialize_$(FORMAT)($xml->$(FIELD));
    }
}


#list<int>, list<float>, list<string>
#serialize:
$xml_list = $xml->addChild("$(FIELD)");
foreach($(OWNER)$(FIELD) as $item)
{
    $xml_list->addChild("item")->addAttribute("value", $item);
}
#deserialize:
if($xml->$(FIELD))
{
    foreach($xml->$(FIELD)->item as $item)
    {
        array_push($(OWNER)$(FIELD), ($(ARG_0))$item["value"]);
    }
}
#list<bool>
#serialize:
$xml_list = $xml->addChild("$(FIELD)");
foreach($(OWNER)$(FIELD) as $item)
{
    $xml_list->addChild("item")->addAttribute("value", $item ? 'yes' : 'no');
}
#deserialize:
if($xml->$(FIELD))
{
    foreach($xml->$(FIELD)->item as $item)
    {
        $value = strtolower((string)$item["value"]);
        array_push($(OWNER)$(FIELD), ($value == 'true' || $value == 'yes'));
    }
}

#list<serialized>
#serialize:
$xml_list = $xml->addChild("$(FIELD)");
foreach($(OWNER)$(FIELD) as $item)
{
    $item->serialize_$(FORMAT)($xml_list->addChild("item"));
}
#deserialize:
if($xml->$(FIELD))
{
    foreach($xml->$(FIELD)->children() as $item)
    {
        $obj = new $(TYPE)();
        $obj->deserialize_$(FORMAT)($item);
        array_push($(OWNER)$(FIELD), $obj);
    }
}


#list<pointer>
#serialize:
$xml_list = $xml->addChild("$(FIELD)");
foreach($(OWNER)$(FIELD) as $item)
{
    $xml_child = $xml_list->addChild($item ? $item->get_type() : "null");
    if($item)
    {
        $item->serialize_$(FORMAT)($xml_list->addChild($item->get_type()));
    }
}
#deserialize:
if($xml->$(FIELD))
{
    foreach($xml->$(FIELD)->children() as $item)
    {
        $type = $item->getName();
        $obj = Factory::build($type);
        if($obj)
        {
            $obj->deserialize_$(FORMAT)($item);
        }
        array_push($(OWNER)$(FIELD), $obj);
    }
}


#link
#serialize:
$xml->addAttribute("$(FIELD)", is_string($(OWNER)$(FIELD)) ? $(OWNER)$(FIELD) : $(OWNER)$(FIELD)->name);
#deserialize:
$(OWNER)$(FIELD) = DataStorage::shared()->get$(TYPE)((string)$xml["$(FIELD)"]);


#list<link>
#serialize:
$xml_list = $xml->addChild("$(FIELD)");
foreach($(OWNER)$(FIELD) as $item)
{
    $xml_list->addChild("item")->addAttribute("value", is_string($item) ? $item : $item->name);
}
#deserialize:
foreach($xml->$(FIELD)->item as $item)
{
    array_push($(OWNER)$(FIELD), DataStorage::shared()->get$(ARG_0)((string)$item["value"]));
}

#map
#serialize:
$map_$(FIELD) = $xml->addChild("$(FIELD)");
$xml_main = $xml;
foreach($(OWNER)$(FIELD) as $key => $value)
{
    $xml = $map_$(FIELD)->addChild("pair");
    $(KEY_SERIALIZE)
    $(VALUE_SERIALIZE)
}
$xml = $xml_main;
#deserialize:
$xml_cache = $xml;
if($xml->$(FIELD))
{
    foreach($xml->$(FIELD)->children() as $xml_child)
    {
        $xml = $xml_child;
        $(VALUE)
        $(KEY_SERIALIZE)
        $map_key = (string)$key;
        $(VALUE_SERIALIZE)
        $(OWNER)$(FIELD)[$map_key] = $value;
    }
}
$xml = $xml_cache;


#enum
#serialize:
$xml->addAttribute("$(FIELD)", $(OWNER)$(FIELD));
#deserialize:
$(OWNER)$(FIELD) = (string)($xml["$(FIELD)"]);
'''

PHP_JSON = '''

#int,bool,float,string
#serialize:
#with default value:
if($(OWNER)$(FIELD) != $(DEFAULT_VALUE))
{
    $json->$(FIELD) = ($(TYPE))$(OWNER)$(FIELD);
}
#without default value:
$json->$(FIELD) = ($(TYPE))$(OWNER)$(FIELD);
#deserialize:
#with default value:
if(isset($json->$(FIELD)))
{
    $(OWNER)$(FIELD) = ($(TYPE))$json->$(FIELD);
}
#without default value:
$(OWNER)$(FIELD) = $json->$(FIELD);


#serialized
#serialize:
$json->$(FIELD) = json_decode("{}");
$(OWNER)$(FIELD)->serialize_$(FORMAT)($json->$(FIELD));
#deserialize:
if(isset($json->$(FIELD)))
{
    $(OWNER)$(FIELD) = new $(TYPE);
    $(OWNER)$(FIELD)->deserialize_$(FORMAT)($json->$(FIELD));
}
#pointer
#serialize
if($(OWNER)$(FIELD))
{
    $type = $(OWNER)$(FIELD)->get_type();
    $json->$(FIELD)        = json_decode("{}");
    $json->$(FIELD)->type  = $type;
    $(OWNER)$(FIELD)->serialize_$(FORMAT)($json->$(FIELD));
}
#deserialize:
if(isset($json->$(FIELD)))
{
    $type = (string) $json->$(FIELD)->type;
    $(OWNER)$(FIELD) = Factory::build($type);
    if($(OWNER)$(FIELD))
    {
        $(OWNER)$(FIELD)->deserialize_$(FORMAT)($json->$(FIELD));
    }
}


#list<int>, list<bool>, list<float>, list<string>
#serialize:
$json->$(FIELD) = array();
foreach($(OWNER)$(FIELD) as $item)
{
    array_push($json->$(FIELD), $item);
}
#deserialize:
if(isset($json->$(FIELD)))
{
    foreach($json->$(FIELD) as $item)
    {
        array_push($(OWNER)$(FIELD), $item);
    }
}


#list<serialized>
#serialize:
$json->$(FIELD) = array();
foreach($(OWNER)$(FIELD) as $item)
{
    array_push($json->$(FIELD), "");
    $item->serialize_$(FORMAT)($json->$(FIELD)[count($json->$(FIELD))]);
}
#deserialize:
foreach($json->$(FIELD) as $item)
{
    $obj = new $(TYPE)();
    if($obj)
    {
        $obj->deserialize_$(FORMAT)($item);
    }
    array_push($(OWNER)$(FIELD), $obj);
}

#list<pointer>
#serialize:
$json->$(FIELD) = array();
foreach($(OWNER)$(FIELD) as $t)
{
    $type       = $t ? $t->get_type() : "";
    $obj        = json_decode("{}");
    $obj->$type = json_decode("{}");
    if ($t)
    {
        $t->serialize_$(FORMAT)($obj->$type);
    }
    array_push($json->$(FIELD), $obj);
}
#deserialize:
$arr_$(FIELD) = $json->$(FIELD);
foreach($arr_$(FIELD) as $item)
{
    $type = key($item);
    $obj = Factory::build($type);
    if($obj)
    {
        $obj->deserialize_$(FORMAT)($item->$type);
    }
    array_push($(OWNER)$(FIELD), $obj);
}


#link
#serialize:
$json->$(FIELD) = $(OWNER)$(FIELD)->name;
#deserialize:
$name = $json->$(FIELD);
$(OWNER)$(FIELD) = DataStorage::shared()->get$(TYPE)((string)$name);

#list<link>
#serialize:
$json->$(FIELD) = array();
foreach($(OWNER)$(FIELD) as $data)
{
    array_push($json->$(FIELD), $data ? $data->name : "");
}
#deserialize:
foreach($json->$(FIELD) as $name)
{
    $data = DataStorage::shared()->get$(ARG_0)((string)$name);
    array_push($(OWNER)$(FIELD), $data);
}

#map
#serialize:
$map_$(FIELD) = array();
$json_main          = $json;
foreach ($(OWNER)$(FIELD) as $key => $value)
{
    $arr = json_decode("{}");
    $json = $arr;
    $(KEY_SERIALIZE)
    $(VALUE_SERIALIZE)

    array_push($map_$(FIELD), $arr);
}
$json = $json_main;
$json->$(FIELD) = $map_$(FIELD);
#deserialize:
$json_cache = $json;
if(isset($json->$(FIELD)))
{
    $arr = $json->$(FIELD);
    foreach($arr as $json)
    {
        $(VALUE)
        $(KEY_SERIALIZE)
        $map_key = (string)$key;
        $(VALUE_SERIALIZE)
        $(OWNER)$(FIELD)[$map_key] = $value;
    }
}
$json = $json_cache;



#enum
#serialize:
$json->$(FIELD) = $(OWNER)$(FIELD);
#deserialize:
if(isset($json->$(FIELD)))
{
    $(OWNER)$(FIELD) = (string)($json->$(FIELD));
}
'''
