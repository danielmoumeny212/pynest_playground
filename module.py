import hashlib
import random
import string
import string
from typing import List
from uuid import uuid4
from typing import Any, Type, Union


class ModulesContainer(dict):
    def __init__(self):
        super().__init__()
        self._application_id = str(uuid4().hex)

    @property
    def application_id(self):
        return self._application_id

    def get_by_id(self, module_id):
        return next((module for module in self.values() if module.id == module_id), None)
    
    def has(self, token: str): 
        return  True if self.get(token) is not None else False


class Module:
    def __init__(self, metatype, container):
        self._id = str(uuid4().hex)
        self._metatype = metatype
        self.container = container
        self._imports = set()
        self._providers = {}
        self._injectables = {}
        self._middlewares = {}
        self._controllers = {}
        self._entryProviderKeys = set()
        self._exports = set()
        self._distance = 0
        self._token = None

    @property
    def id(self):
        return self._id

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token):
        self._token = token

    @property
    def name(self):
        return self._metatype.__name__


    @property
    def providers(self):
        return self._providers

    @property
    def middlewares(self):
        return self._middlewares

    @property
    def imports(self):
        return self._imports

    @property
    def injectables(self):
        return self._injectables

    @property
    def controllers(self):
        return self._controllers

    @property
    def entryProviders(self):
        return [self._providers[token] for token in self._entryProviderKeys]

    @property
    def exports(self):
        return self._exports

    @property
    def instance(self):
        if self._metatype not in self._providers:
            raise Exception("RuntimeException")
        module = self._providers[self._metatype]
        return module.instance

    @property
    def metatype(self):
        return self._metatype

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, value):
        self._distance = value
    
    def add_import(self, moduleRef): 
        self._imports.add(moduleRef);
    
    def add_imports(self, module_ref: List[Any]):
          for module in module_ref:
              self.add_import(module)
        
        
    def add_provider(self, provider) -> str: 
         self._providers[provider.__name__] = provider;
         return provider.__name__;
    
    def add_controller(self, controller) -> str: 
         self._controllers[controller.__name__] = controller
         return controller.__name__
  

    def add_exported_provider(self, provider):
        def add_exported_unit(token):
            self._exports.add(self._validate_exported_provider(token))

        if self._is_custom_provider(provider):
            return self._add_custom_exported_provider(provider)
        elif isinstance(provider, (str, type)):
            return add_exported_unit(provider)
        elif self._is_dynamic_module(provider):
            module_class_ref = provider.module
            return add_exported_unit(module_class_ref)
        add_exported_unit(provider)

    def _add_custom_exported_provider(self, provider):
        provide = provider.provide
        if isinstance(provide, (str, type)):
            return self._exports.add(self._validate_exported_provider(provide))
        self._exports.add(self._validate_exported_provider(provide))

    def _validate_exported_provider(self, token):
        if token in self._providers:
            return token
        imports = [imp.metatype for imp in self._imports if imp]
        if token not in imports:
            provider_name = token.__name__ if callable(token) else str(token)
            raise Exception(provider_name, self._metatype.__name__)
        return token

    def _is_custom_provider(self, provider):
        return hasattr(provider, 'provide') and provider.provide is not None

    def _is_dynamic_module(self, exported):
        return bool(exported and getattr(exported, 'module', None))

    def _add_custom_provider(self, provider, collection, enhancer_subtype=None):
        if self._is_custom_class(provider):
            return self._add_custom_class(provider, collection, enhancer_subtype)
        elif self._is_custom_value(provider):
            return self._add_custom_value(provider, collection, enhancer_subtype)
        elif self._is_custom_factory(provider):
            return self._add_custom_factory(provider, collection, enhancer_subtype)
        elif self._is_custom_use_existing(provider):
            return self._add_custom_use_existing(provider, collection, enhancer_subtype)
        return provider.provide

    def _is_custom_class(self, provider):
        return hasattr(provider, 'useClass') and provider.useClass is not None

    def _is_custom_value(self, provider):
        return isinstance(provider, dict) and 'useValue' in provider

    def _is_custom_factory(self, provider):
        return hasattr(provider, 'useFactory') and provider.useFactory is not None

    def _is_custom_use_existing(self, provider):
        return hasattr(provider, 'useExisting') and provider.useExisting is not None

    def _add_custom_class(self, provider, collection, enhancer_subtype=None):
        scope = provider.scope if hasattr(provider, 'scope') else None
        durable = provider.durable if hasattr(provider, 'durable') else None
        use_class = provider.useClass
        if scope is None:
            scope = self._get_class_scope(use_class)
        if durable is None:
            durable = self._is_durable(use_class)
        token = provider.provide
        collection[token] = {
            'token': token,
            'name': use_class.__name__ if callable(use_class) else use_class,
            'metatype': use_class,
            'instance': None,
            'isResolved': False,
        }
 

class ModuleTokenFactory:
    def __init__(self):
        self.module_token_cache = {}
        self.module_ids_cache = {}

    def create(self, metatype, dynamic_module_metadata=None) -> str:
        module_id = self.get_module_id(metatype)

        if dynamic_module_metadata is None:
            return self.get_static_module_token(module_id, self.get_module_name(metatype))

        opaque_token = {
            "id": module_id,
            "module": self.get_module_name(metatype),
            "dynamic": dynamic_module_metadata,
        }
        opaque_token_string = self.stringify_opaque_token(opaque_token)

        return self.hash_string(opaque_token_string)

    def get_static_module_token(self, module_id, module_name):
        key = f"{module_id}_{module_name}"
        if key in self.module_token_cache:
            return self.module_token_cache[key]

        hash_value = self.hash_string(key)
        self.module_token_cache[key] = hash_value
        return hash_value

    def stringify_opaque_token(self, opaque_token):
        return str(opaque_token)

    def get_module_id(self, metatype):
        if metatype in self.module_ids_cache:
            return self.module_ids_cache[metatype]

        module_id = self.random_string_generator()
        self.module_ids_cache[metatype] = module_id
        return module_id

    def get_module_name(self, metatype):
        return metatype.__name__

    def random_string_generator(self, length=10):
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))

    def hash_string(self, value):
        return hashlib.sha256(value.encode()).hexdigest()



class ModuleFactory:
    def __init__(self, type: Type[Any], token: str, dynamic_metadata: dict = None):
        self.type = type
        self.token = token
        self.dynamic_metadata = dynamic_metadata

class ModuleCompiler:
    def __init__(self, module_token_factory: ModuleTokenFactory = ModuleTokenFactory()):
        self.module_token_factory = module_token_factory

    def compile(self, metatype: Type[Any]):
        metadata = self.extract_metadata(metatype)
        module_type = metadata["type"]
        dynamic_metadata = metadata["dynamic_metadata"]
        token = self.module_token_factory.create(module_type, dynamic_metadata)
        return ModuleFactory(module_type, token, dynamic_metadata)

    def extract_metadata(self, metatype) -> dict:
       metadata = {}
       metadata["type"] = metatype
       metadata["dynamic_metadata"] = {}
       
       if not self.has_module_metadata(metatype): 
            raise Exception(f"{metatype.__name__} as no metadata found")
       for props in  ["imports", 'providers', "controllers"]: 
          metadata["dynamic_metadata"][props]  = getattr(metatype, props, [])
       return metadata
    
    def has_module_metadata(self, metatype):
       for props in  ["imports", 'providers', "controllers"]: 
           if  hasattr(metatype, props):
                return True 
       else : 
           return False 
   