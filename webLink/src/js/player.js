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

queueEmpty.on("click", function () {$("#searchBut").trigger("click");});

const searchQuery = $("#searchQuery");
const searchHint = $("#searchHint");
const searchButton = $("#searchButton");
const searchTray = $("#searchTray");
var hintController = new AbortController();

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
                query = query.split("\"").join("\\\"")

                data = data.split("\",[").slice(1).join("\",[");
                data = JSON.parse("[" + data.split(",{\"")[0]);

                searchHint.empty();
                for(let i = 0; i < data.length; i++) {
                    let hintDom = $('<div class="w-full py-1 px-2 align-middle hover:bg-black hover:bg-opacity-15"></div>');
                    hintDom.text(data[i][0]);
                    hintDom.on("mousedown", function () {
                        searchQuery.val(data[i][0]);
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

function searchResult() {
    searchHint.hide();
    searchTray.empty();
}

searchQuery.keyup(function (e) {
    if (e.key === "Enter") {
        searchResult();
    } else {
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