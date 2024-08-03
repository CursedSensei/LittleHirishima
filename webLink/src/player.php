<?php require 'session.php';?>

<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="./css/output.css" rel="stylesheet">
        <link href="./css/font-awesome.min.css" rel="stylesheet">
    </head>
    <body class="min-h-screen bg-gradient-to-b from-slate-900 to-zinc-950">
        <div class="h-screen w-11 bg-black bg-opacity-20 opacity-100 transition-all duration-100 hover:w-40 flex flex-col text-transparent hover:text-white text-xl pt-2">
            <div class="overflow-hidden text-nowrap px-2 flex items-center">
                <img class="size-7 border-sky-700 rounded-md" src="https://cdn.discordapp.com/app-icons/1000885935107473458/30764c598519d21c84710865ff638dad.png?size=128">
                <div class="ml-3 font-bold text-base text-justify">
                    <p>Little</p>
                    <p>Hirishima</p>
                </div>
            </div>
            <a href="#" class="mt-12 overflow-hidden text-nowrap px-3.5 pt-4 pb-4 hover:bg-slate-600">
                <i class="fa fa-headphones text-white" aria-hidden="true"></i> &nbsp;&nbsp;Player
            </a>
            <a href="#playlist" class="overflow-hidden text-nowrap px-3.5 pl-4 pt-4 pb-4 hover:bg-slate-600 border-t border-slate-600">
                <i class="fa fa-bookmark text-white" aria-hidden="true"></i> &nbsp;&nbsp;Playlists
            </a>
            <a href="logout.php" class="mt-auto overflow-hidden text-nowrap px-3.5 pt-4 pb-4 hover:bg-slate-600">
                <i class="fa fa-arrow-circle-left text-white" aria-hidden="true"></i> &nbsp;&nbsp;Sign Out
            </a>
        </div>
        <div></div>
    </body>
</html>