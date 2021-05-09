import events
from structures import Response, Config
from tasks import thread_function
import time

config = Config()
rates = {}
timeouts = {}

@events.add_handle("startup")
@thread_function
def rate_reset(event):
	while True:
		rates = {}
		time.sleep(10)

@events.add_handle("http_request", priority=100)
def analizer_http(event):
	request = event.request
	path = [i.lower() for i in request.path.split("/")[1:] if i]
	event.add_property(path=path)
	if event.address not in rates:
		rates[event.address] = 0
	rates[event.address] += 1
	if rates[event.address] > 10:
		timeouts[event.address] = time.time()+60
	
	if event.address in timeouts and timeouts[event.address] >= time():
		return Response.make(
			429,
			'Too Many Requests',
			{"Server": "chatpls/1.0"},
			b"Error: 429 (Too Many Requests)"
		)
	elif event.address in timeouts and timeouts[event.address] < time():
		timeouts.remove(event.address)
	
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


