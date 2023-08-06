from .client import Client as _Client


iei = _Client()
connections = iei.extract_connections()


__all__ = [ 'iei', 'connections' ]
