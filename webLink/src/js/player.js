const loadingDiv = $('#loading');
const selectionDiv = $('#selection');
const selectionDivError = $('#emptyServer');
const playerDiv = $('#player');
const playerName = $('#serverName');
const playerIcon = $('#serverIcon');
const playerBg = $('#playerBackground');

selectionDiv.hide();
selectionDivError.hide();
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
    res = await fetch("actions/unsubscribe.php");
    if (res.status == 401) {
        window.location.href = "logout.php";
    } else {
        switchPage();
    }
});

document.getElementById("selection_refresh").addEventListener("click", function () {
    switchPage();
});