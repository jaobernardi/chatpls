import events
from structures import Response, Config
from tasks import thread_function
import time
import socket

config = Config()
global rates
global timeouts
global clean_time
rates = {}
timeouts = {}
clean_time = time.time() + 10


@events.add_handle("http_request", priority=100)
def analizer_http(event):
	request = event.request
	path = [i.lower() for i in request.path.split("/")[1:] if i]
	event.add_property(path=path)
	event.add_property(default_headers={"X-Server": 'chatpls/1.0', 'X-Backend': socket.gethostname()})
	
@events.add_handle("http_request", priority=-1)
def fallback_http(event):
	request = event.request
	default_headers = {
		"Server": "chatpls/1.0",
	}
	return Response.make(
		200,
		'OK',
		default_headers,
		f"If you're reading this, you fucked up.\nHeaders: {request.headers}\nQuery string: {request.query_string}\nData: {request.data}".encode()
	)


