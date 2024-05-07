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



document.addEventListener("DOMContentLoaded", function () {
  const dropdownToggle = document.getElementById('dropdownToggle');
  const dropdownMenu = document.getElementById('dropdownMenu');

  dropdownToggle.addEventListener('click', function (event) {
    dropdownMenu.classList.toggle('hidden');
    dropdownMenu.classList.toggle('block');
  });

});



const logoText = document.getElementById('logo-text');
const text = "SocialHub";
let index = 0;

let post_card = document.getElementsByClassName('posts-card')
function posts_animation() {
  let c = true
  for (let post of post_card) {
    if (c) {
      post.attributes[0].nodeValue = "fade-left"
      console.log(post_card[0].attributes[0].nodeValue)
      c=false
    }
    else {
      post.attributes[0].nodeValue = "fade-right"
      c=true
    }
  }
}
posts_animation()





