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
        <link rel="icon" href="assets/bot.png" type="image/x-icon">
        <meta name="guild_id" content="<?php echo isset($_SESSION['guild']) ? $_SESSION['guild']->id : "" ?>">
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
                <button class="ml-auto text-xl bg-white bg-opacity-20 px-6 py-3 rounded-full hover:bg-opacity-30" id="changeGuild"><i class="fa fa-arrow-circle-o-left" aria-hidden="true"></i> &nbsp;Switch Server</button>
            </div>
            <div class="flex h-5/6 w-full gap-2 flex-row-reverse pb-8">
                <div class="float-end bg-white w-1/2 h-full bg-opacity-30 backdrop-blur-xl rounded-lg text-lg overflow-hidden flex flex-col">
                    <div class="shrink-0 w-full h-12 flex" id="pageButtons">
                        <button name="queue" class="w-1/3 border-b border-gray-700 hover:font-semibold hover:border-gray-500 bg-black bg-opacity-30 hover:bg-opacity-20 active"><i class="fa fa-clone" aria-hidden="true"></i> Queue</button>
                        <button name="search" class="w-1/3 border-b border-gray-700 hover:font-semibold hover:border-gray-500 bg-black hover:bg-opacity-20 bg-opacity-30" id="searchBut"><i class="fa fa-search" aria-hidden="true"></i> Search</button>
                        <button name="recent" class="w-1/3 border-b border-gray-700 hover:font-semibold hover:border-gray-500 bg-black hover:bg-opacity-20 bg-opacity-30"><i class="fa fa-history" aria-hidden="true"></i> Recent</button>
                    </div>
                    <div class="grow relative flex min-h-0" style="width: 300%;">
                        <div class="h-full w-1/3" id="queuePage">
                            <div class="w-full flex gap-5 px-6 py-2 bg-black bg-opacity-0 hover:bg-opacity-15">
                                <div class="shrink-0 flex flex-col justify-center gap-3 cursor-pointer">
                                    <p class="rounded-lg bg-black bg-opacity-20 p-1"></p>
                                    <p class="rounded-lg bg-black bg-opacity-20 p-1"></p>
                                </div>
                                <img class="h-20 shrink-0 aspect-video" src="https://i.ytimg.com/vi/vQjub8dkobc/hq720.jpg?sqp=-oaymwEXCNAFEJQDSFryq4qpAwkIARUAAIhCGAE=&amp;rs=AOn4CLDWACbMxarWRnx_4JalGSsUi5tgUg">
                                <div class="grow w-1/5 overflow-hidden">
                                    <a href="https://www.youtube.com/watch?v=vQjub8dkobc" class="font-bold text-xl text-nowrap hover:underline w-min" target="_blank" style="margin-left: 0px;">
                                        【#ホロ7DTD】49日間サバイバル⁉3日目！【星街すいせい / ホロライブ】</a>
                                    <div class="w-full flex py-3">
                                        <p class="grow text-base">Suisei Channel</p>
                                        <p class="grow-0 text-sm">2:11:59</p>
                                    </div>
                                </div>
                                <div class="shrink-0 flex flex-col justify-center">
                                    <button class="rounded-lg bg-black bg-opacity-20 px-2.5 py-0.5">
                                        <i class="fa fa-play" aria-hidden="true"></i>
                                    </button>
                                </div>
                            </div>
                            <!-- <div class="w-full h-full flex items-center justify-center text-2xl font-bold"><button class="border-2 border-white border-opacity-15 rounded-xl px-2" id="queueHint"><i class="fa fa-plus" aria-hidden="true"></i></button> &nbsp;Add To Queue</div> -->
                        </div>
                        <div class="h-full w-1/3 overflow-y-auto flex flex-col" id="searchPage">
                            <div class="w-1/3 px-10 pt-3 pb-2 text-xl absolute">
                                <div class="w-full flex bg-white rounded overflow-hidden focus-within:border-black border-2">
                                    <input class="grow px-2 py-1 focus:outline-none text-black" type="text" placeholder="Search" id="searchQuery">
                                    <button class="px-3 text-gray-400" id="searchButton"><i class="fa fa-search" aria-hidden="true"></i></button>
                                </div>
                            </div>
                            <div class="w-1/3 px-10 absolute top-14 z-30">
                                <div class="rounded-sm bg-white bg-opacity-85 backdrop-blur-xl text-black text-opacity-80 font-bold shadow-xl" id="searchHint">
                                    <div class="w-full py-1 px-2 align-middle hover:bg-black hover:bg-opacity-15"></div>
                                </div>
                            </div>
                            <div class="grow w-full pt-14" id="searchTray">
                                <div class="w-full h-full flex justify-center items-center">
                                    <img class="size-14" src="assets/error.png">
                                    <p class="font-bold text-xl">  No Results</p>
                                </div>
                            </div>
                        </div>
                        <div class="h-full w-1/3" id="recentPage"></div>
                    </div>
                </div>
                <div class="w-1/2 h-full flex flex-col gap-2">
                    <div class="bg-black/35 w-full backdrop-blur-xl rounded-lg flex flex-col items-center justify-end gap-1 overflow-hidden" style="aspect-ratio: 16/9;" id="playerPage">
                        <img class="w-full aspect-video absolute top-0 -z-10 border-transparent">
                        <div class="w-full bg-gradient-to-t from-gray-950 pb-2 pt-16 px-2">
                            <div class="w-full flex flex-wrap">
                                <input type="range" class="w-full appearance-none cursor-pointer rounded-lg h-2.5 opacity-70 hover:opacity-100 transition-opacity bg-white" min="0" max="0" id="musicLength">
                                <p class="grow" id="startLength">0:00</p>
                                <p class="grow text-right" id="endLength">0:00</p>
                            </div>
                            <div class="flex justify-center">
                                <button class="px-3 text-2xl scale-75" id="shuffleBut"><i class="fa fa-random" aria-hidden="true"></i></button>
                                <button class="px-3 text-2xl scale-x-125" id="prevBut"><i class="fa fa-step-backward" aria-hidden="true"></i></button>
                                <button class="px-3 text-5xl" id="playBut"><i class="fa fa-play-circle" aria-hidden="true"></i></button>
                                <button class="px-3 text-5xl hidden"><i class="fa fa-pause-circle" aria-hidden="true"></i></button>
                                <button class="px-3 text-2xl scale-x-125" id="nextBut"><i class="fa fa-step-forward" aria-hidden="true"></i></button>
                                <button class="px-3 text-2xl scale-75" id="loopBut"><i class="fa fa-refresh" aria-hidden="true"></i></button>
                            </div>
                        </div>
                    </div>
                    <div class="bg-white w-full grow bg-opacity-30 backdrop-blur-xl rounded-lg overflow-hidden flex" id="nextPage">
                        <div class="h-full w-56 bg-black bg-opacity-20"></div>
                    </div>
                </div>
            </div>
        </div>

        <?php // Sidebar ?>
        <div class="h-screen w-11 bg-black bg-opacity-60 backdrop-blur-xl transition-all duration-100 hover:w-40 flex flex-col text-transparent hover:text-white text-xl pt-2 absolute top-0 select-none">
            <div class="overflow-hidden text-nowrap px-2 flex items-center">
                <img class="size-7 border-sky-700 rounded-md" src="assets/bot.png">
                <div class="ml-3 font-bold text-base text-justify">
                    <p>Little</p>
                    <p>Hirishima</p>
                </div>
            </div>
            <a href="#" class="mt-12 overflow-hidden text-nowrap px-3.5 pt-4 pb-4 hover:bg-slate-600 hover:bg-opacity-30 active:bg-opacity-60">
                <i class="fa fa-headphones text-white" aria-hidden="true"></i> &nbsp;&nbsp;Player
            </a>
            <a href="#playlist" class="overflow-hidden text-nowrap px-3.5 pl-4 pt-4 pb-4 hover:bg-slate-600 hover:bg-opacity-30 active:bg-opacity-60">
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