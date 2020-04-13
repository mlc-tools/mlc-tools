<?php
declare(strict_types=1);

require_once 'generated_php/RunAllTests.php';
require_once 'generated_php/Logger.php';

class LoggerImpl extends Logger {
	function message(string $message) {
		echo ("$message\n");
	}
};


$logger           = new LoggerImpl();
$tests            = new RunAllTests();
$tests->initialize($logger);
$result = $tests->execute();

exit($result == true?0:1);

?>