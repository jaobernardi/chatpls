function image_element(link){
    element = document.createElement("img")
    element.href = link
    return element
}

function queue_item_element(text) {
    element = document.createElement("h4")
    element.align = "center"
    element.innerText = text
    return element
}

function update_list(queue) {
    queue_element = document.getElementById("queue")
    queue_element.innerHTML = ""
    if (queue){
        queue.forEach(element => {
            queue_element.appendChild(queue_item_element(element.username))
        });
    } else {
        no_one = queue_item_element("Nada por aqui . . . ")
        no_one.innerHTML += image_element("https://cdn.betterttv.net/emote/5d7eefb7c0652668c9e4d394/1x")
        queue_element.appendChild(no_one)
    }

}

setInterval(()=>{
    get_queue((queue) => {update_list(queue)})
}, 100)