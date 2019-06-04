
from .writer import Writer

class GeneratorFactory(object):

    def __init__(self):
        pass

    @staticmethod
    def generate(model):
        writer = Writer('')
        writer.model = model
        content = writer.prepare_file(FACTORY)
        model.add_file('Factory.php', content)


FACTORY = '''<?php

class Factory
{
    static function build($type)
    {
        require_once "$type.php";
        return new $type;
    }
    {{format=xml}}
    static function create_command_from_xml($payload)
    {
        $xml     = simplexml_load_string($payload);
        $class   = $xml->getName();
        require_once "$class.php";
        $command = new $class;
        $command->deserialize_xml($xml);
        return $command;
    }

    static function serialize_command_to_xml($command)
    {
        $xml = simplexml_load_string('<'.$command->get_type().'/>');
        $command->serialize_xml($xml);
        return $xml->asXML();
    }

    static function clone_object($obj)
    {
        $payload = Factory::serialize_command_to_xml($obj);
        $clone = Factory::create_command_from_xml($payload);
        return $clone;
    }
    {{end_format=xml}}
    {{format=json}}
    static function create_command_from_json($payload)
    {
        $json    = json_decode($payload);
        $class   = key($json);
        require_once "$class.php";
        $command = new $class;
        $command->deserialize_json($json->$class);
        return $command;
    }

    static function serialize_command_to_json($command)
    {
        $type = $command->get_type();
        $json = json_decode('{"'.$type.'": {}}');
        $command->serialize_json($json->$type);
        return json_encode($json, JSON_PRETTY_PRINT);
    }

    static function clone_object($obj)
    {
        $payload = Factory::serialize_command_to_json($obj);
        $clone = Factory::create_command_from_json($payload);
        return $clone;
    }
    {{end_format=json}}
    {{format=both}}
    static function create_command_from_xml($payload)
    {
        $xml     = simplexml_load_string($payload);
        $class   = $xml->getName();
        require_once "$class.php";
        $command = new $class;
        $command->deserialize_xml($xml);
        return $command;
    }

    static function serialize_command_to_xml($command)
    {
        $xml = simplexml_load_string('<'.$command->get_type().'/>');
        $command->serialize_xml($xml);
        return $xml->asXML();
    }
    
    static function create_command_from_json($payload)
    {
        $json    = json_decode($payload);
        $class   = key($json);
        require_once "$class.php";
        $command = new $class;
        $command->deserialize_json($json->$class);
        return $command;
    }

    static function serialize_command_to_json($command)
    {
        $type = $command->get_type();
        $json = json_decode('{"'.$type.'": {}}');
        $command->serialize_json($json->$type);
        return json_encode($json, JSON_PRETTY_PRINT);
    }

    static function clone_object($obj)
    {
        $payload = Factory::serialize_command_to_json($obj);
        $clone = Factory::create_command_from_json($payload);
        return $clone;
    }
    {{end_format=both}}

};

?>'''
