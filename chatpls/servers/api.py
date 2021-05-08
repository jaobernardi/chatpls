import events
from structures import Response, Config

config = Config()

@events.add_handle("http_request")
def api_http(event):
	request = event.request
	if "Host" in request.headers and request.headers["Host"] == config.scopes["api"]:
		default_headers = {
			"Server": "chatpls/1.0",
		}
		path = [i.lower() for i in request.path.split("/")[1:] if i]
		# check api-method.
		if path[0] == "incoming":
			message = b'{"status": 200, "message": "reached incoming path.", "error": false}'
			return Response.make(
				200,
				'OK',
				default_headers | {'Content-Type': 'application/json',
				'Content-Length': len(message)},
				message
			)
		else:
			message = b'{"status": 200, "message": "ok.", "error": false}'
			return Response.make(
				200,
				'OK',
				default_headers | {'Content-Type': 'application/json',
				'Content-Length': len(message)},
				message
			)
