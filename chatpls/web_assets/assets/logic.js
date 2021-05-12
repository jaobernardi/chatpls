function queue_item_element(text) {
    element = document.createElement("h4")
    element.innerText = text
    return text
}

function update_list(queue) {
    queue_element = document.getElementById("queue")
    queue_element.innerHTML = ""
    if (queue){
        queue.forEach(element => {
            queue_element.appendChild(queue_item_element(element.username))
        });
    } else {
        queue_element.appendChild("Nada por aqui . . . ")
    }

}

setInterval(()=>{
    get_queue((queue) => {update_list(queue)})
}, 100)