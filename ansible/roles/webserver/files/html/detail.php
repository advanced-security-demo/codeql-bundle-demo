<?php
require_once("top.php");
require_once("xmlpp.php");
?>

<div id="main-container">
        <div id="main" class="wrapper clearfix">
        <content>
                <table class="list">
<?php
try {
	$dbh = new PDO("mysql:host=$host;dbname=demo", $user, $pass);
    $findChildSTH = $dbh->prepare("select t.id, t.client_id, t.user,t.interface, t.service, t.operation, t.status, t.server , t.correlation_id, t.created, t.updated, t.in, t.out, e.message, e.type,e.stack  from tracking t left join tracking_error e on t.id=e.tracking_id left outer join tracking pt on t.parent_id=pt.id where true     and t.correlation_id in ( :correlationID ) order by t.created desc");


}
catch(PDOException $e)
{
    echo $e->getMessage();
    echo "Exiting";
    exit;
}

$findChildSTH->execute(array(':correlationID' => $correlationID));

if ( $findChildSTH->rowCount() == 0){
    $findChildSTH = $dbh->prepare("select tracking.id, client_id, status, tracking_error.created, updated, interface, operation, message from tracking join tracking_error on tracking.id = tracking_error.tracking_id where tracking.id= :correlationID ");
    $findChildSTH->execute(array(':correlationID' => $correlationID));
}


$findChildSTH->setFetchMode(PDO::FETCH_OBJ);  

$detailData = $findChildSTH;

echo "<ul>";
echo "<li><a href=transaction.php?env=". $env . "&trackingId=" .urlencode($correlationID) ." > " . $correlationID . "</a></li>";
echo "<li> $host </li>";
echo "</ul>";

echo "<tr class='listHeader'> <td><b>Created</b></td> <td><b>Updated</b></td> <td><b>Status</b></td> <td><b>Interface</b></td><td><b>Operation</b></td><td><b>Account ID</b></td><td><b>Message</b></td><td><b>Stack</b></td></tr>";
while($row = $findChildSTH->fetch()) 
{
	echo "<tr><td>" . $row->created . "</td>";
        echo "<td>" . $row->updated . "</td>";
	if ($row->status == 'Error') { echo $cssTrick = '<td id="error">' . $row->status; } else { echo "<td> $row->status </td>"; };
	echo "<td>" . $row->interface . "</td>";
    echo '<td><a href="/trackingdb/transaction.php?env='.$env.'&trackingId=' . $row->id . '">' . $row->operation . "</a></td>";
    echo "<td><a href=account.php?env=". $env . "&account=" .urlencode($row->client_id) ." > " . $row->client_id . "</a></td>";

    try{
      $dom = new DOMDocument;
      $dom->preserveWhiteSpace = FALSE;
      $dom->loadXML($row->message);
      $dom->formatOutput = TRUE;
      echo "<td><pre>" . htmlentities($dom->saveXml()) . "</pre></td>";
    }catch(Exception $e){
      echo "<td>".$row->message."</td>";
    }

    if ($row->stack != null)
    {
        echo "<td><a href='javascript:child_open()'>Stack Trace</a> </td>";
    }
    else {
        echo "<td>No Trace available</td>";
    } 


	echo "</tr>";
}

?>
                </table>
        </content>
<?php
require_once("footer.php");
?>
