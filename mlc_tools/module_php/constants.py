FACTORY = '''<?php

class Factory
{
    static function build($type)
    {
        if(strcmp($type, "") == 0 || strcmp($type, "null") == 0)
        {
            return null;
        }
        try {
            require_once "$type.php";
            return new $type;
        } catch (Exception $e) {
            return null;
        }
    }
};

?>
'''

COMMON_XML = '''
function create_command_from_xml($payload)
{
    $xml     = simplexml_load_string($payload);
    $class   = $xml->getName();
    require_once "$class.php";
    $command = new $class;
    $command->deserialize_xml($xml);
    return $command;
}

function serialize_command_to_xml($command)
{
    $xml = simplexml_load_string('<'.$command->get_type().'/>');
    $command->serialize_xml($xml);
    return $xml->asXML();
}
'''

COMMON_JSON = '''
function create_command_from_json($payload)
{
    $json    = json_decode($payload);
    $class   = key($json);
    require_once "$class.php";
    $command = new $class;
    $command->deserialize_json($json->$class);
    return $command;
}

function serialize_command_to_json($command)
{
    $type = $command->get_type();
    $json = json_decode('{"'.$type.'": {}}');
    $command->serialize_json($json->$type);
    return json_encode($json, JSON_PRETTY_PRINT);
}
'''

CLONE_XML = '''
function clone_object($obj)
{
    $payload = serialize_command_to_xml($obj);
    $clone = create_command_from_xml($payload);
    return $clone;
}
'''

CLONE_JSON = '''
function clone_object($obj)
{
    $payload = serialize_command_to_json($obj);
    $clone = create_command_from_json($payload);
    return $clone;
}
'''

COMMON = '''<?php
@{xml}
@{json}

function mg_swap(&$x, &$y) {
    list($x,$y) = array($y, $x);
}

?>
'''