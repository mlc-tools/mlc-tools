<?php

require_once "EnumHolder.php";
require_once "Factory.php";

class FactoryTest
{
	//members:
	public $ptr = None;
	public static $__type__ = "FactoryTest";
	
	//functions
	public function get_type()
	{
		return FactoryTest::$__type__;
	}
	public function serialize($xml)
	{
		if(ptr)
		{
			$child = $xml->addChild("ptr");
			$child->addAttribute("type", $this->ptr->get_type());
			$this->ptr->serialize($child);
		}
	}
	public function deserialize($xml)
	{
		if($xml->ptr)
		{
			$type = (string)$xml->ptr["type"];
			$this->ptr = Factory::build($type);
			$this->ptr->deserialize($xml->ptr);
		}
	}
	
};

?>