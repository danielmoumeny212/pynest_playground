from pynest_factory import PyNestFactory
from decorators import Module
from src.user.user_module  import UserModule
from src.product.product_module import ProductModule
from src.management.management_module import ManagementModule
from app_controller import AppController
from event.emmiter import EventEmitter

@Module(
    imports=[UserModule, ManagementModule, ProductModule],
    controllers=[AppController]
)
class AppModule(): 
    pass 
value  = { "touche": False}
def touch_value():
    """Flip the test bit to True."""
    value['touched'] = True
    print(value)
    
    
event = EventEmitter()

event.on("touch_value", touch_value)

app = PyNestFactory.create( 
    AppModule,
    description="This is my FastAPI app.", 
    title="My App", 
    version="1.0.0",
    debug=True)
http_server = app.get_server()

userModule = app.select(UserModule)
@http_server.get("/hello")
def hello():
     return "Hello, world!"
 

