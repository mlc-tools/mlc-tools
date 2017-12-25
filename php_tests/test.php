<?php

function test_enums(){
    require_once "gen/EnumTest.php";
    require_once "gen/EnumHolder.php";

    $xml_data = '<data value="test_value_1"><map><pair key="test_value_2" value="string_value"/></map></data>';
    $xml = simplexml_load_string($xml_data);

    $test = new EnumHolder();
    $test->deserialize($xml);

    $value = EnumTest::$test_value_2;
    if(strcmp($test->map[$value], "string_value") != 0){
        echo("\nCompare map value with key - fail\n");
        var_dump($test);
    } else {
        echo("\nCompare map value with key - Ok");
    }

    $xml = simplexml_load_string('<data/>');
    $test->serialize($xml);

    $test2 = new EnumHolder();
    $test2->deserialize($xml);
    if($test2->value != $test->value && $test->map != $test2->map){
        echo("\nCompare two serialized-deserialized object with original - fail");
    } else {
        echo("\nCompare two serialized-deserialized object with original - Ok");
    }
}


function test_factory(){
    require_once "gen/Factory.php";
    require_once "gen/FactoryTest.php";

    $xml_data = '<data><ptr type="EnumHolder" value="test_value_1"><map><pair key="test_value_2" value="string_value"/></map></ptr></data>';
    $xml = simplexml_load_string($xml_data);

    $test = new FactoryTest();
    $test->deserialize($xml);
    if(is_null($test) || is_null($test->ptr)){
        echo("\nDeserialized pointer - fail");
    }else{
        echo("\nDeserialized pointer - Ok");
    }
}

test_enums();
test_factory();
?>