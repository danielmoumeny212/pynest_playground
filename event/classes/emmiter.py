# """Event emitter mixin class."""
from functools import lru_cache
from decorators import Injectable

@Injectable
class EventEmitter:
    _instance = None  
    
    def __new__(cls):
      if cls._instance is None:
        cls._instance = super(EventEmitter, cls).__new__(cls)
      return cls._instance
  
    def __init__(self):
        self._listeners = {}
    

    def on(self, event_type:str, callback):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)

    def emit(self, event_type:str, *args, **kwargs):
        print(self._listeners[event_type])
        if event_type in self._listeners.keys():
            for callback in self._listeners[event_type]:
                callback(*args, **kwargs)

    def remove_listener(self, event_type: str, callback):
        if event_type in self._listeners:
            self._listeners[event_type].remove(callback)

    def remove_all_listeners(self, event_type=None):
        if event_type is not None:
            del self._listeners[event_type]
        else:
            self._listeners = {}
            
