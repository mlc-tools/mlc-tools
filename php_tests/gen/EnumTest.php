<?php

require_once "Factory.php";

class EnumTest
{
	//members:
	public static $test_value_1 = (1 << 0);
	public static $test_value_2 = (1 << 1);
	public $_value = (1 << 0);
	
	//functions
	public function __toString()
	{
		if($this->_value == EnumTest::$test_value_1)return "test_value_1";
		if($this->_value == 1)
		{
			$this->_value = EnumTest::$test_value_1; return "test_value_1";
		}
		
		if($this->_value == "1")
		{
			$this->_value = EnumTest::$test_value_1; return "test_value_1";
		}
		;
		if($this->_value == EnumTest::$test_value_2)return "test_value_2";
		if($this->_value == 2)
		{
			$this->_value = EnumTest::$test_value_2; return "test_value_2";
		}
		
		if($this->_value == "2")
		{
			$this->_value = EnumTest::$test_value_2; return "test_value_2";
		}
		;
	}
	public function str()
	{
		return (string)$this;
	}
	public function set($value)
	{
		if($value == EnumTest::$test_value_1) $this->_value = EnumTest::$test_value_1;
		if($value == "1") $this->_value = EnumTest::$test_value_1;
		if($value == "test_value_1") $this->_value = EnumTest::$test_value_1;
		if($value == EnumTest::$test_value_2) $this->_value = EnumTest::$test_value_2;
		if($value == "2") $this->_value = EnumTest::$test_value_2;
		if($value == "test_value_2") $this->_value = EnumTest::$test_value_2;
	}
	public function int()
	{
		if($this->_value == EnumTest::$test_value_1) return EnumTest::$test_value_1;
		if($this->_value == "1") return EnumTest::$test_value_1;
		if($this->_value == "test_value_1") return EnumTest::$test_value_1;
		if($this->_value == EnumTest::$test_value_2) return EnumTest::$test_value_2;
		if($this->_value == "2") return EnumTest::$test_value_2;
		if($this->_value == "test_value_2") return EnumTest::$test_value_2;
	}
	public function s_to_int($value)
	{
		if($value == EnumTest::$test_value_1) return EnumTest::$test_value_1;
		if($value == "1") return EnumTest::$test_value_1;
		if($value == "test_value_1") return EnumTest::$test_value_1;
		if($value == EnumTest::$test_value_2) return EnumTest::$test_value_2;
		if($value == "2") return EnumTest::$test_value_2;
		if($value == "test_value_2") return EnumTest::$test_value_2;
	}
	public function serialize()
	{
		
	}
	public function deserialize()
	{
		
	}
	
};

?>