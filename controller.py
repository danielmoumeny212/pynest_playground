from fastapi.routing import APIRouter
from helpers import class_based_view as ClassBasedView
from constants import STATUS_CODE_TOKEN
from fastapi import Depends, status 


def Controller(tag: str = None, prefix: str = None):
    """
    Decorator that turns a class into a controller, allowing you to define routes using FastAPI decorators.

    Args:
        tag (str, optional): The tag to use for OpenAPI documentation.
        prefix (str, optional): The prefix to use for all routes.

    Returns:
        class: The decorated class.

    """
    # Use tag as default prefix if prefix is None
    if prefix is None:
        prefix = tag

    if not prefix.startswith("/"):
        prefix = "/" + prefix
    if prefix.endswith("/"):
        prefix = prefix[:-1]

    def wrapper(cls) -> ClassBasedView:
        router = APIRouter(tags=[tag] if tag else None)

        http_method_names = ("GET", "POST", "PUT", "DELETE", "PATCH")

        for name, method in cls.__dict__.items():
            if callable(method) and hasattr(method, "method"):
                # Check if method is decorated with an HTTP method decorator
                assert (
                    hasattr(method, "__path__") and method.__path__
                ), f"Missing path for method {name}"

                http_method = method.method
                # Ensure that the method is a valid HTTP method
                assert http_method in http_method_names, f"Invalid method {http_method}"
                if prefix:
                    method.__path__ = prefix + method.__path__
                if not method.__path__.startswith("/"):
                    method.__path__ = "/" + method.__path__
                if hasattr(method, STATUS_CODE_TOKEN) and method.__kwargs__.get(STATUS_CODE_TOKEN) is None: 
                    method.__kwargs__[STATUS_CODE_TOKEN] = method.__dict__[STATUS_CODE_TOKEN]
                router.add_api_route(
                    method.__path__, method, methods=[http_method], **method.__kwargs__
                )

        def get_router() -> APIRouter:
            """
            Returns:
                APIRouter: The router associated with the controller.
            """
            return router

        cls.get_router = get_router

        return ClassBasedView(router=router, cls=cls)

    return wrapper


def route(method: str, path: str = "/", **kwargs):
    """
    Decorator that defines a route for the controller.

    Args:
        method (str): The HTTP method for the route (GET, POST, DELETE, PUT, PATCH).
        path (str): The URL path for the route.
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

Get = lambda path="/", **kwargs: route("GET", path, **kwargs)
Post = lambda path="/", **kwargs: route("POST", path, **kwargs)
Delete = lambda path="/", **kwargs: route("DELETE", path, **kwargs)
Put = lambda path="/", **kwargs: route("PUT", path, **kwargs)
Patch = lambda path="/", **kwargs: route("PATCH", path, **kwargs)

