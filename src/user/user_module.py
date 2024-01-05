from .user_controller import UserController
from .user_service import UserService
from decorators import Module 

@Module(
    controllers=[UserController],
    providers=[UserService],
    imports=[]
)
class UserModule:
    pass
