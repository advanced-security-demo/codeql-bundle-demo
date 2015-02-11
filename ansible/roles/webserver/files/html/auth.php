<?php
if ($_POST['user'] != '') {
    if ("demo" == $_POST['user']) {
        $ldapbind = ("demo" == $_POST['pass']);
    }
    if ($ldapbind) {
        session_start();
        $_SESSION['user'] = "demo";
        session_write_close();
        header('Location: /');
    } else {
        header('Location: /?error=1');
    }
} else {
    header('Location: /');
}
?>