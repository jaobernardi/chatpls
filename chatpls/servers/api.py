import events
from structures import Response, Config

config = Config()

@events.add_handle("http_request")
def api_http(event):
	request = event.request
	print("reached API")
	if "Host" in request.headers and request.headers["Host"] == config.scopes["api"]:
		default_headers = {
			"Server": "chatpls/1.0",
		}
		path = [i for i in request.path.split("/")[1:] if i]
		print("reached api 2")
		print(path)
		# check api-method.
		match path:
			case ["incoming", *params]:
				message = b'{"status": 200, "message": "reached incoming path.", "error": false}'
				return Response.make(
					200,
					'OK',
					default_headers | {'Content-Type': 'application/json',
					'Content-Length': len(message)},
					message
				)
			case _:
				message = b'{"status": 200, "message": "ok.", "error": false}'
				return Response.make(
					200,
					'OK',
					default_headers | {'Content-Type': 'application/json',
					'Content-Length': len(message)},
					message
				)
		print("omegalul")