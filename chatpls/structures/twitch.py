# Internal use ONLY.
import requests
from .database import User


class TwitchAPI:
	def __init__(self, client_id, client_secret):
		self.client_id = client_id
		self._client_secret = client_secret
	
	def refresh_access_token(self, refresh_token):
		request = requests.get(f"https://id.twitch.tv/oauth2/token?grant_type=refresh_token&refresh_token={refresh_token}&client_id={self.client_id}&client_secret={self._client_secret}")
		request_json = request.json()
		return request_json["access_token"], request_json["refresh_token"]

	def userinfo_data(self, user: User):
		request = requests.get("https://id.twitch.tv/oauth2/userinfo", headers={"Authorization": f"Bearer {user.access_token}"})
		if request.status_code != 200:
			new_access_token, new_refresh_token = self.refresh_access_token(user.refresh_token)
			user.update_access_token(new_access_token, new_refresh_token)
			return userinfo_data(user)
		return request.json()

	def get_user_follows(self, access_token, refresh_token, id, channel_id):
		return False
	def get_user_subscription_status(self, access_token, refresh_token, id):
		return False