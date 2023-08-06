from .client import Client as _Client


compass = _Client()
connections = compass.extract_connections()


__all__ = [ 'compass', 'connections' ]
