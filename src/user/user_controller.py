from controller import Controller, Get, Post, Depends
from decorators import HttpCode 

from event.decorateur import OnEvent
from .user_service import UserService
from fastapi import status 
from .user_model import User


@Controller("user")
class UserController:

    service: UserService = Depends(UserService)
    
    @Get("/all")
    def get_user(self):
        return self.service.get_user()
    
    @OnEvent("user.added")
    def user_added(self):
        print("User added")
        
    @Post(status_code=200)
    @HttpCode(status.HTTP_201_CREATED)
    def add_user(self, user: User):
        return self.service.add_user(user)

