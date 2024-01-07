from .product_controller import ProductController
from .product_service import ProductService
from decorators import Module 



@Module(
    controllers=[ProductController],
    providers=[ProductService],
    imports=[], 
    exports=[]
)
class ProductModule:
    pass
