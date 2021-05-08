import events
from structures import Response, Config
import requests
import json


config = Config()

@events.add_handle("http_request")
def auth_http(event):
	request = event.request
	if "Host" in request.headers and request.headers["Host"] == config.scopes["auth"]:
		default_headers = {
			"Server": "chatpls/1.0",
		}
		if "code" in request.query_string:
			twitch_query = requests.post(f'https://id.twitch.tv/oauth2/token?client_id=r9fxp28e0wimgjdpf9dg050ncn7spi&client_secret={config.client_secret}&code={request.query_string["code"]}&grant_type=authorization_code&redirect_uri=https://auth.chatpls.live')
	
			return Response.make(
				200,
				'OK',
				default_headers | {'Content-Type': 'application/json'},
				json.dumps(twitch_query.json()).encode()
			)
		return Response.make(
			302,
			'Found',
			default_headers | {'Location': "https://id.twitch.tv/oauth2/authorize?client_id=r9fxp28e0wimgjdpf9dg050ncn7spi&redirect_uri=https://auth.chatpls.live&response_type=code&scope=openid user:read:subscriptions user:read:follows"}
			b""
		)