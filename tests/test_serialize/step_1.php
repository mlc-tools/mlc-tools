<?php

require_once "generated_php/TestData.php";
require_once "generated_php/config.php";

if ($MG_SERIALIZE_FORMAT == $MG_XML) {
	$xml  = simplexml_load_file('data.py.xml');
	$data = new TestData();
	$data->deserialize($xml);

	$xml = simplexml_load_string('<data/>');
	$data->serialize($xml);

	$string = $xml->asXML();
	file_put_contents('data.php.xml', $string);
} else {
	$string = file_get_contents('data.py.json');
	$json   = json_decode($string);

	$data = new TestData();
	$data->deserialize($json);

	// var_dump($data->object_ptr_map);

	$json = json_decode('{}');
	$data->serialize($json);

	$string = json_encode($json, JSON_PRETTY_PRINT);
	file_put_contents('data.php.json', $string);
}
?>