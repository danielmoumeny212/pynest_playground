from controller import Controller, Get
from exception import BadRequestException

@Controller("app")
class AppController:
    
    @Get("/")
    def index(self):
    
      return "app"
    
