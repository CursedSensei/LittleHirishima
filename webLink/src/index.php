<?php
session_start();
if (isset($_GET['code'])) {
    # do authorization from OAuth2
}

if (isset($_SESSION['user_id'])) {
    header("Location: guild.php");
    exit;
}
?>

<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="./css/output.css" rel="stylesheet">
    </head>
    <body class="min-h-screen bg-gradient-to-b from-slate-900 to-zinc-950">
        <header class="flex p-4">
            <img class="size-12 border-sky-700 rounded-xl" src="https://cdn.discordapp.com/app-icons/1000885935107473458/30764c598519d21c84710865ff638dad.png?size=128">
            <h2 class="float-start ml-3 font-semibold text-white text-4xl">Little Hirishima</h2>
        </header>
        <div class="bg-white w-1/3 mx-auto bg-opacity-20 mt-52 rounded-md flex text-white">
            <div class="w-7/12">
                <div class="flex pl-2 pt-2">
                    <img class="size-8 border-sky-700 rounded-xl" src="https://cdn.discordapp.com/app-icons/1000885935107473458/30764c598519d21c84710865ff638dad.png?size=128">
                    <h2 class="float-start ml-3 font-semibold text-xl">Little Hirishima</h2>
                </div>
                <p class="p-2 text-justify">Yap yap yapYap yap yapYap yap yapYap yap yapYap yap yapYap yap yapYap yap yapYap yap yapYap yap yapYap yap yapYap yap yapYap yap yapYap yap yapYap yap yapYap yap yapYap yap yapYap yap yapYap yap yapYap yap yapYap yap yapYap yap yapYap yap yapYap yap yapYap yap yapYap yap yapYap yap yap</p>
            </div>
            <div class="w-5/12 flex float-end border-l-2 border-black">
                <a class="m-auto shadow-md px-4 py-2 rounded-3xl border border-gray-800 bg-blue-800 hover:bg-blue-600 transition-colors duration-100" href="https://discord.com/oauth2/authorize?client_id=1000885935107473458&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%2Fbot%2Findex.php&scope=identify+guilds">Login</a>
            </div>
        </div>
    </body>
    
    <script src="js/jquery-3.7.1.min.js"></script>
</html>