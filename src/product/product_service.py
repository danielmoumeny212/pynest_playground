from decorators import Injectable 

@Injectable
class ProductService: 
    
    def get_product(self):
        return {"product_name": "mon article", "price": 100}
