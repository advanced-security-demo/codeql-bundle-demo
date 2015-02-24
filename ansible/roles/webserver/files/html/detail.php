<?php
require_once("top.php");
require_once("xmlpp.php");
?>

<div id="main-container">
        <div id="main" class="wrapper clearfix">
        <content>
                <table class="list">
<?php


if ( !isset($_GET['id']) ){
    $id = 10;
}
else{

$id = $_GET['id'];
}

if (!$link = mysql_connect($host, $user, $pass)) {
    echo 'Could not connect to mysql';
    exit;
}

if (!mysql_select_db('demo', $link)) {
    echo 'Could not select database';
    exit;
}


$query = "select * from tracking where id='" . $id . "' order by id;";
$result = mysql_query($query, $link);
if (!$result)
{
        print("No Result: " . mysql_error());
}
print("</h6><h3>");
print("<table border='10' width='800px'>");
print("<th>Tracking ID</th><th>Client ID</th><th>User</th><th>Status</th><th>Note</th>");
while ($row = mysql_fetch_array($result))
{
        print("<tr>");
        print("<td>" . $row['id'] . "</td>");
        print("<td>" . $row['client_id'] . "</td>");
        print("<td>" . $row['user'] . "</td>");
        print("<td>" . $row['status'] . "</td>");
        print("<td>" . htmlentities($row['note']) . "</td>");
        
        print("</tr>");
}
mysql_close($link);


?>
                </table>
        </content>
<?php
require_once("footer.php");
?>
