from controller import Controller, Get, Post, Depends
from decorators import HttpCode 

from event.decorateur import OnEvent
from .user_service import UserService
from fastapi import status 
from .user_model import User
from event.classes.emmiter import EventEmitter 

@Controller("user")
class UserController:

    service: UserService = Depends(UserService)

    
    @Get("/all")
    def get_user(self):
        return self.service.get_user()
    
    @OnEvent("user.added")
    def user_added(self, message):
        print("User added", message)
        
    @Post()
    @HttpCode(status.HTTP_201_CREATED)
    def add_user(self, user: User):
        return self.service.add_user(user)

