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
		print("Cleaning")	
		rates = {}
		time.sleep(2)

@events.add_handle("http_request", priority=100)
def analizer_http(event):
	print(rates)
	request = event.request
	path = [i.lower() for i in request.path.split("/")[1:] if i]
	event.add_property(path=path)
	if event.address[0] not in rates:
		rates[event.address[0]] = 0
	rates[event.address[0]] += 1
	if rates[event.address[0]] > 10:
		timeouts[event.address[0]] = time.time()+60
	
	if event.address[0] in timeouts and timeouts[event.address[0]] >= time.time():
		return Response.make(
			429,
			'Too Many Requests',
			{"Server": "chatpls/1.0"},
			b"Error: 429 (Too Many Requests)"
		)
	elif event.address[0] in timeouts and timeouts[event.address[0]] < time.time():
		timeouts.remove(event.address[0])
	
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


