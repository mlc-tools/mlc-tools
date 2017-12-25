<?php

require_once "Factory.php";

class SerializedObject
{
	//members:
	public $_reference_counter = 1;
	public static $__type__ = "SerializedObject";
	
	//functions
	public function get_type()
	{
		return SerializedObject::$__type__;
	}
	public function serialize($xml)
	{
		
	}
	public function deserialize($xml)
	{
		
	}
	
};

?>