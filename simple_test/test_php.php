<?php

require_once 'generated_php/DataStorage.php';
require_once 'generated_php/AllTests.php';

$file = 'data.xml';
if (count($argv) > 1) {
	$file = 'data.'.$argv[1];
}

$file = realpath(dirname(__FILE__))."/assets/$file";

DataStorage::$PATH_TO_DATA = $file;
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