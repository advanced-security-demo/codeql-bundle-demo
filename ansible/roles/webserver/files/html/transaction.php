<?php
require_once("top.php");
include("xmlpp.php");
?>

<div id="main-container">
        <div id="main" class="wrapper clearfix">
        <content>
<?php
try {
	$dbh = new PDO("mysql:host=$host;dbname=demo", $user, $pass);
    $findChildSTH = $dbh->prepare("select * from tracking where id = :trackingID");
    $findChildSTH->execute(array(':trackingID' => urlDecode($trackingId)));


}
catch(PDOException $e)
{
    echo $e->getMessage();
    echo "Exiting";
    exit;
}

if ( $findChildSTH->rowCount() == 0){
    echo "noting was found";
}


$findChildSTH->setFetchMode(PDO::FETCH_OBJ);  

$detailData = $findChildSTH;

echo "<ul>";
echo "<li>". urldecode($trackingId)." </li>";
echo "<li> $host </li>";
while($row = $findChildSTH->fetch()) 
{
    $inputxml = new DOMDocument();
    $inputxml->preserveWhiteSpace = FALSE;
    $inputxml->loadXML($row->in);
    $inputxml->formatOutput = TRUE;
    $outputxml = new DOMDocument();
    $outputxml->preserveWhiteSpace = TRUE;
    $outputxml->loadXML($row->out);
    $outputxml->formatOutput = TRUE;
    echo "<li> Created: " . $row->created . "</li>";
    echo "<li> Updated: " . $row->updated . "</li>";
	echo "<li> Interface: " . $row->interface . "</li>";
	echo "<li> Operation: " . $row->operation . "</li>";
    echo "<li> Interface: " . $row->interface . "</li>";
    echo "<li> Operation: " . $row->operation . "</li>";
    echo "<li> Input:<pre>" . htmlspecialchars($inputxml->saveXML()) . "</pre></li>";
    echo "<li> Output:<pre>" . htmlspecialchars($outputxml->saveXML()) . "</pre></li>";
    echo "<li> Account: <a href=account.php?env=". $env . "&account=" .urlencode($row->user) ." > " . $row->client_id . "</a></li>";
    echo "<li> Client ID: <a href=account.php?env=". $env . "&account=" .urlencode($row->client_id) ." > " . $row->client_id . "</a></li>";
    echo "<li> Correlation ID: <a href=detail.php?env=". $env . "&correlationID=" .urlencode($row->correlation_id) ." > " . $row->correlation_id . "</a></li>";
    echo "<li> Server: " . $row->server ."</li>";
    echo "<li> NameSpace: ". $row->namespace . "</li>";
    echo "<li> Note: " . $row->note . "</li>";
    if ($row->status == 'Error') { echo $cssTrick = '<li id="error">' . $row->status; } else { echo "<li> $row->status </li>"; };
}
?>
</ul>
        </content>
<?
require_once("footer.php");
?>
