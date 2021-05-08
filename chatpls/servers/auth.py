import events
from structures import Response, Config

config = Config()

@events.add_handle("http_request")
def auth_http(event):
	request = event.request
	if "Host" in request.headers and request.headers["Host"] == config.scopes["auth"]:
		default_headers = {
			"Server": "chatpls/1.0",
		}
		print(request.query_string)
		print(request.method)
		print(request.data)
