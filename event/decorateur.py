from typing import Any, Callable, Optional, TypeVar

T = TypeVar("T")

EVENT_LISTENER_METADATA = "event_listener_metadata"

class OnEventMetadata:
    def __init__(self, event: str, options: Optional[Any] = None):
        self.event = event
        self.options = options

def OnEvent(event: str, options: Optional[Any] = None) -> Callable[..., T]:
    def decorator_factory(func: Callable[..., T]) -> Callable[..., T]:
        metadata = {"on_envent_metadata": OnEventMetadata(event, options), "func": func}
        setattr(func, EVENT_LISTENER_METADATA, metadata)
        return func
    return decorator_factory

# Exemple d'utilisation du décorateur
@OnEvent('user.password_configuration', options={'priority': 1})
def passwordConfiguration(data: Any) -> Any:
    print(f"Handling pas sword configuration with data: {data}")
    # Votre logique ici
    return data
