<?php

require_once 'generated_php/DataStorage.php';
require_once 'generated_php/AllTests.php';

DataStorage::$PATH_TO_DATA = realpath(dirname(__FILE__))."/assets/data.json";
DataStorage::shared()->loadAllDataUnits();

class Logger {
	function add_result($result, $message) {
		echo ("\n$message: " .($result?"Ok":"Fail"));
		return $result;
	}
};

$logger = new Logger();

$result = true;
$result = AllTests::run($logger) and $result;

echo ("\n\n");
exit($result == true?0:1);

?>