<?php
require_once 'session.php';

if ($_GET['guild_id'] == $_SESSION['guild']->id) {
    if (!$_SESSION['client_lock'] && time() - $_SESSION['client_time'] <= 17) {
        $_SESSION['client_lock'] = true;
        $fp = fopen("../../pipes/" . $_SESSION['client_id'], "w");
        fwrite($fp, "close");
        fclose($fp);
    }
    unset($_SESSION['guild']);
}