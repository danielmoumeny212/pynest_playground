from pynest_container import PyNestContainer
from fastapi import FastAPI, HTTPException, Request
from fastapi.routing import APIRouter
from logger import Logger

class RoutesResolver: 
  
  def __init__(self, container: PyNestContainer, http_adaptater: FastAPI):
        self.container = container 
        self.http_adaptater = http_adaptater
        self.logger =  Logger(self.__class__.__name__)
        
  
  def register_routes(self): 
    for module in self.container.modules.values(): 
      for controller in module.controllers.values(): 
        self.register_route(controller)

  def register_route(self, controller): 
    router: APIRouter = controller.get_router()
    self.http_adaptater.include_router(router)
  
     
  def route_not_found_exception_handler(self, request, exc):
    from fastapi.responses import JSONResponse

    available_routes = []
    for route in self.http_adaptater.routes:
        if hasattr(route, "path"):
            available_routes.append("{} -> {}".format(route.path.split('/')[0], route.path))
    error_message = "Route not found. Available routes:\n{}".format(",\n".join(available_routes))
    response_content = {
        "detail": error_message,
        "status_code": exc.status_code,
    }
    return JSONResponse(content=response_content, status_code=exc.status_code)


  
  def not_found_handler(self): 
        self.http_adaptater.add_exception_handler(404,self.route_not_found_exception_handler)
    