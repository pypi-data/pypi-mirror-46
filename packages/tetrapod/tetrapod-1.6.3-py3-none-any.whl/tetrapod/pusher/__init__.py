from .client import Client as _Client


pusher = _Client()
connections = pusher.extract_connections()

__all__ = [ 'pusher', 'connections' ]
