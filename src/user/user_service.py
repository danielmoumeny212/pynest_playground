from decorators import Injectable 

@Injectable
class UserService: 
    
      
    def __init__(self, name):
       pass 
    
    def get_user(self):
        return {"user_name": "manasse", "password": "manasse"}
    