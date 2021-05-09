import events
from structures import Response, Config
import json

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
				output = {"status": 501, "message": "Not Implemented.", "error": True}

			case ["current", "reaction"]:
				output = {"status": 501, "message": "Not Implemented.", "error": True}

			case ["current", "action"]:
				output = {"status": 501, "message": "Not Implemented.", "error": True}

			case ["current", "reaction"]:
				output = {"status": 501, "message": "Not Implemented.", "error": True}

			case ["queue"]:
				output = {"status": 501, "message": "Not Implemented.", "error": True}

			case ["queue", "join"]:
				output = {"status": 501, "message": "Not Implemented.", "error": True}

			case ["queue", "leave"]:
				output = {"status": 501, "message": "Not Implemented.", "error": True}

			case ["queue", "keepalive"]:
				output = {"status": 501, "message": "Not Implemented.", "error": True}

			case []:
				output = {"status": 200, "message": "OK", "error": False}

			case _:
				output = {"status": 404, "message": "Not Found", "error": True}

		jsonfied = json.dumps(output).encode()
		return Response.make(
			output["status"],
			output["message"],
			default_headers | {'Content-Type': 'application/json',
			'Content-Length': len(jsonfied)},
			jsonfied
		)
