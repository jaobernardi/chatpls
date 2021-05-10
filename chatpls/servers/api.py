import events
from structures import Response, Config, Database, TwitchAPI
import json
import time
from urllib.parse import urlparse
from datetime import datetime

config = Config()
twitch = TwitchAPI('r9fxp28e0wimgjdpf9dg050ncn7spi', config.client_secret)


def format_queue(inp):
	queue = []
	for item in inp:
		item["add_time"] = item["add_time"].timestamp()
		item["start_time"] = item["start_time"].timestamp()
		queue.append(item)
	return queue

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
				else:
					with Database() as db:
						queue = format_queue(db.get_queue())
						output = {"status": 200, "message": "OK", "error": False, "data": None if not queue else queue[0]}

			case ["current", "reaction"]:
				output = {"status": 501, "message": "Not Implemented", "error": True}
				
			case ["current", "skip"]:
				if request.method != "POST":					
					default_headers = default_headers | {'Allow': 'POST'}
					output = {"status": 405, "message": "Method Not Allowed", "error": True}
				elif 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json':
					try:
						data = json.loads(request.data.decode("utf-8"))
						match data:
							case {"token": token}:								
								with Database() as db:
									users = db.get_tokens(token=token)	
									if users and db.get_user(user_id=users[0]).is_mod:
										if queue := db.get_queue():
											db.delete_from_queue(queue[0]["username"])
											output = {"status": 200, "message": "OK", "error": False}
										else:
											output = {"status": 404, "message": "Not Found", "error": True}
									else:
										output = {"status": 403, "message": "Unauthorized", "error": True}
							case _:
								output = {"status": 422, "message": "Unprocessable Entity", "error": True}
					except Exception as e:					
						output = {"status": 422, "message": "Unprocessable Entity", "error": True}
				else:							
					output = {"status": 422, "message": "Unprocessable Entity", "error": True}

			case ["queue"]:
				if request.method != "GET":					
					default_headers = default_headers | {'Allow': 'POST'}
					output = {"status": 405, "message": "Method Not Allowed", "error": True}
				else:
					with Database() as db:
						output = {"status": 200, "message": "OK", "error": False, "queue": format_queue(db.get_queue())}

			case ["queue", "join"]:
				if request.method != "POST":					
					default_headers = default_headers | {'Allow': 'POST'}
					output = {"status": 405, "message": "Method Not Allowed", "error": True}
				elif 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json':
					try:
						data = json.loads(request.data.decode("utf-8"))
						match data:
							case {"token": token, "link": link}:								
								with Database() as db:
									users = db.get_tokens(token=token)
									print(users)
									if users:
										user = db.get_user(user_id=users[0])
										if twitch.check_subscription(user):
											print(urlparse(link))
											if urlparse(link).netloc == "youtube.com":
												db.append_to_queue(user.username, link, datetime.now())
												output = {"status": 200, "message": "OK", "error": False}
											else:
												output = {"status": 422, "message": "Unprocessable Entity", "error": True}
										else:
											output = {"status": 403, "message": "Unauthorized", "error": True, "not_sub": True}
									else:
										output = {"status": 403, "message": "Unauthorized", "error": True}
							case _:
								output = {"status": 422, "message": "Unprocessable Entity", "error": True}
					except Exception as e:					
						output = {"status": 422, "message": "Unprocessable Entity", "error": True}
				else:							
					output = {"status": 422, "message": "Unprocessable Entity", "error": True}

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
