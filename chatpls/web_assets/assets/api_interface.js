function get_current(callback){
    Http = new XMLHttpRequest();
    url='https://api.chatpls.live/current/';
    Http.open("GET", url);
    Http.send();

    Http.onreadystatechange = (e) => {
        if (Http.readyState == 4){
            response = Http.responseText
            try {
                response = JSON.parse(response)
            } catch (error) {
                response = {status: 500, data: null}
            }
            if (response.status == 200 && response.data){
                callback(response.data.link, response.data.start_time)
            } else {
                callback(null, null)
            }
        }
    }
}

function get_queue(callback){
    Http = new XMLHttpRequest();
    url='https://api.chatpls.live/queue/';
    Http.open("GET", url);
    Http.send();

    Http.onreadystatechange = (e) => {
        if (Http.readyState == 4){
            response = Http.responseText
            console.log(response)
            try {
                response = JSON.parse(response)
            } catch (error) {
                response = {queue: []}
            }
            console.log(response)
            queue = response.queue
            callback(queue)
    
        }
    }
}
