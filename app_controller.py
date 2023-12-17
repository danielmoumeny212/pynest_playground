from controller import Controller, Get

@Controller("app")
class AppController:
    
    @Get("/")
    def index(self): 
        return "Hello, world!"
    
