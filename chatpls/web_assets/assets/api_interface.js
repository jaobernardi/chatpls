function get_current(callback){
    current_request = new XMLHttpRequest();
    url='https://api.chatpls.live/current/';
    current_request.open("GET", url);
    current_request.send();

    current_request.onreadystatechange = (e) => {
        if (current_request.readyState == 4){
            response = current_request.responseText
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
    queue_request = new XMLHttpRequest();
    url='https://api.chatpls.live/queue/';
    queue_request.open("GET", url);
    queue_request.send();

    queue_request.onreadystatechange = (e) => {
        if (queue_request.readyState == 4){
            response = queue_request.responseText
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
