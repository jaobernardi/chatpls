class EventResponse(object):
	"""
	This class powers the event module.

	...

	Attributes
	----------
	cancelled : bool, False
		expresses if this event has already been declared cancelled.
	
	responsable : bool, True
		expresses if the event can recieve any responses

	* This class will dynamically add new attributes according to calling event needs
	"""
	def __init__(self, cancellable = False, responsable = True, **kwargs):
		"""
		Parameters
		----------
		cancellable : bool, optional
			defines if the event can be cancelled        
		"""
		self._cancellable = cancellable
		self._cancelled = False
		self.__dict__ = self.__dict__ | kwargs
		self._response = None
		self.responsable = responsable
	
	@property
	def response(self):
		return self._response
	
	@response.setter
	def response(self, new):
		if not self.responsable:
			raise EventDosentSuppotResponse("This event does not support response setting.")
		self._response = new

	@property   
	def cancelled(self):
		return self._cancelled
	
	@cancelled.setter
	def cancelled(self, new: bool):
		if not self._cancellable:
			raise EventNotCancellable("This event cannot be cancelled.")
		self._cancelled = new


class RelativeJsonFile(object):
	"""
	This class interfaces input and output to json files.
	(Ported from version 4.0.0)
	"""
	def __init__(self, input):
		self.file = input
		with open(f"{input}", encoding="utf-8") as file:
			object.__setattr__(self, "_data", json.load(file))

	def __getattribute__(self, name):
		_data = object.__getattribute__(self, "_data")
		if name in _data:
			return _data[name]
		return object.__getattribute__(self, name)

	def __enter__(self):
		return self

	def __exit__(self, *args, **kwargs):
		self.flush()

	def flush(self):
		with open(f"{self.file}", "w", encoding="utf-8") as file:
			json.dump(object.__getattribute__(self, "_data"),
					  file, indent=4, ensure_ascii=False)

class Config(RelativeJsonFile):
	"""
	Represents the config file.
	"""
	def __init__(self):
		super().__init__("config.json")
