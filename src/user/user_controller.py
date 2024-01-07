from controller import Controller, Get, Post, Depends

from event.decorateur import OnEvent
from .user_service import UserService
from .user_model import User
from event.classes.emmiter import EventEmitter


@Controller("user")
class UserController:
    emitter: EventEmitter  = Depends(EventEmitter)
   
    service: UserService = Depends(UserService)
    
    @Get()
    def get_user(self):
        return self.service.get_user()
    
    @OnEvent("user.added")
    def user_added(self):
        print("User added")
        
    @Post()
    def add_user(self, user: User):
        self.emitter.emit("user.added")
        return self.service.add_user(user)

