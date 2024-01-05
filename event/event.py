
class Event(list):
    def __call__(self, *args ,**kwds):
      for item in self: 
        item(*args, **kwds)