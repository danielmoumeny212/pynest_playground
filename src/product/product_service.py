from controller import Depends
from event.decorateur import OnEvent
from event.classes.emmiter import EventEmitter
from .product_model import Product
from functools import lru_cache
from decorators import Injectable

@lru_cache()
@Injectable
class ProductService:
    emitter = Depends(EventEmitter)

    def __init__(self):
        self.database = []
        
    def get_product(self):
        return self.database
    
    def add_product(self, product: Product):
        self.database.append(product)
        self.emitter.emit("product.added")
        return product
    
    @OnEvent("product.added")
    def product_added(self): 
        print ("Product added")
        
        
