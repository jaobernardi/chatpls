import events
from structures import Response, Config, Database, TwitchAPI
import json

config = Config()
twitch = TwitchAPI('r9fxp28e0wimgjdpf9dg050ncn7spi', config.client_secret)
queue = []
current = {"song": 1}

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
				if request.method != "GET":
					default_headers = default_headers | {'Allow': 'GET'}
					output = {"status": 405, "message": "Method Not Allowed", "error": True}
				elif not current:
					output = {"status": 404, "message": "Not Found", "error": True, "data": current}
				else:
					output = {"status": 200, "message": "OK", "error": False, "data": current}

			case ["current", "reaction"]:
				if request.method != "POST":
					print("1")
					default_headers = default_headers | {'Allow': 'POST'}
					output = {"status": 405, "message": "Method Not Allowed", "error": True}
				elif not current:
					print("2")
					output = {"status": 404, "message": "Not Found", "error": True}
				elif 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json':
					print("3")
					print(request.data)
					try:
						data = json.loads(request.data)
						print(data)
						match data:
							case {"token": token, "username": username, "action_id": action_id}:
								output = {"status": 501, "message": "Not Implemented.", "error": True}
							case _:
								output = {"status": 422, "message": "Unprocessable Entity", "error": True}
					except:
						print("4")
						output = {"status": 422, "message": "Unprocessable Entity", "error": True}

				else:			
					print("5")		
					output = {"status": 422, "message": "Unprocessable Entity", "error": True}
				print(output)
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
