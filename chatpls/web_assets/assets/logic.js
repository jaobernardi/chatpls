function image_element(link){
    element = document.createElement("img")
    element.src = link
    return element
}

function queue_item_element(text) {
    element = document.createElement("h4")
    element.align = "center"
    element.style = "padding: 1.5vh"
    element.innerText = text
    return element
}

var modCheck = image_element("https://cdn.betterttv.net/emote/5d7eefb7c0652668c9e4d394/1x");

function update_list(input) {
    queue_element = document.getElementById("queue")
    queue_element.innerHTML = ""
    if (input.length){
        input.forEach(element => {
            queue_element.appendChild(queue_item_element(element.username))
        });
    } else {
        no_one = queue_item_element("Nada por aqui . . . ")
        no_one.appendChild(modCheck)
        queue_element.appendChild(no_one)
    }
}

function update_video(id, start_time){
    if (id){
        if (player.getVideoData().video_id != id){
            player.loadVideoById(id)
        }
    }
}

setInterval(()=>{
    get_queue((queue) => {update_list(queue)});
}, 700)
setInterval(()=>{
    get_current((id, start_time)=>{update_video(id, start_time)})
}, 700)