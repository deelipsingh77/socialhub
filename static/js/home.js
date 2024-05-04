let likeContainers = document.getElementsByClassName('like-container')
for (let likeContainer of likeContainers) {
    if (likeContainer.childElementCount == 2){
        likeContainer.lastElementChild.style.display = 'none'
    }
}