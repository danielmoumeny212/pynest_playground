from fastapi import FastAPI , HTTPException
from abc import abstractmethod, ABC
from pynest_app_context import PyNestApplicationContext
from typing import Any, Dict, List, Union
from collections import defaultdict
from pynest_container import PyNestContainer
from router_resolver import RoutesResolver

class DependencyGraph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.visited = set()
        self.recursion_stack = set()

    def add_dependency(self, module, dependency):
        self.graph[module].append(dependency)

    def has_circular_dependency(self, module):
        if module not in self.visited:
            self.visited.add(module)
            self.recursion_stack.add(module)

            for dependency in self.graph[module]:
                if dependency not in self.visited:
                    if self.has_circular_dependency(dependency):
                        return True
                elif dependency in self.recursion_stack:
                    return True

            self.recursion_stack.remove(module)
        return False

class AbstractPyNestApp(ABC):
    
    @abstractmethod
    def use (self, middleware_class: type, **options: Any) -> None: 
      pass 
    
  
    
class PyNestApp(PyNestApplicationContext):
    _is_listening = False
    
    @property
    def is_listening(self):
        self._is_listening 
        
    def __init__(self,
                 container: PyNestContainer,
                 http_server: FastAPI
                 ):
        self._container = container
        self._http_adaptater = http_server
        super().__init__(self._container)
        self.routes_resolver = RoutesResolver(self._container, self._http_adaptater)
        self.select_context_module()
        self._register_routes()
             
        
    def use (self, middleware: type, **options: Any) -> None: 
        self._http_adaptater.add_middleware(middleware, **options)
        return self 
    
    def get_server(self): 
        return self._http_adaptater
    

    def enable_cors(self, options: Dict[str, Union[str, bool, List[str]]]):
        """
        Configure Cross-Origin Resource Sharing (CORS) for the HTTP server.

        :param options: A dictionary containing the CORS configuration options.
        :type options: Dict[str, Union[str, bool, List[str]]]

        :raises ValueError: If an unexpected key is passed in the `options` dictionary.
        :Expected keys: allow_origins, allow_credentials, allow_headers, allow_methods

        Example usage:
        >>> cors_options = {
        ...     "allow_origins": ["example.com", "test.com"],
        ...     "allow_credentials": True,
        ...     "allow_methods": ["GET", "POST"],
        ...     "allow_headers": ["Content-Type", "Authorization"]
        ... }
        """
        from fastapi.middleware.cors import CORSMiddleware

        # Define the expected keys
        expected_keys = ["allow_origins", "allow_credentials", "allow_methods", "allow_headers"]

        # Check for unexpected keys
        unexpected_keys = [key for key in options if key not in expected_keys]
        if unexpected_keys:
            raise ValueError(f"Unexpected keys in options: {unexpected_keys}")

        # Extract options
        allow_origins = options.get("allow_origins", [])
        allow_credentials = options.get("allow_credentials", True)
        allow_methods = options.get("allow_methods", ["*"])
        allow_headers = options.get("allow_headers", ["*"])

        # Configure CORS using CORSMiddleware
        cors_middleware = CORSMiddleware(
            allow_origins=allow_origins,
            allow_credentials=allow_credentials,
            allow_methods=allow_methods,
            allow_headers=allow_headers,
        )

        self._http_adaptater.add_middleware(cors_middleware)

        
    def _register_routes(self):
          self.routes_resolver.register_routes()
          if self._http_adaptater.debug: 
               self.routes_resolver.not_found_handler()
               
      
    def global_prefix(self, prefix: str): 
         self._http_adaptater.prefix = prefix 
        
        