from decorators import Module
from .user_controller import UserController
from src.management.management_module import ManagementModule
from .user_service import UserService 

@Module(
    imports= [ManagementModule],
    controllers=[UserController],
    providers=[UserService]
)
class UserModule:
    pass  
