import events
from structures import Response, Config
from tasks import thread_function
import time

config = Config()
global rates
global timeouts
global clean_time
rates = {}
timeouts = {}
clean_time = time.time() + 10


@events.add_handle("http_request", priority=100)
def analizer_http(event):
	print(globals()["rates"])
	print(globals()["clean_time"]-time.time())
	print(globals()['timeouts'])
	request = event.request
	path = [i.lower() for i in request.path.split("/")[1:] if i]
	event.add_property(path=path)

	if globals()['clean_time'] <= time.time():
		globals()["rates"] = {}
		globals()['clean_time'] = time.time() + 10

	if event.address[0] not in globals()["rates"]:
		globals()["rates"][event.address[0]] = 0
	globals()["rates"][event.address[0]] += 1
	if globals()["rates"][event.address[0]] > 10:
		globals()['timeouts'][event.address[0]] = time.time()+1
	
	if event.address[0] in globals()['timeouts'] and globals()['timeouts'][event.address[0]] >= time.time():
		return Response.make(
			429,
			'Too Many Requests',
			{"Server": "chatpls/1.0"},
			b"Error: 429 (Too Many Requests)"
		)
	elif event.address[0] in globals()['timeouts'] and globals()['timeouts'][event.address[0]] < time.time():
		globals()['timeouts'].pop(event.address[0])
	
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


