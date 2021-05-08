import mariadb
from .wrappers import Config
from time import time

class User:
	def __init__(self, username, access_token, refresh_token, id_token, user_id):
		self.username = username
		self.access_token = access_token
		self.refresh_token = refresh_token
		self.id_token = id_token
		self.user_id = user_id
	
	def update_access_token(self, access_token, refresh_token):
		self.access_token = access_token
		self.refresh_token = refresh_token
		with Database() as db:
			db.update_user(self)

class Database:
	def __init__(self):
		config = Config()
		self.conn = mariadb.connect(
			user=config.database['user'],
			password=config.database['password'],
			host=config.database['host'],
			port=config.database['port'],
			database="chatpls"
		)
	def __enter__(self):
		self.__init__()
		return self
	
	def commit(self):
		self.conn.commit()
		self.conn.close()

	def __exit__(self, *args):
		self.commit()

	def delete_token(self, token):
		cursor = self.conn.cursor()
		cursor.execute(
			"DELETE FROM tokens WHERE token=?", 
			(token,)
		)

	def get_tokens(self, user_id):
		cursor = self.conn.cursor()
		cursor.execute(
			"SELECT * FROM tokens WHERE user_id=?", 
			(user_id,)
		)
		x = []
		for row in cursor:
			if (time() - row[2]) >= 604800:
				self.delete_token(row[1])
			else:
				x.append(row[0])
		return x
	
	def get_user(self, username):
		cursor = self.conn.cursor()
		cursor.execute(
			"SELECT * FROM users WHERE username=?", 
			(username,)
		)
		for row in cursor:
			return User(*row)
	
	def update_user(self, user):
		cursor = self.conn.cursor()
		cursor.execute(
			"UPDATE `users` SET `username`=?, `access_token`=?, `refresh_token`=?, `id_token`=?, `user_id`=? WHERE `user_id`=?", 
			(username, access_token, refresh_token, id_token, user_id, user_id)
		)

	def create_user(self, username, access_token, refresh_token, id_token, user_id):
		if not self.get_user(username):
			cursor = self.conn.cursor()
			cursor.execute(
				"INSERT INTO `users`(`username`, `access_token`, `refresh_token`, `id_token`, `user_id`) VALUES (?, ?, ?, ?, ?)", 
				(username, access_token, refresh_token, id_token, user_id)
			)
			return User(username, access_token, refresh_token, id_token, user_id)

	def create_token(self, token, user):
		cursor = self.conn.cursor()
		cursor.execute(
			"INSERT INTO `tokens`(`user_id`, `token`) VALUES (?, ?)", 
			(user.user_id, token)
		)
		return token


