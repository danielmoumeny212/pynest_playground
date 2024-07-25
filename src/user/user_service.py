from event.classes.emmiter import EventEmitter
from exception import BadRequestException
from .user_model import User
from functools import lru_cache
from decorators import Injectable
from  controller import Depends
@lru_cache()
@Injectable
class UserService:
      
    def __init__(self):
        self.database = []

    def get_user(self):
        raise BadRequestException("erreur")
        
        # return self.database

    def add_user(self, user: User):
        self.database.append(user)
        
        return user
