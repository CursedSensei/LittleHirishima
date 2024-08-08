<?php
require_once 'session.php';

if (isset($_SESSION['guild']) && time() - $_SESSION['client_time'] <= 20) {
    echo json_encode([$_SESSION['guild']->name, $_SESSION['guild']->icon != "" ? "https://cdn.discordapp.com/icons/" . $_SESSION['guild']->id . "/" . $_SESSION['guild']->icon . ".png?size=128" : "assets/no-image.png", $_SESSION['guild']->id]);
    exit;
}


if (isset($_SESSION['guilds']) && isset($_POST['guild_id'])) {
    for ($i = count($_SESSION['guilds']) - 1; $i >= 0; $i--) {
        if ($_SESSION['guilds'][$i]->id == $_POST['guild_id']) {

            $id = 1;
            while (!($fp = fopen("../../requests/$id.req", "x"))) $id++;

            fwrite($fp, $_POST['guild_id']);
            fclose($fp);

            time_nanosleep(0, 10);
            $time = time();
            while (time() - $time <= 10) {
                if (file_exists("../../requests/$id.con")) {
                    $_SESSION['guild'] = $_SESSION['guilds'][$i];
                    $_SESSION['client_id'] = file_get_contents("../../requests/$id.con");
                    $_SESSION['client_time'] = time();
                    $_SESSION['client_lock'] = false;
                    echo json_encode([$_SESSION['guilds'][$i]->name, $_SESSION['guilds'][$i]->icon != "" ? "https://cdn.discordapp.com/icons/" . $_SESSION['guilds'][$i]->id . "/" . $_SESSION['guilds'][$i]->icon . ".png?size=128" : "assets/no-image.png", $_SESSION['guilds'][$i]->id]);
                    unlink("../../requests/$id.req");
                    exit;
                }
                time_nanosleep(0, 10000);
            }

            unlink("../../requests/$id.req");
        }
    }
}

http_response_code(400);
exit;