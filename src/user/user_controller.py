from controller import Controller, Get 
from decorators import Inject
from fastapi import Depends
from src.user.user_service import UserService

@Controller("users")
class UserController:
     
     def __init__(self, user_service: UserService):
              pass
     
     @Get('/me')
     def me(self):
         return self.user_service.get_user()  
     