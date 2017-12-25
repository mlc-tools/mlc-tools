<?php

require_once "EnumTest.php";
require_once "EnumTest.php";
require_once "Factory.php";

class EnumHolder
{
	//members:
	public $value = None;
	public $map = array();
	public static $__type__ = "EnumHolder";
	
	//functions
	public function get_type()
	{
		return EnumHolder::$__type__;
	}
	public function serialize($xml)
	{
		$xml->addAttribute("value", $this->value);
		$map_map = $xml->addChild("map");
		$xml_main = $xml;
		foreach($this->map as $key => $value)
		{
			$xml = $map_map->addChild("pair");
			$xml->addAttribute("key", $key);
			$xml->addAttribute("value", $value);
		}
		$xml = $xml_main;
		
	}
	public function deserialize($xml)
	{
		$this->value = EnumTest::s_to_int($xml["value"]);
		$xml_cache = $xml;
		foreach($xml->map->children() as $xml_child)
		{
			$xml = $xml_child;
			
			$key = EnumTest::s_to_int($xml["key"]);
			$map_key = (string)$key;
			$value = (string)$xml["value"];
			$this->map[$map_key] = $value;
		}
		$xml = $xml_cache;
		
	}
	
};

?>