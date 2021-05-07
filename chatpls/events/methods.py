from structures.wrappers import EventResponse

events = {}
super_handles = []

def create_event(event_name):
	events[event_name] = {}

def super_handle(function):
	super_handles.append(function)

def add_handle(event_name, priority=0, function=None):
	def wrapper(function):
		if event_name not in events:
			create_event(event_name)

		if priority not in events[event_name]:
			events[event_name][priority] = []

		events[event_name][priority].append(function)
	if not function:
		return wrapper
	wrapper(function)


def call_event(event_name, cancellable=False, event_field=None, **kwargs):
	event_field = event_field or events
	if not event_name in event_field:
		create_event(event_name)

	order = list(event_field[event_name])
	order.sort()
	order.reverse()

	event = EventResponse(cancellable=cancellable, **kwargs)

	for handle in super_handles:
		if event.cancelled:
			return event
		event.response = handle(event_name, event)

	for priority in order:
		for handle in event_field[event_name][priority]:
			if event.cancelled:
				return event
			event.response = handle(event)
	return event
