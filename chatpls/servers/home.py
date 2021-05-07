import events
from structures import Response, Config
import os
import json

config = Config()
mime_types = json.load(open("mime_types.json"))
errors = {
	404: b"",
	403: b"",
	500: b"",
	}


@events.add_handle("http_request")
def normal_http(event):
	request = event.request
	if "Host" in request.headers and request.headers["Host"] == config.scopes["home"]:
		default_headers = {
			"Server": "chatpls/1.0",
		}
		path = os.path.join("web_assets/", request.path.removeprefix("/"))

		if ".." in path:
			return Response.make(
				403,
				'Unauthorized', 
				default_headers|{
					'Content-Type': 'text/html',
					'Content-Length': len(errors[403])
				},
				errors[403]
			)
		if os.path.exists(path):
			# detect file
			if os.path.isfile(path):
				filename = path
			elif os.path.exists(os.path.join(path, 'index.html')):
				filename = os.path.join(path, "index.html")
			else:
				return Response.make(
					404,
					'Not Found', 
					default_headers|{
						'Content-Type': 'text/html',
						'Content-Length': len(errors[404])
					},
					errors[404]
				)
		else:
			# not found response
				return Response.make(
					404,
					'Not Found', 
					default_headers|{
						'Content-Type': 'text/html',
						'Content-Length': len(errors[404])
					},
					errors[404]
				)
		data = open(filename, 'rb').read()
		prefix = os.path.basename(filename).split(".")[-1]
		if prefix in mime_types:
			default_headers['Content-Type'] = mime_types[prefix]
		return Response.make(
			200,
			'OK', 
			default_headers|{
				'Content-Length': len(data),
			},
			data
		)
