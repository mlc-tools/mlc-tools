<?php
require_once __DIR__ .'/../../generated_php/DataBase.php';

class DataBaseMySql extends DataBase {
	private static $mysqli;

	public function connect($host, $database, $user, $password) {
		DataBaseMySql::$mysqli = new mysqli($host, $user, $password, $database);
		if (DataBaseMySql::$mysqli->connect_error) {
			die('Connect Error ('.DataBaseMySql::$mysqli->connect_errno.') '.DataBaseMySql::$mysqli->connect_error);
		}
	}
	public function query_all($query) {
		$response = DataBaseMySql::$mysqli->query($query) or die('Query error: '.DataBaseMySql::$mysqli->error."\nQuery: $query\n");
		if (is_bool($response)) {
			return array();
		}
		$result = array();
		$row    = $response->fetch_array(MYSQLI_ASSOC);
		while ($row) {
			array_push($result, $row);
			$row = $response->fetch_array(MYSQLI_ASSOC);
		}
		return $result;
	}
	public function query_one($query) {
		$response = DataBaseMySql::$mysqli->query($query) or die('Query error: '.DataBaseMySql::$mysqli->error."\nQuery: $query\n");
		if (is_bool($response)) {
			return array();
		}
		return $response->fetch_array(MYSQLI_ASSOC);
	}
}

class DataBaseSqlite extends DataBase {
	private static $db;

	public function connect($host, $database, $user, $password) {
		$file = $database.".db";

		DataBaseSqlite::$db = new SQLite3($file);
	}
	public function query_all($query) {
		$response = DataBaseSqlite::$db->query($query);
		if (is_bool($response)) {
			return array();
		}

		$result = array();
		while ($response->numColumns() && $row = $response->fetchArray()) {
			$row2 = array();
			foreach ($row as $key => $value) {
				if (is_int($key)) {
					array_push($row2, $value);
				}
			}
			array_push($result, $row2);
		}
		return $result;
	}
	public function query_one($query) {
		$response = DataBaseSqlite::$db->query($query);
		if (is_bool($response)) {
			return array();
		}

		if ($response->numColumns() && $row = $response->fetchArray()) {
			$row2 = array();
			foreach ($row as $key => $value) {
				if (is_int($key)) {
					array_push($row2, $value);
				}
			}
			return $row2;
		}
		return array();
	}
}

?>