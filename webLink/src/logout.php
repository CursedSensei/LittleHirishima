<?php
session_start();

require_once '../vendor/discordAPI.php';
revokeUser();

session_destroy();

header("Location: index.php");