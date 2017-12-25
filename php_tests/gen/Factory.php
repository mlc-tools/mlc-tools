
<?php

class Factory
{
	static function build($type)
	{
		require_once "$type.php";
		return new $type;
	}
};

?>
