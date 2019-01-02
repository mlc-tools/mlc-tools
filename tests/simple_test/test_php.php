<?php

require_once 'generated_php/DataStorage.php';
require_once 'generated_php/AllTests.php';
require_once 'generated_php/RunAllTests.php';
require_once 'generated_php/Logger.php';
require_once 'generated_php/config.php';

$file = 'data.xml';
if(!Config::$SUPPORT_XML_PROTOCOL){
	$file = 'data.json';
}

$file = realpath(dirname(__FILE__))."/assets/$file";

DataStorage::$PATH_TO_DATA = $file;
DataStorage::shared()->loadAllDataUnits();

class LoggerImpl extends Logger {
	function print_log($result, $message) {
		echo ("\n$message: " .($result?"Ok":"Fail"));
	}
};

$logger = new LoggerImpl();

$result = true;
$result = AllTests::run($logger) and $result;

$tests = new RunAllTests();
$tests->initialize($logger);
$result = $tests->execute() && $result;

echo ("\n\n");
exit($result == true?0:1);

?>