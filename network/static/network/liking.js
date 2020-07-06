for (let button of document.getElementsByTagName("button")) {
    button.addEventListener("click", async function() {
        let response = await fetch(`/changelikestatus/${button.id}/`, {
            method: "PUT"
        });
        if (response.ok) {
            const likeNumber = document.getElementById(`likes${button.id}`);
            if (button.innerText == "Like") {
                button.innerText = "Unlike";
                button.classList = "btn btn-danger";
                likeNumber.innerText = Number(likeNumber.innerText) + 1;
            } else {
                button.innerText = "Like";
                button.classList = "btn btn-primary";
                likeNumber.innerText = Number(likeNumber.innerText) - 1;
            }
        } else {
            console.error(`HTTP-Error: ${response.status}`)
        }
    });
}
