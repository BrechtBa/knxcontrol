<?php

	include('../data/mysql.php');
	
	$id = $_POST['id'];
	
	// add alarm to the mysql database
	$query = "DELETE FROM alarms WHERE id=$id";
	$result = mysql_query($query) or die('Error: ' . mysql_error());

?>