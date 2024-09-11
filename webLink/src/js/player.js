const loadingDiv = $('#loading');
const selectionDiv = $('#selection');
const selectionDivError = $('#emptyServer');
const playerDiv = $('#player');
const playerName = $('#serverName');
const playerIcon = $('#serverIcon');
const playerBg = $('#playerBackground');
const queueEmpty = $('#queueHint');

var guildId = $("meta[name='guild_id']").attr("content");

selectionDiv.hide();
selectionDivError.hide();

// queueEmpty.hide();
playerDiv.hide();
playerBg.fadeOut(0);

var playerBgToRight = true;
var playerBgAnimate = false;

async function animatePlayerBg() {
    if (!playerBgAnimate) return;
    await new Promise(resolve => setTimeout(resolve, 400));
    playerBg.animate({
        left: playerBgToRight ? "-50vw" : "0vw"
    }, 24000, animatePlayerBg);
    playerBgToRight = !playerBgToRight;
}

const queuePageDom = $("#queuePage");
const searchPageDom = $("#searchPage");
const recentPageDom = $("#recentPage");
const slidePageDom = queuePageDom.parent();

function slidePage(left) {
    slidePageDom.stop(true, false);
    slidePageDom.animate({
        left: left
    }, 300);
}

$("#pageButtons > button").on("click", function () {
    const butDom = $(this);
    butDom.parent().children().removeClass("active");
    butDom.addClass("active");

    switch (butDom.attr("name")) {
        case "queue":
            slidePage("0%")
            break;
        case "search":
            slidePage("-100%")
            break;
        case "recent":
            slidePage("-200%")
            break;
    }
});

function radioText(jDom, reversed = false) {
    if (!reversed) {
        var offset = jDom.width() - jDom.parent().width();
        if (offset <= 0) return;
    } else {
        var offset = 0;
    }

    jDom.animate({
        "margin-left": (offset * -1) + "px"
    },
    {
        duration: 6000,
        complete: function () {
            radioText(jDom, !reversed);
        },
        fail: function () {
            jDom.css("margin-left", "0px");
        }
    });
}

function radioTextStop(jDom) {
    jDom.stop(true, false);
}

$("#queuePage > div > button").on("mousedown", queueMove);

var queueShadow = $('<div class="w-full bg-black bg-opacity-15 animate-pulse"></div>');
var queueSelected = null;
var mouseY = 0;
var queueY = -1;
var mouseOff = 0;

function queueMove(e) {
    queueSelected = $(this).parent();
    const pos = queueSelected.position();

    queueY = pos.top;
    mouseOff = mouseY;

    queueShadow.outerHeight(queueSelected.outerHeight());
    queueSelected.after(queueShadow);

    queueSelected.css("width", queueSelected.outerWidth() + "px");
    queueSelected.css("position", "absolute");
    queueSelected.css("z-index", "10");

    queueSelected.off("mousedown");
}

function queueSwap(e) {
    if (queueY != -1) {
        if (queueShadow.index() !== queueSelected.index() - 1 && queueShadow.index() !== queueSelected.index() + 1) {
            // swap call
        }
        queueShadow.remove();
        queueSelected.css("position", "");
        queueSelected.css("top", "");
        queueSelected.css("width", "");

        queueY = -1;

        queueSelected.find("button").first().on("mousedown", queueMove);
    }
}

$(document).on("mouseup", queueSwap);

window.addEventListener("focusout", queueSwap);

$(document).on("mousemove", function (e) {
    mouseY = e.pageY;

    if (queueY != -1) {
        queueSelected.css("top", Math.max(queueY + mouseY - mouseOff, 0) + "px");
    }
});


queueEmpty.on("click", function () {$("#searchBut").trigger("click");});

const searchQuery = $("#searchQuery");
const searchHint = $("#searchHint");
const searchButton = $("#searchButton");
const searchTray = $("#searchTray");

var hintController = new AbortController();
var resultController = new AbortController();
var continueController = new AbortController();

var searchTopPosition = 0;
var continueToken = "";
var continueLock = false;
var hintLookup = -1;

searchHint.hide();

function getHint(query) {
    hintController.abort();

    hintController = new AbortController();
    fetch(
        "actions/hint.php?&q=" + encodeURIComponent(query),
        {
            method: "get",
            signal: hintController.signal,
        }
    ).then(function (res) {
        if (res.status == 200) {
            res.text().then((data) => {
                data = JSON.parse(data);

                searchHint.empty();
                hintLookup = -1;
                for(let i = 0; i < data.length; i++) {
                    let hintDom = $('<div class="w-full py-1 px-2 align-middle hover:bg-black hover:bg-opacity-15"></div>');
                    hintDom.text(data[i]);
                    hintDom.on("mousedown", function () {
                        searchQuery.val(data[i]);
                        searchButton.click();
                    });
                    hintDom.appendTo(searchHint);
                }
            });
        }
    });
}

searchQuery.on("focusin", function () {
    searchHint.empty();
    searchHint.show();

    if (searchQuery.val() != "") {
        getHint(searchQuery.val());
    }
});

searchQuery.on("focusout", function () {
    searchHint.hide();
});

function searchEmpty() {
    searchTray.append($(`<div class="w-full h-full flex justify-center items-center">
        <img class="size-14" src="assets/error.png">
        <p class="font-bold text-xl">  No Results</p>
    </div>`));
}

function appendResult(data) {
    for (let i = 0; i < data.length - 1; i++) {
        let mainDiv = $('<div class="w-full flex gap-6 px-6 py-2 bg-black bg-opacity-0 hover:bg-opacity-15"></div>');
        mainDiv.append($('<img class="h-20 shrink-0 aspect-video" src="' + data[i]['thumb'] + '">'));

        let detailSection = $('<div class="grow w-1/5 overflow-hidden"></div>');
        let detailChild = $('<a href="https://www.youtube.com/watch?v=' + data[i]['key'] + '" class="font-bold text-xl text-nowrap hover:underline w-min" target="_blank"></a>');
        detailChild.text(data[i]['name']);
        mainDiv.hover(function (e) {radioText($(this).find("a").first())}, function (e) {radioTextStop($(this).find("a").first())});
        detailSection.append(detailChild);

        let childSection = $('<div class="w-full flex py-3"></div>');
        detailChild = $('<p class="grow text-base"></p>');
        detailChild.text(data[i]['channel']);
        childSection.append(detailChild);

        detailChild = $('<p class="grow-0 text-sm"></p>');
        detailChild.text(data[i]['rawlength']);
        childSection.append(detailChild);

        detailSection.append(childSection);
        mainDiv.append(detailSection);

        detailSection = $('<div class="shrink-0 flex flex-col gap-4"></div>');
        let playButton = $('<button class="grow rounded-lg bg-black bg-opacity-20 px-2"><i class="fa fa-play" aria-hidden="true"></i></button>');
        let queueButton = $('<button class="grow rounded-lg bg-black bg-opacity-20 px-2"><i class="fa fa-clone" aria-hidden="true"></i></button>');

        detailSection.append(playButton);
        detailSection.append(queueButton);

        mainDiv.on("dblclick", function (e) {
            // play
        });

        mainDiv.append(detailSection);
        searchTray.append(mainDiv);
    }
}

function searchResult() {
    searchHint.hide();
    resultController.abort();
    continueController.abort();
    continueToken = "";
    searchTray.empty();
    searchQuery.blur();
    searchTopPosition = 0;

    if (searchQuery.val() != "") {
        resultController = new AbortController();
        fetch("actions/search.php?&q=" + encodeURIComponent(searchQuery.val()), {
            method: "get",
            signal: resultController.signal,
        }).then(function (res) {
            if (res.status == 200) {
                res.json().then(function (data) {
                    appendResult(data);
                    continueToken = data[data.length - 1];
                });
            } else {
                searchEmpty();
            }
        });
    } else {
        searchEmpty();
    }
}

function searchContinue() {
    if (searchPageDom.scrollTop() < searchTopPosition){
        return;
    }

    searchTopPosition = searchPageDom.scrollTop() <= 0 ? 0 : searchPageDom.scrollTop();
    if (searchPageDom.scrollTop() + searchPageDom.height() + 200 < searchPageDom.prop('scrollHeight')){
        console.log(searchPageDom.scrollTop(), searchPageDom.height(), searchPageDom.prop('scrollHeight'));
        return;
    }

    if (continueToken && !continueLock) {
        continueLock = true;
        fetch("actions/search.php?&c=" + encodeURIComponent(continueToken), {
            method: "get",
            signal: resultController.signal,
        }).then(function (res) {
            if (res.status == 200) {
                res.json().then(function (data) {
                    appendResult(data);
                    continueToken = data[data.length - 1];
                    continueLock = false;
                });
            }
            continueLock = false;
        }).catch(function (e) {
            continueLock = false;
        });
    }
}

searchPageDom.on("wheel", searchContinue);
searchPageDom.on("scroll", searchContinue);
searchPageDom.on("resize", function (e) {
    if (searchTopPosition == 0) {
        return;
    }

    searchTopPosition = searchPageDom.scrollTop() <= 0 ? 0 : searchPageDom.scrollTop();
});

searchQuery.keydown(function (e) {
    if (e.key === "Tab") {
        if (hintLookup != -1) {
            searchQuery.val(searchHint.children().eq(hintLookup).text());
            getHint(searchQuery.val());
            e.preventDefault();
        }
    }
});

searchQuery.keyup(function (e) {
    if (e.key === "Enter") {
        if (hintLookup != -1) {
            searchHint.children().eq(hintLookup).trigger("mousedown");
        } else {
            searchResult();
        }
    } else if (e.key === "ArrowDown") {
        let hintDom = searchHint.children().eq(hintLookup + 1);
        if (hintDom != -1) {
            hintLookup++;
            searchHint.children().removeClass("hint-active")
            hintDom.addClass("hint-active");
        }
    } else if (e.key === "ArrowUp") {
        if (hintLookup >= 0) {
            searchHint.children().removeClass("hint-active")
            searchHint.children().eq(--hintLookup).addClass("hint-active");;
        }
    } else if (e.key !== "Backspace" && e.key.length > 1);
    else {
        if (searchQuery.val() != "") {
            getHint(searchQuery.val());
        } else {
            searchHint.empty();
        }
    }
});

$("#searchButton").on("click", function () {
    searchResult();
});


function playerInit() {
    fetch('actions/guilds.php').then((res) => {
        if (window.location.hash === "#playlist") {
            return;
        }
        if (res.status == 200) {
            res.text().then((output) => {
                if (window.location.hash === "#playlist") {
                    return;
                }
                selectionDiv.children().remove();
                loadingDiv.hide();
                if (output == "") {
                    selectionDivError.show();
                    return;
                }
                selectionDiv.html(output);
                selectionDiv.children().each(function () {
                    this.addEventListener("click", function () {
                        data = new FormData();
                        data.append("guild_id", this.getAttribute("name"));
                        fetch("actions/subscribe.php", {
                            method : "POST",
                            body : data,
                        }).then((res) => {
                            if (res.status == 200) {
                                res.json().then((guild) => {
                                    playerName.text(guild[0]);
                                    playerIcon.attr('src', guild[1]);
                                    guildId = guild[2];

                                    if (window.location.hash === "#playlist") {
                                        return;
                                    }

                                    selectionDiv.hide();
                                    if (guild[1] != "assets/no-image.png") {
                                        playerBg.css("background-image", "url(" + guild[1]  + ")");
                                    } else {
                                        playerBg.css("background-image", "");
                                    }
                                    playerBg.fadeIn(1000);
                                    playerBgAnimate = true;
                                    animatePlayerBg();
                                    playerDiv.show();
                                });
                            } else if (res.status == 401) {
                                window.location.href = "logout.php";
                            }
                        });
                    })
                });
                selectionDiv.show();
            })
        } else if (res.status == 304) {
            loadingDiv.hide();
            playerBg.fadeIn(1000);
            playerBgAnimate = true;
            animatePlayerBg();
            playerDiv.show();
        } else {
            window.location.href = "logout.php";
        }
    });
}

function playlistInit() {

}

function switchPage() {
    loadingDiv.show()
    selectionDiv.hide();
    selectionDivError.hide();
    playerDiv.hide();
    playerBgAnimate = false;
    playerBg.stop(true, true);
    playerBg.fadeOut();
    if (window.location.hash === "#playlist") {
        playlistInit();
    } else {
        playerInit();
    }
}

switchPage();

window.addEventListener('hashchange', () => {
    switchPage();
});

document.getElementById("changeGuild").addEventListener("click", async function () {
    res = await fetch("actions/unsubscribe.php?guild_id=" + guildId);
    if (res.status == 401) {
        window.location.href = "logout.php";
    } else {
        switchPage();
    }
});

document.getElementById("selection_refresh").addEventListener("click", function () {
    switchPage();
});