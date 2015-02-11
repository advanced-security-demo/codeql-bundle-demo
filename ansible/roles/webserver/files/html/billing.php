<?php
require_once("top.php");
?>
<a href="?env=<?php echo $_GET['env'] ?>&operations=GetBillingDay&num=10">See without Payments</a>
<div id="main-container">
	<div id="main" class="wrapper clearfix">
	<content>
		<table class="list" cellpadding="1">
<?php
if ( !isset($_GET['num']) ){
    $num_entries = 10;
}
else{

$num_entries = $_GET['num'];
}

if (!$link = mysql_connect($host, $user, $pass)) {
    echo 'Could not connect to mysql';
    exit;
}

if (!mysql_select_db('demo', $link)) {
    echo 'Could not select database';
    exit;
}



$query = "select * from tracking_error order by id desc limit " . $num_entries . ";";
$result = mysql_query($query, $link);
if (!$result)
{
        print("No Result: " . mysql_error());
}
print("</h6><h3>");
print("<table border='10'>");
print("<th>Tracking ID</th><th>Type</th><th>Message</th>");
while ($row = mysql_fetch_array($result))
{
        print("<tr>");
        print("<td>" . $row['tracking_id'] . "</td>");
        print("<td>" . $row['type'] . "</td>");
        print("<td>" . $row['message'] . "</td>");
        print("</tr>");
}
mysql_close($link);
?>



		</table>
	</content>
<?php
#require_once("left.php");
require_once("footer.php");
?>
