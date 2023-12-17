from controller import Controller, Get

@Controller("management")
class ManagementController:
    
    @Get("/get")
    def management(self):
        return self.product_service.get_product()