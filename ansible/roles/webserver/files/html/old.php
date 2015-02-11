<html>
<head>
<title>Query Results</title>
</head>
<body>
<h6>
<?php
require_once('./config.php');
$num_entries = $_POST['num'];
if (!$con)
{
die('Could not connect to DB <br>' . mysql_error());
}
if ($con)
{
print("Connected");

}
$query = "select * from tracking.tracking_error order by id desc limit " . $num_entries . ";";
$result = mysql_query($query);
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
mysql_close($con);
?>

</body>
</html>
