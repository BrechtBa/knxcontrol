<?php
	session_start();
	include('../data/mysql.php');

	if($_SESSION['userid']>0){
		
		$ip = $_POST['ip'];
		$port = $_POST['port'];
		$webip = $_POST['webip'];
		$webport = $_POST['webport'];
		$token = $_POST['token'];
		
		$query = "UPDATE data SET ip='$ip', port=$port, web_ip='$webip', web_port=$webport, token=$token WHERE id=1";
		$result = mysql_query($query) or die('Error: ' . mysql_error());
		
	}
?>