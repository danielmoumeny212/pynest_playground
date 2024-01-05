from module import ModulesContainer
from module import ModuleCompiler, ModuleTokenFactory, ModuleFactory, Module
from exceptions import UnknownModuleException, CircularDependencyException, NoneInjectableException
from constants import INJECTABLE_TOKEN, MODULE_METADATA_PARAMS, CONTROLLERS_TOKEN, PROVIDER_TOKEN, IMPORTS_TOKEN
from typing import List , Any, Dict 
from logger import Logger
import click

class PyNestContainer: 
   _instance = None 
   
   
    
   def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PyNestContainer, cls).__new__(cls)
        return cls._instance

   def __init__(self):
      self.logger =  Logger(self.__class__.__name__)
    
   _global_modules = set()
   _modules = ModulesContainer()
   _module_token_factory = ModuleTokenFactory()
   _module_compiler =  ModuleCompiler(_module_token_factory)
   _modules_metadata  = {}
   
   @property
   def modules(self):
        return self._modules
    
   @property
   def module_token_factory(self): 
        return self._module_token_factory
   @property
   def modules_metadata(self):
        return self._modules_metadata
   
   
   @property
   def module_compiler(self):
       return self._module_compiler
   
   def get_module_by_key(self, module_key: str) ->Module:
        return self._modules[module_key]
       
   
   def add_module(self, metaclass):
        module_factory = self._module_compiler.compile(metaclass)
        token = module_factory.token 
        if self._modules.has(token):
             return {"module_ref": self.modules.get(token), "inserted": True}
        return {"module_ref": self.set_module(module_factory), "inserted":False}
    
   def add_related_module(self, related_module, token: str):
         if not self.modules.has(token):
             return; 
         module_ref = self.modules.get(token)
         related_mod = self.module_compiler.compile(related_module)
         related = self.modules.get(related_mod.token)
         module_ref.add_import(related)
         
    
  
   def _get_controllers(self, token: str): 
           module_metadata = self.modules_metadata[token]
           controllers = self.extract_module_param_metadata(module_metadata,CONTROLLERS_TOKEN)
           return controllers
      
   def _get_providers(self, token: str): 
           module_metadata = self.get_module_metadata(token)
           providers = self.extract_module_param_metadata(module_metadata,PROVIDER_TOKEN)
           return providers
    
   def add_providers(self, providers: List[Any], module_token: str):
           for provider in providers:
                self.add_provider(module_token, provider)
                
   def add_controllers(self, controllers: List[Any], module_token: str): 
         for controller in controllers: 
              self.add_controller(module_token, controller)
              
   def add_controller(self, token: str, controller):
         if not self.modules.has(token):
               raise UnknownModuleException()
         module_ref: Module = self.modules[token]
         module_ref.add_controller(controller)         
      
  
   def set_module(self, module_factory: ModuleFactory)-> Module: 
        module_ref =  Module(module_factory.type, self)
        module_ref.token =  module_factory.token
        module_token = module_factory.token
        self._modules[module_factory.token] = module_ref
        self.add_metadata(module_token, module_factory.dynamic_metadata)
        self.add_import(module_token)
        self.add_controllers(self._get_controllers(module_token), module_token)
        self.add_providers(self._get_providers(module_token), module_token)      
        self.logger.info(f"{click.style( module_factory.type.__name__ + ' Detected ', fg='green')}" ,)        
        return module_ref
   
   def add_metadata(self, token: str, module_metadata):
         if not module_metadata: 
              return 
         self._modules_metadata[token] = module_metadata
   
   def add_modules(self, modules: List[Any]):
          if not modules: 
               return 
          for module in modules:
               self.add_module(module)
               
   def add_import(self, token: str):
          if not self.modules.has(token): 
               return ;
          module_metadata: Dict[str, List] = self.get_module_metadata(token)
          module_ref: Module = self.get_module_ref(token)
          imports_mod: List[Any] = self.extract_module_param_metadata(module_metadata,IMPORTS_TOKEN)
          self.add_modules(imports_mod)
          module_ref.add_imports(imports_mod)
          
   
   def get_module_ref(self, token: str) -> Module:
          module_ref: Module = self.modules.get(token)
          return module_ref 
   
   def extract_module_param_metadata(self, module_metadata: Dict[str, List] , params_name: str): 
           if not params_name in MODULE_METADATA_PARAMS:
                raise Exception("Invalid module metadata parameter")
           return module_metadata.get(params_name)
      
           
   def get_module_metadata(self, token: str):
          module_metadata = self._modules_metadata.get(token)
          if module_metadata is None:
                 raise Exception("No module metadata Found ")
          return module_metadata 

   def add_provider(self, token: str, provider): 
        module_ref:Module = self.modules[token]
        if not provider: 
             raise CircularDependencyException(module_ref.metatype)
        
        if not module_ref: 
             raise UnknownModuleException()
        if not hasattr(provider, INJECTABLE_TOKEN):
          error_message = f"""
               {click.style(provider.__name__, fg='red')} is not injectable. 
               To make {provider.__name__} injectable, apply the {click.style("@Injectable decorator", fg='green')} to the class definition. 
               or remove {click.style(provider.__name__, fg='red')} from the provider array of the Module class. 
               Please check your code and ensure that the decorator is correctly applied to the class.
          """
          raise NoneInjectableException(error_message)

        module_ref.add_provider(provider)
        
   def clear (self): 
        self.modules.clear() 
        