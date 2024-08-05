const loadingDiv = $('#loading');
const selectionDiv = $('#selection');
const selectionDivError = $('#emptyServer');
const playerDiv = $('#player');
const playerName = $('#serverName');
const playerIcon = $('#serverIcon');

selectionDiv.hide();
selectionDivError.hide();
playerDiv.hide();

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
    await fetch("actions/unsubscribe.php");
    switchPage();
});

document.getElementById("selection_refresh").addEventListener("click", function () {
    switchPage();
});