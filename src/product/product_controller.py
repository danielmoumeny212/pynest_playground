from controller import Controller, Get, Post, Depends
from event.decorateur import OnEvent
from .product_service import ProductService
from .product_model import Product


@Controller("product")
class ProductController:
    

    service: ProductService = Depends(ProductService)
    
    @OnEvent("send.email")
    def send_email(self):
          print ("Sending email")
    
    @Get("/")
    def get_product(self):
        return self.service.get_product()
        
    @Post("/")
    def add_product(self, product: Product):
        return self.service.add_product(product)

