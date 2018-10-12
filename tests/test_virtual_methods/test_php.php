<?php
require_once 'generated_php/RunAllTests.php';
require_once 'generated_php/Logger.php';

class LoggerImpl extends Logger {
	function print_log($result, $message) {
		echo ("\n$message: " .($result?"Ok":"Fail"));
	}
};


$logger           = new LoggerImpl();
$tests            = new RunAllTests();
$tests->initialize($logger);
$result = $tests->execute();

$percent = 100.0*$logger->implemented_methods_count/$logger->all_methods_count;
echo "\n\n";
echo "Sumary: $logger->success_count/$logger->tests_count success\n";
echo "  Count of classes: $logger->class_count\n";
echo "  Count of method: $logger->methods_count\n";
echo "  Count of all methods: $logger->all_methods_count\n";
echo "  Count of tested methods: $logger->implemented_methods_count\n";
echo "  Code coverage: $percent%\n\n";
echo "\n\n";
exit($result == true?0:1);

?>