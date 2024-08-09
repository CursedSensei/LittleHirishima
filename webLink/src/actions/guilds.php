<?php
require_once 'session.php';

// if (isset($_SESSION['guild']) && time() - $_SESSION['client_time'] <= 20) {
if (isset($_SESSION['guild'])) {
    http_response_code(304);
    exit;
}

require_once '../../vendor/discordAPI.php';

$guilds = getGuilds();

$_SESSION['guilds'] = $guilds;

if ($guilds !== false) {
    for ($i = count($guilds) - 1; $i >= 0; $i--) {
        $guildIcon = $guilds[$i]->icon != "" ? "https://cdn.discordapp.com/icons/" . $guilds[$i]->id . "/" . $guilds[$i]->icon . ".png?size=128" : "assets/no-image.png";
    ?>
        <div class="w-72 h-80 py-8 px-14 flex-none snap-center hover:scale-110 transition-all duration-75 bg-white bg-opacity-20 hover:bg-opacity-25 rounded-xl border border-transparent hover:border-sky-800 active:border-sky-500 overflow-hidden cursor-pointer" name="<?php echo $guilds[$i]->id; ?>">
            <img class="size-32 mx-auto rounded-3xl <?php echo $guildIcon == "assets/no-image.png" ? "" : "shadow-2xl"; ?>" src="<?php echo $guildIcon; ?>">
            <p class="mx-auto mt-3 text-center text-lg font-semibold"><?php echo $guilds[$i]->name; ?></p>
        </div>
    <?php
    }
} else {
    http_response_code(401);
    exit;
}