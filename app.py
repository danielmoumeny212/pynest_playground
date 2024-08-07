from pynest_factory import PyNestFactory
from decorators import Module
from src.user.user_module  import UserModule
from src.product.product_module import ProductModule
from src.management.management_module import ManagementModule
from app_controller import AppController
from event.event_module import EventEmitterModule
from event.classes.emmiter import EventEmitter
from ioc import analyse_constructor
from fastapi.responses import JSONResponse
import asyncio 
@Module(
    imports=[UserModule, ManagementModule, ProductModule, EventEmitterModule],
    controllers=[AppController]
)
class AppModule(): 
    pass 


app = PyNestFactory.create( 
    AppModule,
    description="This is my FastAPI app.", 
    title="My App", 
    version="1.0.0",
    debug=True)
http_server = app.get_server()
userModule = app.select(UserModule)
 

