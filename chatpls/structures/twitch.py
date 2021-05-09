# Internal use ONLY.
import requests
from .database import User


class TwitchAPI:
	def __init__(self, client_id, client_secret):
		self.client_id = client_id
		self._client_secret = client_secret
	
	def refresh_access_token(self, refresh_token):
		request = requests.post(f"https://id.twitch.tv/oauth2/token?grant_type=refresh_token&refresh_token={refresh_token}&client_id={self.client_id}&client_secret={self._client_secret}")
		request_json = request.json()
		return request_json["access_token"], request_json["refresh_token"]

	def userinfo_data(self, user: User):
		request = requests.get("https://id.twitch.tv/oauth2/userinfo", headers={"Authorization": f"Bearer {user.access_token}"})
		if request.status_code != 200:
			new_access_token, new_refresh_token = self.refresh_access_token(user.refresh_token)
			user.update_access_token(new_access_token, new_refresh_token)
			return userinfo_data(user)
		return request.json()

	def check_follow(self, user: User):
		request = request.get(f"https://api.twitch.tv/helix/users/follows?from_id={user.user_id}&to_id=28579002", headers={"Authorization": f"Bearer {user.access_token}", "Client-Id": self.client_id})
		if request.status_code != 200:
			new_access_token, new_refresh_token = self.refresh_access_token(user.refresh_token)
			user.update_access_token(new_access_token, new_refresh_token)
			return check_follow(user)
		request = request.json()
		if request['total'] > 0:
			return True
		return False

	def get_user_subscription_status(self, access_token, refresh_token, id):
		request = request.get(f"https://api.twitch.tv/helix/subscriptions/user?user_id={user.user_id}&broadcaster_id=28579002", headers={"Authorization": f"Bearer {user.access_token}", "Client-Id": self.client_id})
		if request.status_code not in [200, 404]:
			new_access_token, new_refresh_token = self.refresh_access_token(user.refresh_token)
			user.update_access_token(new_access_token, new_refresh_token)
			return check_follow(user)

		if request.status_code == 200:
			return True
		return False
	