from decorators import Module
from event.classes.emmiter import EventEmitter


@Module(
  imports=[],
  providers=[EventEmitter],
  exports=[EventEmitter]
)
class EventEmitterModule: 
   pass 
