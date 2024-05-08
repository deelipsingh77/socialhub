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
    dropdownMenu.classList.add('animate')
    dropdownMenu.classList.toggle('block');
  });

});





document.addEventListener("DOMContentLoaded", function () {
  var navLinks = document.querySelectorAll(".nav-link");
  var feedLinks = document.querySelectorAll(".feed-link");
  // Function to add active class to the link
  function setActiveLink() {
    var currentPath = window.location.pathname;
    navLinks.forEach(function (link) {
      
      if (`${link.getAttribute("href")}/` === currentPath) {
        link.classList.add("active");
      } else {
        link.classList.remove("active");
      }
    });
    feedLinks.forEach(function (link) {
      if (`${link.getAttribute("href")}/` === currentPath) {
        link.classList.add("active");
      } else {
        link.classList.remove("active");
      }
    });
  }

  // Call the function initially
  setActiveLink();

  // Call the function whenever the user clicks on a link
  navLinks.forEach(function (link) {
    link.addEventListener("click", setActiveLink);
  });

  feedLinks.forEach(function (link) {
    link.addEventListener("click", setActiveLink);
  });
});





