<?php
date_default_timezone_set('America/Chicago');
ini_set("display_errors", 0);
$environments = array('prod_us','prod_uk','staging_us','staging_uk');
if (isset($_GET['env']) && in_array($_GET['env'],$environments))
{
    $env = $_GET['env'];
}
else { $env = "prod_us";}
if (isset($_GET['correlationID']) && strpos($_GET['correlationID'], 'ID:' ) !== false )
{
    $correlationID = urldecode($_GET['correlationID']);
} else {
    $correlationID = 0;
}
if (isset($_GET['serverIp']))
{
    $serverIp= $_GET['serverIp'];
} else {
    $serverIp = 0;
}
if (isset($_GET['serverDataSearchFrom']))
{
    $serverDataSearchFrom = urldecode($_GET['serverDataSearchFrom']);
} else {
    $serverDataSearchFrom = strtotime ( '-3 day' , strtotime ( date("Y-m-d H:i:s") ));
}
if (isset($_GET['trackingId']) && strpos($_GET['trackingId'], 'ID:' ) !== false )
{
    $trackingId = urldecode($_GET['trackingId']);
}
if (isset($_GET['operation']))
    $operation = urldecode($_GET['operation']);

session_start();
if ($_SESSION['user'] != '') {
    $username = $_SESSION['user'];
    $loggedin = TRUE;
} elseif ($_SERVER['SCRIPT_NAME'] != '/login.php') {
    header('Location: login.php?error=1');
    exit();
}
if ($_GET['action'] == 'logout') {
    session_destroy();
    header('Location: /');
    exit();
}
session_write_close();

require_once("includes/config.php");
?>

    <html>
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
        <link rel="stylesheet" type="text/css" href="default.css" />
        <title> Demo Application for <?php echo $prettyName ?></title>
        <script type="text/javascript" language="javascript">
            function Refresh(env){
                location.href="index.php?env=" + env
            }
            var popupWindow=null;

            function child_open()
            {
                popupWindow =window.open('stacktrace.php?env=<?php echo $env ."&correlationID=" . $correlationID; ?>',"_blank","directories=no, status=no, menubar=no, scrollbars=yes, resizable=no,width=900, height=500,top=200,left=200");
            }
            function parent_disable() {
                if(popupWindow && !popupWindow.closed)
                    popupWindow.focus();
            }
        </script>
    </head>
    <body>
    <div id="header-container">
        <!-- Top Logo thinggy -->

        <header class="wrapper clearfix">
            <h1 id="title">Demo Application</h1>
        </header>
    </div>
<?php
if ($loggedin) {
    echo 'Logged in as: '.$username.' | <a href="/?action=logout">Logout</a><br />';;
}
require_once("subheader.php");
?>
