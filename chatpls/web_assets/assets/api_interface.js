function get_current(callback){
    Http = new XMLHttpRequest();
    url='https://api.chatpls.live/current/';
    Http.open("GET", url);
    Http.send();

    Http.onreadystatechange = (e) => {
        response = Http.responseText
        if (response.status == 200 && response.queue){
            callback(response.queue.link, response.queue.start_time)
        } else {
            callback(null, null)
        }
    }
}

function get_queue(callback){
    Http = new XMLHttpRequest();
    url='https://api.chatpls.live/queue/';
    Http.open("GET", url);
    Http.send();

    Http.onreadystatechange = (e) => {
        response = Http.responseText
        callback(response.data)
    }
}
