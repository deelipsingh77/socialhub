let likeContainers = document.getElementsByClassName("like-container");
for (let likeContainer of likeContainers) {
  if (likeContainer.childElementCount == 2) {
    likeContainer.lastElementChild.style.display = "none";
  }
}

let followButtons = document.getElementsByClassName("follow-button");
for (let followButton of followButtons) {
  if (followButton.innerText == "") {
    followButton.innerText = "Follow";
  }
}
