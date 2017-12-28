php_xml = '''
#string
#serialize:
#with default value:
$xml->addAttribute("$(FIELD)", $(OWNER)$(FIELD));
#without default value:
$xml->addAttribute("$(FIELD)", $(OWNER)$(FIELD));

#deserialize:
#with default value:
$(OWNER)$(FIELD) = (string)$xml["$(FIELD)"];
#without default value:
$(OWNER)$(FIELD) = (string)$xml["$(FIELD)"];


#float, int
#serialize:
#with default value:
$xml->addAttribute("$(FIELD)", $(OWNER)$(FIELD));
#without default value:
$xml->addAttribute("$(FIELD)", $(OWNER)$(FIELD));

#deserialize:
#with default value:
$(OWNER)$(FIELD) = ($(TYPE))$xml["$(FIELD)"];
#without default value:
$(OWNER)$(FIELD) = ($(TYPE))$xml["$(FIELD)"];

#bool
#serialize:
#with default value:
$xml->addAttribute("$(FIELD)", $(OWNER)$(FIELD) ? 'yes' : 'no');
#without default value:
$xml->addAttribute("$(FIELD)", $(OWNER)$(FIELD) ? 'yes' : 'no');

#deserialize:
#with default value:
$value = strtolower((string)$xml["$(FIELD)"]);
$(OWNER)$(FIELD) = ($value == 'true' || $value == 'yes');
#without default value:
$value = strtolower((string)$xml["$(FIELD)"]);
$(OWNER)$(FIELD) = ($value == 'true' || $value == 'yes');


#serialized
#serialize:
$(OWNER)$(FIELD)->serialize($xml->addChild("$(FIELD)"));
#deserialize:
$(OWNER)$(FIELD) = new $(TYPE);
$(OWNER)$(FIELD)->deserialize($xml->$(FIELD));

#pointer
#serialize
if($(FIELD))
{
    $child = $xml->addChild("$(FIELD)");
    $child->addAttribute("type", $(OWNER)$(FIELD)->get_type());
    $(OWNER)$(FIELD)->serialize($child);
}
#deserialize:
if($xml->$(FIELD))
{
    $type = (string)$xml->$(FIELD)["type"];
    $(OWNER)$(FIELD) = Factory::build($type);
    $(OWNER)$(FIELD)->deserialize($xml->$(FIELD));
}


#list<int>, list<bool>, list<float>, list<string>
#serialize:
$xml_list = $xml->addChild("$(FIELD)");
foreach($(OWNER)$(FIELD) as $item)
{
    $xml_list->addChild("item")->addAttribute("value", $item);
}
#deserialize:
foreach($xml->$(FIELD)->item as $item)
{
    array_push($(OWNER)$(FIELD), $item["value"]);
}

#list<serialized>
#serialize:
$xml_list = $xml->addChild("$(FIELD)");
foreach($(OWNER)$(FIELD) as $item)
{
    $item->serialize($xml_list->addChild("item"));
}
#deserialize:
if($xml->$(FIELD))
{
    foreach($xml->$(FIELD)->children() as $item)
    {
        $obj = new $(TYPE)();
        $obj->deserialize($item);
        array_push($(OWNER)$(FIELD), $obj);
    }
}


#pointer_list
#serialize:
$xml_list = $xml->addChild("$(FIELD)");
foreach($(OWNER)$(FIELD) as $item)
{
    $item->serialize($xml_list->addChild($item->get_type()));
}
#deserialize:
if($xml->$(FIELD))
{
    foreach($xml->$(FIELD)->children() as $item)
    {
        $type = $item->getName();
        $obj = Factory::build($type);
        $obj->deserialize($item);
        array_push($(OWNER)$(FIELD), $obj);
    }
}


#link
#serialize:
$xml->addAttribute("$(FIELD)", is_string($(OWNER)$(FIELD)) ? $(OWNER)$(FIELD) : $(OWNER)$(FIELD)->name);
#deserialize:
$(OWNER)$(FIELD) = (string)$xml["$(FIELD)"];


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
    array_push($(OWNER)$(FIELD), (string)$item["value"]);
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
foreach($xml->$(FIELD)->children() as $xml_child)
{
    $xml = $xml_child;
    $(VALUE)
    $(KEY_SERIALIZE)
    $map_key = (string)$key;
    $(VALUE_SERIALIZE)
    $(OWNER)$(FIELD)[$map_key] = $value;
}
$xml = $xml_cache;


#enum
#serialize:
$xml->addAttribute("$(FIELD)", $(OWNER)$(FIELD));
#deserialize:
$(OWNER)$(FIELD) = (string)($xml["$(FIELD)"]);
'''
