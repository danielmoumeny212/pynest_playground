from decorators import Module 
from .management_controller import ManagementController 
from src.product.product_service import ProductService

@Module(
    providers=[ProductService],
    controllers=[ManagementController],
    imports=[],
    exports=[]
)
class ManagementModule: 
     pass 