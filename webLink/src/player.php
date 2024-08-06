<?php require 'session.php';?>

<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="./css/output.css" rel="stylesheet">
        <link href="./css/font-awesome.min.css" rel="stylesheet">
        <title>Little Hirishima Dashboard</title>
        <link rel="preconnect" href="https://cdn.discordapp.com" />
        <link rel="icon" href="https://cdn.discordapp.com/app-icons/1000885935107473458/30764c598519d21c84710865ff638dad.png?size=128" type="image/x-icon">
    </head>
    <body class="min-h-screen bg-gradient-to-b from-slate-900 to-zinc-950 overflow-hidden">
        <?php // Loading ?>
        <div class="h-screen w-89 ml-11 p-8 flex flex-wrap overflow-hidden" id="loading">
            <div class="flex gap-2 h-1/3 mt-16 w-full">
                <div class="w-1/2 h-full bg-white bg-opacity-20 rounded-md pt-12 pb-16 px-16">
                    <div class="flex-1 space-y-6 py-1 animate-pulse mb-12">
                        <div class="h-2 bg-gray-900 rounded"></div>
                        <div class="space-y-3">
                            <div class="grid grid-cols-3 gap-4">
                                <div class="h-2 bg-gray-900 rounded col-span-2"></div>
                                <div class="h-2 bg-gray-900 rounded col-span-1"></div>
                            </div>
                            <div class="h-2 bg-gray-900 rounded"></div>
                        </div>
                    </div>
                    <div class="flex-1 space-y-6 py-1 animate-pulse mb-12">
                        <div class="h-2 bg-gray-900 rounded"></div>
                        <div class="space-y-3">
                            <div class="grid grid-cols-3 gap-4">
                                <div class="h-2 bg-gray-900 rounded col-span-2"></div>
                                <div class="h-2 bg-gray-900 rounded col-span-1"></div>
                            </div>
                            <div class="h-2 bg-gray-900 rounded"></div>
                        </div>
                    </div>
                </div>
                <div class="w-1/2 h-full bg-white bg-opacity-20 rounded-md pt-12 pb-16 px-16">
                    <div class="flex-1 space-y-6 py-1 animate-pulse mb-12">
                        <div class="h-2 bg-gray-900 rounded"></div>
                        <div class="space-y-3">
                            <div class="grid grid-cols-3 gap-4">
                                <div class="h-2 bg-gray-900 rounded col-span-2"></div>
                                <div class="h-2 bg-gray-900 rounded col-span-1"></div>
                            </div>
                            <div class="h-2 bg-gray-900 rounded"></div>
                        </div>
                    </div>
                    <div class="flex-1 space-y-6 py-1 animate-pulse mb-12">
                        <div class="h-2 bg-gray-900 rounded"></div>
                        <div class="space-y-3">
                            <div class="grid grid-cols-3 gap-4">
                                <div class="h-2 bg-gray-900 rounded col-span-2"></div>
                                <div class="h-2 bg-gray-900 rounded col-span-1"></div>
                            </div>
                            <div class="h-2 bg-gray-900 rounded"></div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="w-full h-1/2 bg-white bg-opacity-20 rounded-md pt-12 pb-16 px-16">
                <div class="flex-1 space-y-6 py-1 animate-pulse mb-12">
                    <div class="h-2 bg-gray-900 rounded"></div>
                    <div class="space-y-3">
                        <div class="grid grid-cols-3 gap-4">
                            <div class="h-2 bg-gray-900 rounded col-span-2"></div>
                            <div class="h-2 bg-gray-900 rounded col-span-1"></div>
                        </div>
                        <div class="h-2 bg-gray-900 rounded"></div>
                    </div>
                </div>
                <div class="flex-1 space-y-6 py-1 animate-pulse mb-12">
                    <div class="h-2 bg-gray-900 rounded"></div>
                    <div class="space-y-3">
                        <div class="grid grid-cols-3 gap-4">
                            <div class="h-2 bg-gray-900 rounded col-span-2"></div>
                            <div class="h-2 bg-gray-900 rounded col-span-1"></div>
                        </div>
                        <div class="h-2 bg-gray-900 rounded"></div>
                    </div>
                </div>
                <div class="flex-1 space-y-6 py-1 animate-pulse mb-12">
                    <div class="h-2 bg-gray-900 rounded"></div>
                    <div class="space-y-3">
                        <div class="grid grid-cols-3 gap-4">
                            <div class="h-2 bg-gray-900 rounded col-span-2"></div>
                            <div class="h-2 bg-gray-900 rounded col-span-1"></div>
                        </div>
                        <div class="h-2 bg-gray-900 rounded"></div>
                    </div>
                </div>
            </div>
        </div>

        <?php // Server Selection ?>
        <div class="h-screen w-89 ml-11 flex scroll-smooth overflow-x overflow-y-hidden items-center snap-x gap-7 px-16 text-white select-none" id="selection"></div>

        <?php // Server Selection: No Server Error ?>
        <div class="h-screen w-89 ml-11 p-8 flex flex-col items-center justify-center text-white" id="emptyServer">
            <h1 class="text-2xl font-bold scale-150"><i class="fa fa-exclamation-circle" aria-hidden="true"></i> &nbsp;No Servers Available</h1>
            <button class="mt-16 bg-white bg-opacity-10 px-4 py-2 rounded-md hover:bg-opacity-15" id="selection_refresh"><i class="fa fa-refresh" aria-hidden="true"></i> &nbsp;Refresh</button>
        </div>

        <?php // Player Background ?>
        <div class="h-screen absolute -z-50 bg-repeat blur-lg opacity-45" style="width: 150vw; background-image: url(<?php echo isset($_SESSION['guild']) ? ($_SESSION['guild']->icon != "" ? "https://cdn.discordapp.com/icons/" . $_SESSION['guild']->id . "/" . $_SESSION['guild']->icon . ".png?size=128" : "") : ""; ?>);" id="playerBackground"></div>

        <?php // Player ?>
        <div class="h-screen w-89 ml-11 px-8 text-white" id="player">
            <div class="w-full h-1/6 flex items-center overflow-hidden">
                <img class="size-28 rounded-2xl mr-7" id="serverIcon" src="<?php echo isset($_SESSION['guild']) ? ($_SESSION['guild']->icon != "" ? "https://cdn.discordapp.com/icons/" . $_SESSION['guild']->id . "/" . $_SESSION['guild']->icon . ".png?size=128" : "assets/no-image.png") : ""; ?>">
                <h1 class="w-4/6 overflow-hidden text-3xl font-bold font-serif text-ellipsis" id="serverName"><?php echo isset($_SESSION['guild']) ? $_SESSION['guild']->name : ""; ?></h1>
                <button class="ml-auto text-xl bg-white bg-opacity-20 px-6 py-3 rounded-full" id="changeGuild"><i class="fa fa-arrow-circle-o-left" aria-hidden="true"></i> &nbsp;Switch Server</button>
            </div>
            <div class="flex h-5/6 w-full gap-2 flex-row-reverse pb-8">
                <div class="float-end bg-white w-1/2 h-full bg-opacity-30 backdrop-blur-xl rounded-lg text-xl overflow-hidden">
                    <div class="w-full h-12 flex">
                        <button class="w-1/3 border-b border-gray-700 hover:font-semibold hover:border-gray-500 bg-black bg-opacity-30 hover:bg-opacity-20 active"><i class="fa fa-clone" aria-hidden="true"></i> Queue</button>
                        <button class="w-1/3 border-b border-gray-700 hover:font-semibold hover:border-gray-500 bg-black hover:bg-opacity-20 bg-opacity-30"><i class="fa fa-search" aria-hidden="true"></i> Search</button>
                        <button class="w-1/3 border-b border-gray-700 hover:font-semibold hover:border-gray-500 bg-black hover:bg-opacity-20 bg-opacity-30"><i class="fa fa-inbox" aria-hidden="true"></i> Recent</button>
                    </div>
                </div>
                <div class="w-1/2 h-full flex flex-col gap-2">
                    <div class="bg-white w-full h-4/6 bg-opacity-30 backdrop-blur-xl rounded-lg"></div>
                    <div class="bg-white w-full h-2/6 bg-opacity-30 backdrop-blur-xl rounded-lg"></div>
                </div>
            </div>
        </div>

        <?php // Sidebar ?>
        <div class="h-screen w-11 bg-black bg-opacity-60 backdrop-blur-xl transition-all duration-100 hover:w-40 flex flex-col text-transparent hover:text-white text-xl pt-2 absolute top-0 select-none">
            <div class="overflow-hidden text-nowrap px-2 flex items-center">
                <img class="size-7 border-sky-700 rounded-md" src="https://cdn.discordapp.com/app-icons/1000885935107473458/30764c598519d21c84710865ff638dad.png?size=128">
                <div class="ml-3 font-bold text-base text-justify">
                    <p>Little</p>
                    <p>Hirishima</p>
                </div>
            </div>
            <a href="#" class="mt-12 overflow-hidden text-nowrap px-3.5 pt-4 pb-4 hover:bg-slate-600 hover:bg-opacity-30 active:bg-opacity-60">
                <i class="fa fa-headphones text-white" aria-hidden="true"></i> &nbsp;&nbsp;Player
            </a>
            <a href="#playlist" class="overflow-hidden text-nowrap px-3.5 pl-4 pt-4 pb-4 hover:bg-slate-600 border-t border-slate-600 hover:bg-opacity-30 border-opacity-30 active:bg-opacity-60">
                <i class="fa fa-bookmark text-white" aria-hidden="true"></i> &nbsp;&nbsp;Playlists
            </a>
            <a href="logout.php" class="mt-auto overflow-hidden text-nowrap px-3.5 pt-4 pb-4 hover:bg-slate-600 hover:bg-opacity-30 active:bg-opacity-60">
                <i class="fa fa-sign-out text-white" aria-hidden="true"></i> &nbsp;&nbsp;Sign Out
            </a>
        </div>
    </body>

    <script src="js/jquery-3.7.1.min.js"></script>
    <script src="js/player.js"></script>
</html>