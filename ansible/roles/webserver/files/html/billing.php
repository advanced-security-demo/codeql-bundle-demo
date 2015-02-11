<?php
require_once("top.php");
?>
<a href="?env=<?php echo $_GET['env'] ?>&operations=GetBillingDay,CreatePayment,CreateRenewalPayment">See without Payments</a>
<div id="main-container">
	<div id="main" class="wrapper clearfix">
	<content>
		<table class="list" cellpadding="1">
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

if ($_GET['operations'] == '') {
  $getTrackingErrors = $dbh->query("select tracking.client_id, tracking_error.created, tracking_error.id, tracking_id, message, interface, operation from tracking.tracking_error join tracking on tracking_error.tracking_id = tracking.id where interface in ('Billing') and operation not in ('GetBillingDay') order by id desc limit 300");
} else {
  $operations = explode(',',$_GET['operations']);
  $getTrackingErrors = $dbh->query("select tracking.client_id, tracking_error.created, tracking_error.id, tracking_id, message, interface, operation from tracking.tracking_error join tracking on tracking_error.tracking_id = tracking.id where interface in ('Billing') and operation not in ('".implode("','",$operations)."') order by id desc limit 300");
}
$getTrackingErrors->setFetchMode(PDO::FETCH_OBJ);

echo "<tr class='listHeader'> <td><b>Creeated</b></td> <td><b>Interface</b></td> <td><b>Operation</b></td> <td><b>DDI</b></td> <td><b>Tracking ID</b></td> <td><b>Created</b></td> <td><b>Message</b></td> </tr>";

while($row = $getTrackingErrors->fetch()) {  
    echo "<tr style=\"border-top:1px dotted black;\"><td>" . $row->created . "</td>";  
    echo "<td>" . $row->interface . "</td>";
    echo "<td>" . $row->operation . "</td>";
    echo "<td>" . $row->client_id . "</td>";
    echo "<td><a href=detail.php?env=".$env. "&correlationID=" . urlencode($row->tracking_id) ." > " . $row->tracking_id . "</a></td>";   
    echo "<td>" .$row->created . "</td>";
    $dom = new DOMDocument;
    $dom->preserveWhiteSpace = FALSE;
    $dom->loadXML($row->message);
    $faultstring       = $dom->getElementsByTagName( "faultstring" )->item(0)->nodeValue;
    $dom->formatOutput = TRUE;
    echo "<td><b>Faultstring:</b> ".$faultstring."<br /><pre>".htmlentities($dom->saveXml()) . "\n</pre></td></tr>"; 
}  
?>
		</table>
	</content>
<?php
#require_once("left.php");
require_once("footer.php");
?>
