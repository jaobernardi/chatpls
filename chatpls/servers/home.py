import events
from structures import Response, Config
import os
import json

config = Config()
mime_types = json.load(open("mime_types.json"))

@events.add_handle("http_request")
def normal_http(event):
	request = event.request
	if "Host" in request.headers and request.headers["Host"] == config.scopes["main"]:
		default_headers = {
			"Server": "chatpls/1.0",
		}
		content = open("web_assets\\index.html", "rb").read()
		return Response.make(
			404,
			'Not Found', 
			default_headers|{
				'Content-Type': 'text/html',
				'Content-Length': len(content)
			},
			content
		)