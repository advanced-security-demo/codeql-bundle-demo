<h1>Application</h1>
<?php

$connection = new PDO('mysql:host=localhost;dbname=demo', 'demo', 'demo');
$statement  = $connection->query('SELECT message FROM demo');

echo $statement->fetchColumn();