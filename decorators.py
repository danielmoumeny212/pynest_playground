from ioc import get_di_container
from typing import Type, Union, TypeVar, List
from constants import ModuleMetadata, INJECTABLE_TOKEN 
class Module:
    def __init__(self, imports = None , controllers=None, providers=None, exports=None):
        self.controllers = controllers or []
        self.providers = providers or []
        self.imports = imports or []
        self.exports = exports

    def __call__(self, cls):
        setattr(cls,ModuleMetadata.CONTROLLERS.value, self.controllers)
        setattr(cls,ModuleMetadata.PROVIDER.value, self.providers)
        setattr(cls, ModuleMetadata.IMPORT.value, self.imports)
        setattr(cls, ModuleMetadata.EXPORTS.value, self.exports)
        return cls
      

def Injectable(cls):
    setattr(cls, INJECTABLE_TOKEN, True)
    return cls

  
class Inject:
    def __init__(self, service_class: Type):
        self.service_class = service_class

    def __call__(self, cls):
        def new_instance(cls, *args, **kwargs):
            container = get_di_container()
            service_instance = container.get_service(self.service_class)
            if service_instance is None:
                raise Exception(f"Service not found for {self.service_class}")
            instance = super(cls, cls).__new__(cls)
            class_name = self.service_class.__name__
            service_key = "".join([char if char.islower() else f"_{char.lower()}" for char in class_name])
            service_name = service_key.lstrip("_")
            setattr(instance, service_name, service_instance)
            return instance

        cls.__new__ = new_instance
        return cls

class Inject:
    def __init__(self, service_classes):
        self.service_classes = service_classes

    def __call__(self, cls):
        def new_instance(*args, **kwargs):
            container = get_di_container()
            dependencies = {}
            for service_class in self.service_classes:
                service_instance = container.get_service(service_class)
                if service_instance is None:
                    raise Exception(f"Service not found for {service_class}")
                class_name = service_class.__name__
                service_key = "".join([char if char.islower() else f"_{char.lower()}" for char in class_name])
                service_name = service_key.lstrip("_")
                dependencies[service_name] = service_instance
            instance = super(cls, cls).__new__(cls)
            for key, value in dependencies.items():
               setattr(instance, key, value)
            
            return instance

        cls.__new__ = new_instance
        return cls


from fastapi.exceptions import HTTPException
import logging
import time

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def db_request_handler(func):
    """
    Decorator that handles database requests, including error handling and session management.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The decorated function.
    """

    def wrapper(self, *args, **kwargs):
        try:
            s = time.time()
            result = func(self, *args, **kwargs)
            p_time = time.time() - s
            logging.info(f"request finished after {p_time}")
            if hasattr(self, "session"):
                # Check if self is an instance of OrmService
                self.session.close()
            return result
        except Exception as e:
            logging.error(e)
            if hasattr(self, "session"):
                # Check if self is an instance of OrmService
                self.session.rollback()
                self.session.close()
            return HTTPException(status_code=500, detail=str(e))

    return wrapper
