import mariadb
from .wrappers import Config
from time import time
from datetime import datetime, timedelta

class User(object):
	def __init__(self, username, access_token, refresh_token, id_token, user_id, is_mod):
		self.username = username
		self.access_token = access_token
		self.refresh_token = refresh_token
		self.id_token = id_token
		self.user_id = user_id
		self.is_mod = is_mod
	
	def update_access_token(self, access_token, refresh_token):
		self.access_token = access_token
		self.refresh_token = refresh_token
		with Database() as db:
			db.update_user(self)

	@property
	def permissions(self):
		with Database() as db:
			return db.get_permissions(self.username)
	
	@permissions.setter
	def permissions_setter(self, new_value):
		with Database() as db:
			return db.set_permissions(self, new_value)

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

	def get_tokens(self, user_id=None, token=None, return_time=False):
		cursor = self.conn.cursor()
		if user_id:
			cursor.execute(
				"SELECT * FROM tokens WHERE user_id=?", 
				(user_id,)
			)
		elif token:
			cursor.execute(
				"SELECT * FROM tokens WHERE token=?", 
				(token,)
			)
		x = []
		times = []
		for row in cursor:
			if (row[2].timestamp() - datetime.now().timestamp()) <= 0:
				with Database() as db:
					db.delete_token(row[1])
			else:
				times.append(row[2])
				if token:
					x.append(row[0])
					
				elif user_id:
					x.append(row[1])
		if return_time:
			return x, times
		return x
	
	def get_user(self, username=None, user_id=None):
		cursor = self.conn.cursor()
		if username:
			cursor.execute(
				"SELECT * FROM users WHERE username=?", 
				(username,)
			)
		elif user_id:
			cursor.execute(
				"SELECT * FROM users WHERE user_id=?", 
				(user_id,)
			)
		else:
			raise ValueError("Missing value for username or user_id.")
		
		for row in cursor:
			return User(*row)
	
	def update_user(self, user):
		cursor = self.conn.cursor()
		cursor.execute(
			"UPDATE `users` SET `username`=?, `access_token`=?, `refresh_token`=?, `id_token`=?, `user_id`=?, `is_mod`=? WHERE `user_id`=?", 
			(user.username, user.access_token, user.refresh_token, user.id_token, user.user_id, user.is_mod, user.user_id)
		)

	def create_user(self, username, access_token, refresh_token, id_token, user_id):
		if not self.get_user(username):
			cursor = self.conn.cursor()
			cursor.execute(
				"INSERT INTO `users`(`username`, `access_token`, `refresh_token`, `id_token`, `user_id`) VALUES (?, ?, ?, ?, ?)", 
				(username, access_token, refresh_token, id_token, user_id)
			)
			return User(username, access_token, refresh_token, id_token, user_id)

	def get_queue(self):
		cursor = self.conn.cursor()
		cursor.execute(
			"SELECT * FROM queue ORDER BY add_time ASC", 
		)
		return [{"username": row[0], "link": row[1], "add_time": row[2], "likes": row[3], "dislikes": row[4], "start_time": row[5], "length": row[6]} for row in cursor]
	
	def delete_from_queue(self, username):
		cursor = self.conn.cursor()
		cursor.execute(
			"DELETE FROM queue WHERE username=?", 
			(username,)
		)

	def queue_set_running(self, username, start_time):
		cursor = self.conn.cursor()
		cursor.execute(
			"UPDATE `queue` SET `start_time`=? WHERE `username`=?",
			(start_time, username)
		)
	def get_user_queue(self, username):
		cursor = self.conn.cursor()
		cursor.execute(
			"SELECT * FROM queue WHERE username=?",
			(username,) 
		)
		return [{"username": row[0], "link": row[1], "add_time": row[2], "likes": row[3], "dislikes": row[4], "start_time": row[5], "length": row[6]} for row in cursor]
	
	def append_to_queue(self, username, link, add_time, length):
		cursor = self.conn.cursor()
		cursor.execute(
			"INSERT INTO `queue`(`username`, `link`, `add_time`, `length`) VALUES (?, ?, ?, ?)",
			(username, link, add_time, length)
		)

	def create_token(self, token, user):
		cursor = self.conn.cursor()
		cursor.execute(
			"INSERT INTO `tokens`(`user_id`, `token`, `creation`) VALUES (?, ?, ?)", 
			(user.user_id, token, datetime.now()+timedelta(days=10))
		)
		return token


