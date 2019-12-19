<?php
declare(strict_types=1);

require_once 'generated_php/RunAllTests.php';
require_once 'generated_php/Logger.php';
require_once 'generated_php/TestDataBase.php';
require_once 'lib/php/DataBase.php';

class LoggerImpl extends Logger {
	function message(string $message) {
		echo ("$message\n);
	}
};

function run_test($db) {
	TestDataBase::$db = $db;
	$logger           = new LoggerImpl();
	$tests            = new RunAllTests();
	$tests->initialize($logger);
	return $tests->execute();
}

$result = true;
$result = run_test(new DataBaseMySql()) && $result;
$result = run_test(new DataBaseSqlite()) && $result;
echo ("\n\n");
exit($result == true?0:1);

?>