import events
from structures import Response, Config

config = Config()

queue = []
current = None

@events.add_handle("http_request")
def api_http(event):
	request = event.request
	if "Host" in request.headers and request.headers["Host"] == config.scopes["api"]:
		default_headers = {
			"Server": "chatpls/1.0",
		}
		# check api-method.
		match event.path:
			case ["current"]:
				message = b'{"status": 200, "message": "reached incoming path.", "error": false}'
				return Response.make(
					200,
					'OK',
					default_headers | {'Content-Type': 'application/json',
					'Content-Length': len(message)},
					message
				)
			case []:
				message = b'{"status": 200, "message": "OK", "error": false}'
				return Response.make(
					200,
					'OK',
					default_headers | {'Content-Type': 'application/json',
					'Content-Length': len(message)},
					message
				)
			case _:
				message = b'{"status": 404, "message": "Not Found.", "error": true}'
				return Response.make(
					404,
					'Not Found',
					default_headers | {'Content-Type': 'application/json',
					'Content-Length': len(message)},
					message
				)
