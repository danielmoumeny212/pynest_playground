from fastapi.routing import APIRouter
from helpers import class_based_view as ClassBasedView
from constants import STATUS_CODE_TOKEN
from fastapi import Depends, status 
from typing import Callable, Any, Union, List
from typing import Optional, Union, List
from fastapi import APIRouter

def Controller(tag: str = None, prefix: Optional[Union[str, List[str]]] = None):
    """
    Decorator that turns a class into a controller, allowing you to define routes using FastAPI decorators.

    Args:
        tag (str, optional): The tag to use for OpenAPI documentation.
        prefix (Optional[Union[str, List[str]]]): The prefix or list of prefixes to use for all routes.

    Returns:
        class: The decorated class.
    """
    # Use tag as default prefix if prefix is None
    prefixes = [tag] if tag and prefix is None  else []

    if prefix:
        prefixes.extend(prefix) if isinstance(prefix, list) else [prefix]

    def wrapper(cls) -> ClassBasedView:
        router = APIRouter(tags=prefixes)
        setattr(cls, "prefixes", prefixes)

        http_method_names = ("GET", "POST", "PUT", "DELETE", "PATCH")

        generated_routes = set()

        for name, method in cls.__dict__.items():
            if callable(method) and hasattr(method, "method"):
                # Check if method is decorated with an HTTP method decorator
                assert hasattr(method, "__path__") and method.__path__, f"Missing path for method {name}"

                http_method = method.method
                # Ensure that the method is a valid HTTP method
                assert http_method in http_method_names, f"Invalid method {http_method}"

                # Process single path or list of paths
                paths = method.__path__ if isinstance(method.__path__, list) else [method.__path__]

                for path in paths:
                    if prefixes and isinstance(path, str):
                        for prefix in prefixes:
                            combined_path = f"/{prefix.rstrip('/')}/{path.lstrip('/')}"

                            # Check if the route has already been generated to avoid duplicates
                            if combined_path not in generated_routes:
                                if  hasattr(method, STATUS_CODE_TOKEN) and method.__kwargs__.get(STATUS_CODE_TOKEN) is None:
                                    method.__kwargs__[STATUS_CODE_TOKEN] = method.__dict__[STATUS_CODE_TOKEN]
                            router.add_api_route(combined_path, method,methods=[http_method], **method.__kwargs__)
                            generated_routes.add(combined_path)
                            print(generated_routes)

        def get_router() -> APIRouter:
            """
            Returns:
                APIRouter: The router associated with the controller.
            """
            return router

        cls.get_router = get_router

        return ClassBasedView(router=router, cls=cls)

    return wrapper





from typing import Union, List

def route(method: str, path: Union[str, List[str]] = "/", **kwargs):
    """
    Decorator that defines a route for the controller.

    Args:
        method (str): The HTTP method for the route (GET, POST, DELETE, PUT, PATCH).
        path (Union[str, List[str]]): The URL path for the route.
        **kwargs: Additional keyword arguments to configure the route.

    Returns:
        function: The decorated function.
    """

    def decorator(func):
        func.method = method
        func.__path__ = path
        func.__kwargs__ = kwargs

        return func

    return decorator





# Example usage:
# get_route = Get("/users")
# get_route_decorated = get_route(my_function)


# Decorator for defining a GET route with an optional path
Get: Callable[[Union[str, List[str]]], Callable[..., Any]] = lambda path="/", **kwargs: route("GET", path, **kwargs)

# Decorator for defining a POST route with an optional path
Post: Callable[[Union[str, List[str]]], Callable[..., Any]] = lambda path="/", **kwargs: route("POST", path, **kwargs)

# Decorator for defining a DELETE route with an optional path
Delete: Callable[[Union[str, List[str]]], Callable[..., Any]] = lambda path="/", **kwargs: route("DELETE", path, **kwargs)

# Decorator for defining a PUT route with an optional path
Put: Callable[[Union[str, List[str]]], Callable[..., Any]] = lambda path="/", **kwargs: route("PUT", path, **kwargs)

# Decorator for defining a PATCH route with an optional path
Patch: Callable[[Union[str, List[str]]], Callable[..., Any]] = lambda path="/", **kwargs: route("PATCH", path, **kwargs)

# def Controller(tag: str = None, prefix: str = None):
#     """
#     Decorator that turns a class into a controller, allowing you to define routes using FastAPI decorators.

#     Args:
#         tag (str, optional): The tag to use for OpenAPI documentation.
#         prefix (str, optional): The prefix to use for all routes.

#     Returns:
#         class: The decorated class.

#     """
#     # Use tag as default prefix if prefix is None
#     if prefix is None:
#         prefix = tag

#     # Ensure prefix has correct formatting
#     if prefix:
#         prefix = "/" + prefix.rstrip("/") if not prefix.startswith("/") else prefix.rstrip("/")

#     def wrapper(cls) -> ClassBasedView:
#         router = APIRouter(tags=[tag] if tag else None)

#         http_method_names = ("GET", "POST", "PUT", "DELETE", "PATCH")

#         for name, method in cls.__dict__.items():
#             if callable(method) and hasattr(method, "method"):
                
#                 # Check if method is decorated with an HTTP method decorator
#                 assert hasattr(method, "__path__") and method.__path__, f"Missing path for method {name}"

#                 http_method = method.method
#                 # Ensure that the method is a valid HTTP method
#                 assert http_method in http_method_names, f"Invalid method {http_method}"

#                 # Process single path or list of paths
#                 paths = method.__path__ if isinstance(method.__path__, list) else [method.__path__]
#                 for path in paths:
#                     if prefix and isinstance(path, str):
#                         method.__path__ = f"{prefix.rstrip('/')}/{path.lstrip('/')}" if path else prefix.rstrip('/')
                    
#                     # Set default status code if  provided in @HttpCode decorator
#                     if  hasattr(method, STATUS_CODE_TOKEN) and method.__kwargs__.get(STATUS_CODE_TOKEN) is None:
#                         method.__kwargs__[STATUS_CODE_TOKEN] = method.__dict__[STATUS_CODE_TOKEN]
#                     router.add_api_route(method.__path__, method, methods=[http_method], **method.__kwargs__)

                    
#         def get_router() -> APIRouter:
#             """
#             Returns:
#                 APIRouter: The router associated with the controller.
#             """
#             return router

#         cls.get_router = get_router

#         return ClassBasedView(router=router, cls=cls)

#     return wrapper