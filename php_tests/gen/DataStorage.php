<?php

require_once "Factory.php";

class DataStorage
{
	//members:
	public $_loaded = false;
	public static $__instance = NULL;
	public static $__xml = NULL;
	
	//functions
	public function shared()
	{
		if(DataStorage::$__instance == NULL)
		{
			DataStorage::$__instance = new DataStorage();
			DataStorage::$__xml = simplexml_load_file("assets/data/data.xml");
		}
		return DataStorage::$__instance;
	}
	public function initialize($buffer)
	{
		$root = simplexml_load_string(buffer);
		$this->deserialize(root);
		$this->_loaded = true;
	}
	public function deserialize($xml)
	{
		
	}
	public function serialize($xml)
	{
		
	}
	
};

?>