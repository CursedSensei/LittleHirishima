<?php
require_once 'session.php';

if ($_SESSION['client_lock']) {
    http_response_code(102);
    exit;
}

if (isset($_SESSION['guild']) && $_GET['guild_id'] == $_SESSION['guild']->id && time() - $_SESSION['client_time'] <= 20) {
    $fName = "../../pipes/" . $_SESSION['client_id'];

    while (!($fp = fopen($fName, "x")) && time() - $_SESSION['client_time'] <= 20) {
        time_nanosleep(0, 10000);
    }

    if ($fp === false) {
        http_response_code(405);
        unlink($fName);
        exit;
    }

    fwrite($fp, 'info');
    fclose($fp);

    $_SESSION['client_time'] = time();
    $fName = "../../pipes/" . $_SESSION['client_id'] . ".out";

    while (!($fp = fopen($fName, "r")) && time() - $_SESSION['client_time'] <= 20) {
        time_nanosleep(0, 10000);
    }

    if ($fp === false) {
        http_response_code(405);
        exit;
    }

    $data = fread($fp, filesize($fName));
    fclose($fp);

    unlink($fName);

    echo $data;

} else {
    http_response_code(405);
}