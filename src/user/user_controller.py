from controller import Controller, Get, Post, Depends
from decorators import HttpCode 

from event.decorateur import OnEvent
from .user_service import UserService
from .user_model import User
from event.classes.emmiter import EventEmitter 

@Controller("users")
class UserController:

    service: UserService = Depends(UserService)

    @Get(['/all', "/mange"])
    def get_user(self):
        return self.service.get_user()
    
    @OnEvent("user.added")
    def user_added(self, message):
        print("User added", message)
        
    @HttpCode(201)
    @Post()
    def add_user(self, user: User):
        return self.service.add_user(user)
    
    

