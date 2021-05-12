function get_current(callback){
    Http = new XMLHttpRequest();
    url='https://api.chatpls.live/current/';
    Http.open("GET", url);
    Http.send();

    Http.onreadystatechange = (e) => {
        response = Http.responseText
        if (response.status == 200 && response.data){
            callback(response.data.link, response.data.start_time)
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
        try {
            response = JSON.parse(response)
        } catch (error) {
            response = []
        }
        
        callback(response.queue)
    }
}
