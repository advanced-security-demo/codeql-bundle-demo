<?php
require_once("top.php");
?>

<div id="main-container">
        <div id="main" class="wrapper clearfix">
        <content>
                <table class="list">
<?php
try {
	$dbh = new PDO("mysql:host=$host;dbname=demo", $user, $pass);
}
catch(PDOException $e)
{
	echo $e->getMessage();
	echo "Exiting";
	exit;
}

$account = urldecode($_GET["account"]);
if (is_numeric($account)) {
    echo "<ul>";
    echo "<li> $account </li>";
    echo "<li> $host </li>";
    echo "</ul>";
    $findAccountSTH = $dbh->prepare("select * from tracking where client_id = :accountID order by created desc");
    $findAccountSTH->execute(array(':accountID' => $account));
    $findAccountSTH->setFetchMode(PDO::FETCH_OBJ);  

    echo "<tr class='listHeader'> <td><b>Created</b></td> <td><b>Updated</b></td> <td><b>Status</b></td> <td><b>Interface</b></td><td><b>Operation</b></td><td><b>ID</b></td></tr>";
    while($row = $findAccountSTH->fetch()) 
    {
        echo "<tr><td>" . $row->created . "</td>";
            echo "<td>" . $row->updated . "</td>";
        if ($row->status == 'Error') { echo $cssTrick = '<td id="error">' . $row->status; } else { echo "<td> $row->status </td>"; };
        echo "<td>" . $row->interface . "</td>";
        echo "<td>" . $row->operation . "</td>";
        echo "<td><a href=detail.php?env=".$env. "&correlationID=" . urlencode($row->id) ." > " . $row->id . "</a></td>";
        echo "</tr>";

    }
    echo '</table>';
} else {
    echo 'ERROR: Account should be an integer<br />';
}
    echo '</content>';
require_once("footer.php");
?>
