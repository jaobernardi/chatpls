function get_current(callback){
    Http = new XMLHttpRequest();
    url='https://api.chatpls.live/current/';
    Http.open("GET", url);
    Http.send();

    Http.onreadystatechange = (e) => {
        response = JSON.parse(Http.responseText)
        if (response.status == 200){
            callback(response.link, response.start_time)
        } 
    }
}