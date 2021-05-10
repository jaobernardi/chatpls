import events
from structures import Response, Config, TwitchAPI, Database, User
import requests
import json
from random import choice
from string import ascii_letters
from time import time

errors = {
	404: b"",
	403: b"",
	500: b"",
	}

config = Config()
twitchapi = TwitchAPI('r9fxp28e0wimgjdpf9dg050ncn7spi', config.client_secret)

@events.add_handle("http_request")
def auth_http(event):
	request = event.request
	if "Host" in request.headers and request.headers["Host"] == config.scopes["auth"]:
		default_headers = {
			"Server": "chatpls/1.0",
		}
		match event.path:
			case []:
				if "code" in request.query_string:
					twitch_request = requests.post(f'https://id.twitch.tv/oauth2/token?client_id=r9fxp28e0wimgjdpf9dg050ncn7spi&client_secret={config.client_secret}&code={request.query_string["code"]}&grant_type=authorization_code&redirect_uri=https://auth.chatpls.live')
					twitch_query = twitch_request.json()
					user_request = requests.get("https://id.twitch.tv/oauth2/userinfo", headers={"Authorization": f"Bearer {twitch_query['access_token']}"})
					user_info = user_request.json()
					update_user = False
					time_left = 604800
					with Database() as db:
						user = db.create_user(user_info["preferred_username"], twitch_query["access_token"], twitch_query["refresh_token"], twitch_query["id_token"], user_info["sub"])
						
						# if user already exists, get a existent token and update user.
						if not user:
							update_user = True
							# Grab the user object
							user = db.get_user(user_info["preferred_username"])						
							# get existent tokens
							tokens_query, tokens_time = db.get_tokens(user.user_id, return_time=True)
							# if there is no tokens, create a new one.
							if not tokens_query:
								token = db.create_token("".join([choice(ascii_letters) for i in range(100)]), user)
							# if there is a token, return it.
							else:
								time_left = tokens_time[0].timestamp() - time()
								token = tokens_query[0]
						# if user is new, create a new token.
						else:
							token = db.create_token("".join([choice(ascii_letters) for i in range(100)]), user)
					
					if update_user:
						user.update_access_token(twitch_query["access_token"], twitch_query["refresh_token"])
					print(time_left)
					return Response.make(
						302,
						'Found',
						default_headers | {'Location': 'https://chatpls.live',
						'Set-Cookie': f'sessionToken={token}; Max-Age={time_left}; Secure; Domain=chatpls.live'},
						b""
					)
				return Response.make(
					302,
					'Found',
					default_headers | {'Location': "https://id.twitch.tv/oauth2/authorize?client_id=r9fxp28e0wimgjdpf9dg050ncn7spi&redirect_uri=https://auth.chatpls.live&response_type=code&scope=openid user:read:subscriptions user:read:follows"},
					b""
				)
			case ["tokens"]:
				message = b'{"status": 501, "message": "Not Implemented", "error": true}'
				return Response.make(
					501,
					'Not Implemented',
					default_headers | {'Content-Type': 'application/json',
					'Content-Length': len(message)},
					message
				)
			case _:
				return Response.make(
					403,
					'Unauthorized', 
					default_headers|{
						'Content-Type': 'text/html',
						'Content-Length': len(errors[403])
					},
					errors[403]
				)
