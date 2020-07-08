for (let button of document.getElementsByClassName("followButton")) {
    button.addEventListener("click", async function() {
        const userID = button.getAttribute("data-userID");
        let response = await fetch(`/changefollowstatus/${userID}/`, {
            method: "PUT"
        });
        if (response.ok) {
            if (button.innerText == "Follow") {
                button.innerText = "Unfollow";
                button.classList = "btn btn-warning";
            } else {
                button.innerText = "Follow";
                button.classList = "btn btn-primary";
            }
        } else {
            console.error(`HTTP-Error: ${response.status}`);
        }
    });
}