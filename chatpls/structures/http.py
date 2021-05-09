import events
import tasks
import socket
from time import time
from urllib.parse import unquote
import ssl


# HTTPS Server class
class Server(object):
	''' 
	This class powers the https server 
	'''
	def __init__(self, host, port, certificate, private_key):
		# Initialize variables
		self.host = host
		self.port = port
		if certificate and private_key:
			self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
			self.context.load_cert_chain(certificate, private_key)

	def http_start(self):
		# Create socket, bind and listen.
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((self.host, self.port))
		self.socket.listen(50)
		# Start connection loop
		while True:
			# Accept connection
			conn, addr = self.socket.accept()
			# Route connection to thread
			self.http_request_handler(conn, addr)

	def https_start(self):
		# Create socket, bind and listen.
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((self.host, self.port))
		self.socket.listen(50)
		# Start connection loop
		with self.context.wrap_socket(self.socket, server_side=True) as ssock:
			while True:
				try:
					# Accept connection
					conn, addr = ssock.accept()
					# Route connection to thread
					self.http_request_handler(conn, addr)
				except ssl.SSLError:
					pass
				except Exception as e:
					print(e)
	@classmethod
	@tasks.thread_function
	def http_request_handler(cls, conn, addr):
		# Recieve data
		data = b""
		headers = {}
		while True:			
			if b"\r\n\r\n" in data:
				for line in data.split(b"\n")[1:]:
					headers[line.split(b": ")[0].decode('utf-8')] = b"".join(line.split(b": ")[1:]).decode('utf-8')
				if "Content-Length" in headers:
					body = b"\r\n\r\n".join(data.split(b"\r\n\r\n")[1:])
					print(len(body), headers["Content-Length"])
					if len(body) >= headers["Content-Length"]:
						break
				else:
					break
			new_data = conn.recv(1)
			if not new_data:
				break
			data += new_data
		print(data)
		try:
			request = Request(data, acknowledge=time())
			event = events.call_event("http_request", request=request, connection=conn, address=addr)
			events.call_event("http_response", request=request, resp=event.response.decode('utf-8'))
			if event.response:
				conn.send(event.response)
		except IndexError:
			pass
		conn.close()
		
		pass

	def stop(self):
		self.socket.close()
		pass


class Request(object):
	'''
	This class handles the client-side requests
	'''

	def __init__(self, data: bytes, acknowledge):
		self.acknowledge = acknowledge
		lines = data.split(b"\n")
		if lines[0].endswith(b"\r"):
			lines = data.split(b"\r\n")

		self.method = lines[0].split(b" ")[0].decode('utf-8')
		self.path = lines[0].split(b" ")[1].split(b"?")[0].decode('utf-8')

		self.query_string = {}

		query_string = lines[0].split(b" ")[1].split(b"?")
		if len(query_string) > 1:
			for query_string in query_string[1].split(b"&"):
				string = query_string.split(b"=")
				self.query_string[unquote(string[0].decode('utf-8'))] = unquote(b"".join(string[1:]).decode('utf-8'))

		self.content = b""
		self.headers = {}
		self._hit_switch = False
		self._index = 0
		for line in lines[1:]:
			if not line:
				self._hit_switch = True
				break
			self.headers[line.split(b": ")[0].decode('utf-8')] = b"".join(line.split(b": ")[1:]).decode('utf-8')
			self._index+=1
		print(data)
		self.data = b"\r\n\r\n".join(data.split(b"\r\n\r\n")[1:])


	def append_data(self, data):
		# TODO: Add support for appending data after instanciate
		# This will allow truncate requests to be handled easier.
		pass


class Response(object):
	'''
	This class handles the server's responses.
	'''
	def __init__(self, status_code, status_message, headers={}, data=b""):
		self.status_code = status_code
		self.status_message = status_message
		self.headers = headers
		self.data = data

	def build(self):
		status = f"HTTP/1.1 {self.status_code} {self.status_message}".encode("utf-8")
		head = b""
		for header in self.headers:
			head += f"\r\n{header}: {self.headers[header]}".encode("utf-8")

		output = status
		if head:
			output += head
		output += b"\r\n\r\n"+self.data

		return output
	
	@classmethod
	def make(cls, *args, **kwargs):
		return cls(*args, **kwargs).build()