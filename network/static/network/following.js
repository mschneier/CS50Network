const followButton = document.getElementById("followButton");
followButton.addEventListener("click", async function() {
    let response = await fetch(`/changefollowstatus/${followButton.id}/`, {
        method: "PUT"
    });
    if (response.ok) {
        if (button.innerText == "Follow") {
            button.innerText = "Unfollow";
            button.classList = "btn btn-danger";
        } else {
            button.innerText = "Follow";
            button.classList = "btn btn-primary";
        }
    } else {
        console.error(`HTTP-Error: ${response.status}`);
    }
});
