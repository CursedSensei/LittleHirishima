<?php
require_once 'session.php';

if (isset($_SESSION['guild'])) {
    echo json_encode($_SESSION['guild']);
    exit;
}


if (isset($_SESSION['guilds']) && isset($_POST['guild_id'])) {
    for ($i = count($_SESSION['guilds']) - 1; $i >= 0; $i--) {
        if ($_SESSION['guilds'][$i]->id == $_POST['guild_id']) {
            $_SESSION['guild'] = $_SESSION['guilds'][$i];
            echo json_encode([$_SESSION['guilds'][$i]->name, $_SESSION['guilds'][$i]->icon != "" ? "https://cdn.discordapp.com/icons/" . $_SESSION['guilds'][$i]->id . "/" . $_SESSION['guilds'][$i]->icon . ".png?size=128" : "assets/no-image.png"]);
            exit;
        }
    }
}

http_response_code(400);
exit;