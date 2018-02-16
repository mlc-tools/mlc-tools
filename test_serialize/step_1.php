<?php

require_once "generated_php/TestData.php";

$xml  = simplexml_load_file('data.py.xml');
$data = new TestData();
$data->deserialize($xml);

$xml = simplexml_load_string('<data/>');
$data->serialize($xml);

$string = $xml->asXML();
file_put_contents('data.php.xml', $string);

?>