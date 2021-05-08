import events
from structures import Response, Config

config = Config()

@events.add_handle("http_request", priority=-1)
def fallback_http(event):
	request = event.request
    default_headers = {
        "Server": "chatpls/1.0",
    }
    return Response.make(
        200,
        'OK',
        default_headers,
        b"If you're reading this, you fucked up."
    )
		