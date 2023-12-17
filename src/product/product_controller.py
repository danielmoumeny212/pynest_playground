from fastapi import Depends 
from .product_service import ProductService 
from controller import Controller , Get

@Controller("products")
class ProductsController:
    
    def __init__(self,product_service: ProductService = Depends(ProductService)):
          self.product_service = product_service
    
    @Get("/get_products")
    def get_products(self):
        return self.product_service.get_product()
     
    @Get("/users")
    def get_user(self): 
        return self.user_service.get_user()
 