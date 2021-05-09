import events
from structures import Response, Config, Database, TwitchAPI
import json

config = Config()
twitch = TwitchAPI('r9fxp28e0wimgjdpf9dg050ncn7spi', config.client_secret)
queue = []
current = {
	'data': {'link': '', 'likes': 0, 'dislikes': 0, 'time': 0},
	'stats': {}
}

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
					default_headers = default_headers | {'Allow': 'POST'}
					output = {"status": 405, "message": "Method Not Allowed", "error": True}
				elif not current:					
					output = {"status": 404, "message": "Not Found", "error": True}
				elif 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json':
					if True:
						data = json.loads(request.data.decode("utf-8"))
						match data:
							case {"token": token, "action_id": action_id}:
								with Database() as db:
									users = db.get_tokens(token=token)	
								print(users)												
								if users:
									if users[0] not in current["stats"]:
										current["stats"] = action_id
										if action_id == 0:
											current["data"]["likes"] += 1
										elif action_id == 1:
											current["data"]["dislikes"] += 1
										else:
											output = {"status": 422, "message": "Unprocessable Entity", "error": True}
									if current["stats"] == action_id:										
										output = {"status": 200, "message": "OK", "error": False}
									else:
										if action_id == 0 and current["stats"] == 1:
											current["data"]["dislikes"] -= 1
											current["data"]["likes"] += 1
											output = {"status": 200, "message": "OK", "error": False}
										elif action_id == 1 and current["stats"] == 0:
											current["data"]["dislikes"] += 1
											current["data"]["likes"] -= 1

											output = {"status": 200, "message": "OK", "error": False}
										else:
											output = {"status": 422, "message": "Unprocessable Entity", "error": True}
								else:
									output = {"status": 403, "message": "Unauthorized", "error": True}
							case _:
								output = {"status": 422, "message": "Unprocessable Entity", "error": True}
					#except Exception as e:
					#	print(e)						
					#	output = {"status": 422, "message": "Unprocessable Entity", "error": True}
				else:							
					output = {"status": 422, "message": "Unprocessable Entity", "error": True}
				
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
