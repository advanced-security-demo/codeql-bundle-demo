<?php
require_once("top.php");
?>
    <div id="main-container">
    <div id="main" class="wrapper clearfix">
    <content>
        <table class="list" cellpadding="5px" >
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

            $getTrackingErrors = $dbh->query("select tracking_error.created, tracking_error.id, tracking_id, message, interface, operation from tracking.tracking_error join tracking on tracking_error.tracking_id = tracking.id where message not like '%Unable to issue purge requests%' order by id desc limit 150");

            $getTrackingErrors->setFetchMode(PDO::FETCH_OBJ);

            echo "<tr class='listHeader'> <td><b>Created</b></td><td><b>Interface</b></td><td><b>Operation</b></td><td><b>Tracking ID</b></td> <td><b>Message</b></td> </tr>";

            while($row = $getTrackingErrors->fetch()) {
                echo "<tr style=\"border-top:1px dotted black;\"><td>" . $row->created. "</td>";
                echo "<td>" . $row->interface . "</td>";
                echo "<td>" . $row->operation . "</td>";
                echo "<td><a href=detail.php?env=".$env. "&correlationID=" . urlencode($row->tracking_id) ." > " . $row->tracking_id . "</a></td>";
                $dom = new DOMDocument;
                $dom->preserveWhiteSpace = FALSE;
                $dom->loadXML($row->message);
                $faultstring                = $dom->getElementsByTagName( "faultstring" )->item(0)->nodeValue;
                $dom->formatOutput  = TRUE;
                $output             = $dom->saveXml();
                echo "<td>Faultstring: ".substr($faultstring,0,150)."<br /><pre>" .htmlentities($output). "\n</pre></td></tr>";
            }
            ?>
        </table>
    </content>
<?php
#require_once("left.php");
require_once("footer.php");
?>