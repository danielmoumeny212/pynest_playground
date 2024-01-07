from event.classes.emmiter import EventEmitter

value  = { "touched": False}
def touch_value():
    """Flip the test bit to True."""
    value['touched'] = True
    print(value)
    
event = EventEmitter()

event.on("touch_value", touch_value)