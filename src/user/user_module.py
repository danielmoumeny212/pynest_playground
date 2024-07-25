from src.management.management_module import ManagementModule
from .user_controller import UserController
from .user_service import UserService
from decorators import Module 

@Module(
    controllers=[UserController],
    providers=[UserService],
    imports=[ManagementModule], 
    exports=[],
)
class UserModule:
    
    def __init__(self, hello: str) -> None:
        pass
