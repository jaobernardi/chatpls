// Load the IFrame Player API code asynchronously.
var tag = document.createElement('script');
tag.src = "https://www.youtube.com/player_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// Replace the 'ytplayer' element with an <iframe> and
// YouTube player after the API code downloads.
var player;

function onYouTubePlayerAPIReady() {
    player = new YT.Player('ytplayer', {
    height: '360',
    width: '640',
    videoId: 'dQw4w9WgXcQ'
    });

}

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

function update_list(array_queue) {
    queue_element = document.getElementById("queue")
    queue_element.innerHTML = ""
    if (array_queue.length){
        array_queue.forEach(element => {
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
    get_queue(update_list);
    get_current(update_video)
}, 700)